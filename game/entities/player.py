from game.entities.character import Character
from game.entities.player_state import PlayerState
from game.data.player_config import get_player_config
from game.components.character_health import CharacterHealth
from game.components.character_geometry import CharacterGeometry
from game.components.player_intent import PlayerIntent
from game.components.player_weapon_slot import PlayerWeaponSlot
from game.components.player_movement import PlayerMovement
from game.controllers.player_combat_controller import PlayerCombatController
from game.controllers.player_grab_controller import PlayerGrabController
from game.controllers.player_animation_controller import PlayerAnimationController
from game.components.player_renderer import PlayerRenderer
from game.controllers.player_action_controller import PlayerActionController
from game.controllers.player_state_controller import PlayerStateController
from game.controllers.player_lifecycle_controller import PlayerLifecycleController
from game.controllers.player_reaction_controller import PlayerReactionController
from game.combat.damage_request import DamageRequest
from game.core.events import GameEventQueue
from game.entities.player_state_machine import PlayerStateMachine
from game.input.input_buffer import InputBuffer
from game.input.player_input_state import PlayerInputState
from game.components.player_air_state import PlayerAirState

class Player(Character, PlayerState):
    def __init__(self, player_type, animation_data, anim_fps=None):
        super().__init__(x=300, y=500, state=self.IDLE, facing_right=True)
        self.player_type = player_type

        self._configure_from_player_config(
            get_player_config(player_type),
            animation_data, anim_fps)

    ##### begin of init #####
    def _configure_from_player_config(self, config, animation_data, anim_fps=None):
        self.apply_identity_config(config)
        self.apply_body_config(config)
        self.apply_movement_config(config)
        self.build_state_components(config)
        self.build_input_components()
        self.build_capability_components()
        self.build_controllers(config)
        self.apply_combat_config(config)
        self.build_presentation_components(animation_data, anim_fps)

    def apply_identity_config(self, config):
        self.player_id = config.player_id
        self.display_name = config.display_name

    def apply_body_config(self, config):
        self.width = int(config.width)
        self.height = int(config.height)
        self.geometry = CharacterGeometry()
        self.geometry.configure(
            config.collision_box_w,
            config.collision_box_h,
            config.hurt_box_w,
            config.hurt_box_h,
            config.hurt_box_offset_x,
            config.hurt_box_offset_y,
        )
        self.health = CharacterHealth(config.max_hp)
        self.sprite_scale = config.sprite_scale

    def apply_movement_config(self, config):
        self.speed = config.speed
        self.run_speed = config.run_speed
        self.run_attack_min_distance = config.run_attack_min_distance

    def apply_combat_config(self, config):
        self.combat_controller.attacks = config.attacks or {}
        self.combat_controller.weapon_attacks = config.weapon_attacks or {}
        self.grab_controller.grab_range = config.grab_range

    def build_state_components(self, config):
        self.air = PlayerAirState(
            config.jump_power,
            config.jump_gravity,
            config.air_move_speed,
            config.jump_takeoff_frames,
            config.landing_recovery_frames,
        )
        self.state_machine = PlayerStateMachine(self)

    def build_input_components(self):
        self.intent = PlayerIntent()
        self.input_buffer = InputBuffer()
        self.input_state = PlayerInputState()

    def build_capability_components(self):
        self.movement = PlayerMovement(
            self.air,
            run_attack_min_distance=self.run_attack_min_distance,
        )
        self.weapon_slot = PlayerWeaponSlot()
        self.events = GameEventQueue()

    def build_controllers(self, config):
        self.combat_controller = PlayerCombatController()
        self.action_controller = PlayerActionController()
        self.grab_controller = PlayerGrabController()
        self.state_controller = PlayerStateController()
        self.lifecycle_controller = PlayerLifecycleController(self.x, self.y, config.lives)
        self.reaction_controller = PlayerReactionController(config.hit_stun_duration)

    def build_presentation_components(self, animation_data, anim_fps=None):
        self.animation_controller = PlayerAnimationController(self, animation_data, anim_fps)
        self.renderer = PlayerRenderer()

    ##### end of init #####

    ##### begin of main loop update #####

    def update_lifecycle_state(self):
        if self.state == self.DEAD:
            self.lifecycle_controller.update_dead_state(self)

    def update_reactions(self):
        was_in_hit_stun = self.reaction_controller.is_in_hit_stun()
        self.reaction_controller.update_hit_state(self)
        return was_in_hit_stun

    def advance_timers(self):
        self.action_controller.advance_timers(self)
        self.combat_controller.advance_timers(self)
        self.grab_controller.advance_timers(self)
        self.movement.advance_timers()

    def request_actions(self, context):
        self.action_controller.update(self, context.player_input)

    def update_movement(self, context):
        self._try_start_requested_jump()
        self.movement.update_movement(self, context.player_input)
        self.movement.update_jump_physics(self, context.player_input)
        self.state_controller.update_after_movement(self, self.movement.moving)
        self.grab_controller.update_grabbed_enemy_position(self)

    def update_attack(self, context=None):
        self._try_start_requested_fire()
        attack_was_requested = self.intent.wants_attack()
        if attack_was_requested:
            self._try_start_requested_attack(clear_if_failed=False)
        self.combat_controller.update_attack(self)
        if attack_was_requested and self.intent.wants_attack():
            self._try_start_requested_attack()

    def update_animation(self):
        self.animation_controller.update(self)

    ##### end of main loop update #####

    # todo: move to stage controller/manager?
    def reset_for_stage_start(self, x, y):
        self.lifecycle_controller.reset_for_stage_start(self, x, y)

    def get_attack_data(self, attack_name):
        weapon = self.weapon_slot.weapon
        weapon_type = weapon.weapon_type if weapon else None
        weapon_attack = self.combat_controller.weapon_attacks.get((weapon_type, attack_name))
        if weapon_attack and not weapon.is_ranged:
            return weapon_attack

        return self.combat_controller.attacks.get(attack_name)

    def _try_start_requested_jump(self):
        if not self.intent.wants_jump():
            return

        previous_state = self.state
        self.movement.start_jump(self, self.intent.jump_input)
        if self.state != previous_state:
            self.input_buffer.consume(PlayerActionController.JUMP_ACTION)
        self.intent.clear_jump()

    def _try_start_requested_fire(self):
        if not self.intent.wants_fire():
            return

        self.weapon_slot.fire(self)
        self.intent.clear_fire()

    def _try_start_requested_attack(self, clear_if_failed=True):
        if not self.intent.wants_attack():
            return False

        previous_attack_name = self.combat_controller.current_attack_name

        if self.movement.is_jumping:
            self.combat_controller.start_jump_attack(self)
        elif self.grab_controller.grabbed_enemy:
            self.combat_controller.start_grab_knee_attack(self)
        else:
            self.combat_controller.start_attack(self)

        if self.combat_controller.current_attack_name != previous_attack_name:
            self.input_buffer.consume(PlayerActionController.ATTACK_ACTION)
            self.intent.clear_attack()
            return True

        if clear_if_failed:
            self.intent.clear_attack()
        return False

    def take_damage(self, damage, reaction=None):
        if isinstance(damage, DamageRequest):
            reaction = damage.reaction
            damage = damage.damage

        self.reaction_controller.take_damage(
            self,
            damage,
            reaction=reaction,
        )

    # todo: should return hurbox top?
    def get_top(self):
        return self.get_frame_rect().top
