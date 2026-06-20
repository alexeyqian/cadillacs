from game.entities.character import Character
from game.entities.player_state import PlayerState
from game.data.player_config import get_player_config
from game.components.character_geometry import CharacterGeometry
from game.entities.player_health import PlayerHealth
from game.components.player_weapon_slot import PlayerWeaponSlot
from game.components.player_movement import PlayerMovement
from game.controllers.player_combat_controller import PlayerCombatController
from game.controllers.player_grab_controller import PlayerGrabController
from game.controllers.player_animation_controller import PlayerAnimationController
from game.components.player_renderer import PlayerRenderer
from game.controllers.player_action_controller import PlayerActionController
from game.controllers.player_state_controller import PlayerStateController
from game.controllers.player_lifecycle_controller import PlayerLifecycleController
from game.combat.damage_request import DamageRequest
from game.core.events import GameEventQueue
from game.entities.player_state_machine import PlayerStateMachine
from game.input.input_buffer import InputBuffer
from game.input.player_input_state import PlayerInputState
from game.components.player_air_state import PlayerAirState

class Player(Character, PlayerState):
    def __init__(self, player_type, animation_data, anim_fps):
        super().__init__(x=300, y=500, state=self.IDLE, facing_right=True)
        self.player_type = player_type

        self.configure_from_player_config(
            get_player_config(player_type),
            animation_data, anim_fps)

    # Construction groups
    def configure_from_player_config(self, config, animation_data, anim_fps):
        self.apply_identity_config(config)
        self.apply_body_config(config)
        self.apply_movement_config(config)
        self.build_state_components(config)
        self.build_input_components()
        self.build_capability_components()
        self.build_controllers()
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
        self.health = PlayerHealth(config.max_hp, config.lives, config.hit_stun_duration)
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
        self.input_buffer = InputBuffer()
        self.input_state = PlayerInputState()

    def build_capability_components(self):
        self.movement = PlayerMovement(
            self.air,
            run_attack_min_distance=self.run_attack_min_distance,
        )
        self.weapon_slot = PlayerWeaponSlot()
        self.events = GameEventQueue()

    def build_controllers(self):
        self.combat_controller = PlayerCombatController()
        self.action_controller = PlayerActionController()
        self.grab_controller = PlayerGrabController()
        self.state_controller = PlayerStateController()
        self.lifecycle_controller = PlayerLifecycleController(self.x, self.y)

    def build_presentation_components(self, animation_data, anim_fps):
        self.animation_controller = PlayerAnimationController(self, animation_data, anim_fps)
        self.renderer = PlayerRenderer()

    def reset_for_stage_start(self, x, y):
        self.lifecycle_controller.reset_for_stage_start(self, x, y)

    def update(self, player_input):
        if self.update_lifecycle_state():
            self.update_animation()
            return

        self.advance_timers()
        self.request_actions(player_input)
        moving = self.update_movement(player_input)
        self.update_jump_physics(player_input)
        self.update_state_after_movement(moving)
        self.update_grabbed_enemy_position()
        self.update_animation()

    def update_lifecycle_state(self):
        if self.state == self.DEAD:
            self.lifecycle_controller.update_dead_state(self)
            return True

        if self.lifecycle_controller.update_hit_state(self):
            return True

        return False

    def request_actions(self, player_input):
        self.action_controller.update(self, player_input)

    def update_movement(self, player_input):
        return self.movement.update_movement(self, player_input)

    def update_jump_physics(self, player_input):
        self.movement.update_jump_physics(self, player_input)

    def update_state_after_movement(self, moving):
        self.state_controller.update_after_movement(self, moving)

    def update_grabbed_enemy_position(self):
        self.grab_controller.update_grabbed_enemy_position(self)

    def update_animation(self):
        self.animation_controller.update(self)

    # Timers
    def advance_timers(self):
        self.combat_controller.update_timers(self)
        self.grab_controller.update_timers(self)
        self.movement.update_timers()

    def get_attack_data(self, attack_name):
        weapon = self.weapon_slot.weapon
        weapon_type = weapon.weapon_type if weapon else None
        weapon_attack = self.combat_controller.weapon_attacks.get((weapon_type, attack_name))
        if weapon_attack and not weapon.is_ranged:
            return weapon_attack

        return self.combat_controller.attacks.get(attack_name)

    def take_damage(self, damage, reaction=None, hit_stun_bonus=0):
        if isinstance(damage, DamageRequest):
            reaction = damage.reaction
            damage = damage.damage

        self.lifecycle_controller.take_damage(
            self,
            damage,
            reaction=reaction,
            hit_stun_bonus=hit_stun_bonus,
        )

    # Geometry
    def get_left(self):
        return self.get_frame_rect().left

    def get_top(self):
        return self.get_frame_rect().top
    
    def get_right(self):
        return self.get_frame_rect().right
    
    def get_bottom(self):
        return self.get_frame_rect().bottom
