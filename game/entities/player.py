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
from game.controllers.player_state_resolver import PlayerStateResolver
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

    # --- Init ---

    def _configure_from_player_config(self, config, animation_data, anim_fps=None):
        self._apply_identity_config(config)
        self._apply_body_config(config)
        self._build_state_components(config)
        self._build_input_components()
        self._build_capability_components(config)
        self._build_controllers(config)
        self._apply_combat_config(config)
        self._build_presentation_components(animation_data, anim_fps)

    def _apply_identity_config(self, config):
        self.player_id = config.player_id
        self.display_name = config.display_name

    def _apply_body_config(self, config):
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

    def _build_state_components(self, config):
        self.air = PlayerAirState(
            config.jump_power,
            config.jump_gravity,
            config.air_move_speed,
        )
        self.state_machine = PlayerStateMachine(self)

    def _build_input_components(self):
        self.intent = PlayerIntent()
        self.input_buffer = InputBuffer()
        self.input_state = PlayerInputState()

    def _build_capability_components(self, config):
        self.movement = PlayerMovement(
            self.air,
            run_attack_min_distance=config.run_attack_min_distance,
        )
        self.speed = config.speed
        self.run_speed = config.run_speed
        self.weapon_slot = PlayerWeaponSlot()
        self.events = GameEventQueue()

    def _build_controllers(self, config):
        self.combat_controller = PlayerCombatController()
        self.action_controller = PlayerActionController()
        self.grab_controller = PlayerGrabController()
        self.state_resolver = PlayerStateResolver()
        self.lifecycle_controller = PlayerLifecycleController(self.x, self.y, config.lives)
        self.reaction_controller = PlayerReactionController(config.hit_stun_duration)

    def _apply_combat_config(self, config):
        self.combat_controller.attacks = config.attacks or {}
        self.combat_controller.weapon_attacks = config.weapon_attacks or {}
        self.grab_controller.grab_range = config.grab_range

    def _build_presentation_components(self, animation_data, anim_fps=None):
        self.animation_controller = PlayerAnimationController(self, animation_data, anim_fps)
        self.renderer = PlayerRenderer()

    # --- Per-frame update (called by systems) ---

    def update_reactions(self):
        self.reaction_controller.update_hit_state(self)

    def advance_timers(self):
        self.action_controller.advance_timers(self)
        self.combat_controller.advance_timers(self)
        self.grab_controller.advance_timers(self)
        self.movement.advance_timers()

    def request_actions(self, context):
        self.action_controller.update(self, context.player_input)

    def update_movement(self, context):
        self._try_start_jump()
        self.movement.update_movement(self, context.player_input)
        self.movement.update_jump_physics(self, context.player_input)
        self.state_resolver.resolve(self, self.movement.moving)
        self.grab_controller.update_grabbed_enemy_position(self)

    def update_attack(self, context=None):
        self._try_start_fire()
        attack_was_requested = self.intent.wants_attack()
        if attack_was_requested:
            self._try_start_attack(clear_if_failed=False)
        self.combat_controller.update_attack(self)
        if attack_was_requested and self.intent.wants_attack():
            self._try_start_attack()

    def update_animation(self):
        self.animation_controller.update(self)

    def update_lifecycle_state(self):
        self.lifecycle_controller.update_respawn(self)

    # --- Public API ---

    def take_damage(self, damage, reaction=None):
        if isinstance(damage, DamageRequest):
            reaction = damage.reaction
            damage = damage.damage
        self.reaction_controller.take_damage(self, damage, reaction)

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

    # todo: should return hurtbox top?
    def get_top(self):
        return self.get_frame_rect().top

    # --- Private helpers ---

    def _try_start_jump(self):
        if not self.intent.wants_jump():
            return
        previous_state = self.state
        self.movement.start_jump(self, self.intent.jump_input)
        if self.state != previous_state:
            self.input_buffer.consume(PlayerActionController.JUMP_ACTION)
        self.intent.clear_jump()

    def _try_start_fire(self):
        if not self.intent.wants_fire():
            return
        self.weapon_slot.fire(self)
        self.intent.clear_fire()

    def _try_start_attack(self, clear_if_failed=True):
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
