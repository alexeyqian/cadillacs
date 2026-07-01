from game.entities.character import Character
from game.entities.player_state import PlayerState
from game.data.player_config import get_player_config
from game.components.character_health import CharacterHealth
from game.components.character_geometry import CharacterGeometry
from game.components.player_intent import PlayerIntent
from game.components.player_weapon_slot import PlayerWeaponSlot
from game.components.player_movement import PlayerMovement
from game.components.player_combat_state import PlayerCombatState
from game.components.player_grab_state import PlayerGrabState
from game.components.player_lifecycle_state import PlayerLifecycleState
from game.components.player_reaction_state import PlayerReactionState
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


class Player(Character, PlayerState):
    def __init__(self, player_type, animation_data, anim_fps=None):
        super().__init__(x=300, y=500, state=self.IDLE, facing_right=True)
        self.player_type = player_type
        self._configure_from_player_config(
            get_player_config(player_type),
            animation_data, anim_fps)

    # --- Init ---

    def _configure_from_player_config(self, config, animation_data, anim_fps=None):
        self.player_id = config.player_id
        self.display_name = config.display_name
        self.width = int(config.width)
        self.height = int(config.height)
        self.sprite_scale = config.sprite_scale
        self.speed = config.speed
        self.run_speed = config.run_speed

        self._build_components(config)
        self._build_controllers(config, animation_data, anim_fps)

    def _build_components(self, config):
        self.geometry = CharacterGeometry(
            config.collision_box_w,
            config.collision_box_h,
            config.hurt_box_w,
            config.hurt_box_h,
            config.hurt_box_offset_x,
            config.hurt_box_offset_y,
        )
        self.health = CharacterHealth(config.max_hp)
        self.state_machine = PlayerStateMachine(self)

        self.input_buffer = InputBuffer()
        self.input_state = PlayerInputState()
        self.intent = PlayerIntent()

        self.combat_state = PlayerCombatState()
        self.grab_state = PlayerGrabState()
        self.combat_state.attacks = config.attacks or {}
        self.combat_state.weapon_attacks = config.weapon_attacks or {}
        self.grab_state.grab_range = config.grab_range
        self.reaction_state = PlayerReactionState(config.hit_stun_duration)
        self.lifecycle_state = PlayerLifecycleState(self.x, self.y, config.lives)
        self.movement = PlayerMovement(
            jump_power=config.jump_power,
            gravity=config.jump_gravity,
            air_move_speed=config.air_move_speed,
            run_attack_min_distance=config.run_attack_min_distance,
        )
        self.weapon_slot = PlayerWeaponSlot()
        self.events = GameEventQueue()


    def _build_controllers(self, config, animation_data, anim_fps):
        self.combat_controller = PlayerCombatController()
        self.action_controller = PlayerActionController()
        self.grab_controller = PlayerGrabController()
        self.state_resolver = PlayerStateResolver()
        self.lifecycle_controller = PlayerLifecycleController()
        self.reaction_controller = PlayerReactionController()
        self.animation_controller = PlayerAnimationController(self, animation_data, anim_fps)
        self.renderer = PlayerRenderer()


    # --- Cross-controller coordination ---

    def _cancel_combat_commitment(self):
        self.combat_controller.cancel_attack(self)
        self.movement.attack_movement.cancel_run_attack_momentum()
        self.movement.attack_movement.cancel_combo_finisher_nudge()
        self.grab_state.grabbed_enemy = None

    def _on_death(self):
        self.lifecycle_controller.lose_life(self)
        self.lifecycle_controller.enter_dead_state(self)

    def _end_grab_knee(self):
        self.combat_state.attack_manager.cancel()
        self.combat_controller.set_action_lock(self, self.combat_state.grab_knee_recovery_duration)

    def _set_action_lock(self, duration):
        self.combat_controller.set_action_lock(self, duration)

    # --- Per-frame update (called by systems) ---

    
    def request_actions(self, context):
        self.action_controller.request_actions(self, context.player_input)

    def update_movement(self, context):
        if not self.can_act():
            return
        if self.state == self.GRAB:
            self._try_throw_from_direction(context.player_input)
            return
        self._try_start_jump()
        self.movement.update_movement(self, context.player_input)
        self.movement.jump_movement.update_jump_physics(self, context.player_input)
        self.state_resolver.resolve(self, self.movement.moving)
        self.grab_controller.update_grabbed_enemy_position(self)

    def _try_throw_from_direction(self, player_input):
        if player_input.right:
            self.facing_right = True
            self.grab_controller.throw_grabbed_enemy(self)
        elif player_input.left:
            self.facing_right = False
            self.grab_controller.throw_grabbed_enemy(self)

    def update_attack(self, context=None):
        if not self.can_act():
            return
        self._try_start_fire()
        if self.intent.wants_attack():
            self._try_start_attack(clear_if_failed=False)
        self.combat_controller.update_attack(self)
        if self.intent.wants_attack():
            self._try_start_attack()

    def update_animation(self):
        self.animation_controller.update(self)

    def update_lifecycle_state(self):
        self.lifecycle_controller.update_respawn(self)

    def update_reactions(self):
        self.reaction_controller.update_hit_state(self)

    def advance_timers(self):
        self.input_buffer.advance_timers()
        self.combat_controller.advance_timers(self)
        self.grab_controller.advance_timers(self)
        self.movement.run_movement.advance_timers()

    # --- Public API ---
    
    def can_act(self):
        is_blocked = self.state == self.DEAD or self.reaction_controller.is_in_hit_stun(self)
        return not is_blocked

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
        weapon_attack = self.combat_state.weapon_attacks.get((weapon_type, attack_name))
        if weapon_attack and not weapon.is_ranged:
            return weapon_attack
        return self.combat_state.attacks.get(attack_name)

    # todo: should return hurtbox top?
    def get_top(self):
        return self.get_frame_rect().top

    # --- Private helpers ---

    def _try_start_jump(self):
        if not self.intent.wants_jump():
            return
        previous_state = self.state
        self.movement.jump_movement.start_jump(self, self.intent.jump_input)
        if self.state != previous_state:
            self.input_buffer.consume_jump()
        self.intent.clear_jump()

    def _try_start_fire(self):
        weapon = self.weapon_slot.weapon
        if not weapon or not weapon.is_ranged:
            return
        if not self.intent.wants_attack():
            return
        self.weapon_slot.fire(self)
        self.intent.clear_attack()

    def _try_start_attack(self, clear_if_failed=True):
        if not self.intent.wants_attack():
            return False
        previous_attack_name = self.combat_state.current_attack_name
        if self.movement.is_jumping:
            self.combat_controller.start_jump_attack(self)
        elif self.grab_state.grabbed_enemy:
            self.combat_controller.start_grab_knee_attack(self)
        else:
            self.combat_controller.start_attack(self)
        if self.combat_state.current_attack_name != previous_attack_name:
            self.input_buffer.consume_attack()
            self.intent.clear_attack()
            return True
        if clear_if_failed:
            self.intent.clear_attack()
        return False
