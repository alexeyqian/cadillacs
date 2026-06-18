from game.settings import *
from game.entities.player_config import get_player_config
from game.entities.player_geometry import PlayerGeometry
from game.entities.player_health import PlayerHealth
from game.entities.player_weapon_slot import PlayerWeaponSlot
from game.entities.player_movement import PlayerMovement
from game.entities.player_combat_controller import PlayerCombatController
from game.entities.player_grab_controller import PlayerGrabController
from game.entities.player_animation_controller import PlayerAnimationController
from game.entities.player_renderer import PlayerRenderer
from game.entities.player_action_controller import PlayerActionController
from game.entities.player_state_resolver import PlayerStateResolver
from game.entities.player_lifecycle_controller import PlayerLifecycleController
from game.entities.player_events import PlayerEvents
from game.entities.player_state_machine import PlayerStateMachine
from game.entities.player_input_state import PlayerInputState
from game.entities.player_air_state import PlayerAirState

class Player:
    IDLE = "IDLE"
    WALK = "WALK"
    RUN="RUN"
    ATTACK = "ATTACK" # including 1,2,3
    RUN_ATTACK="RUN_ATTACK"
    JUMP_TAKEOFF = "JUMP_TAKEOFF"
    JUMP = "JUMP"
    JUMP_ATTACK="JUMP_ATTACK"
    LANDING = "LANDING"
    # punch combo
    ATTACK_1 = "ATTACK_1"
    ATTACK_2 = "ATTACK_2"
    ATTACK_3 = "ATTACK_3"
    HIT = "HIT" # hit by enemies
    RECOIL = "RECOIL"
    DEAD = "DEAD"
    GRAB = "GRAB"
    GRAB_KNEE="GRAB_KNEE"
    THROW = "THROW"

    def __init__(self, player_type, animation_data, anim_fps):
        self.player_type = player_type

        # Identity / position
        self.x = 300
        self.y = 500
        self.facing_right = True

        # Core state
        self.state = self.IDLE
        self.state_machine = PlayerStateMachine(self)

        self.apply_player_config(get_player_config(player_type))

        self.air = PlayerAirState(
            self.jump_power,
            self.jump_gravity,
            self.air_move_speed,
            self.jump_takeoff_frames,
            self.landing_recovery_frames,
        )

        # Health
        self.health = PlayerHealth(self.config_max_hp, self.config_lives, self.hit_stun_duration)

        # Input edge flags
        # stop the “hold attack to auto-combo” problem.
        # expected gameplay for attack and attack combo:
        # Hold J: one punch only
        # Press J, release, press J: combo advances
        # Mashing J: combo still works, but requires timing/input
        self.input_state = PlayerInputState()

        # Components
        self.movement = PlayerMovement(self.speed, self.air)
        self.movement.ground_y = self.y
        self.combat = PlayerCombatController()
        self.action_controller = PlayerActionController()
        self.grab = PlayerGrabController()
        self.state_resolver = PlayerStateResolver()
        self.lifecycle = PlayerLifecycleController(self.x, self.y)
        self.weapon_slot = PlayerWeaponSlot()
        self.events = PlayerEvents()
        self.geometry = PlayerGeometry()
        self.animation_controller = PlayerAnimationController(self, animation_data, anim_fps)
        self.renderer = PlayerRenderer()

    # Config
    def apply_player_config(self, config):
        self.player_id = config.player_id
        self.display_name = config.display_name
        self.width = int(config.width)
        self.height = int(config.height)
        self.collision_box_w = int(config.collision_box_w)
        self.collision_box_h = int(config.collision_box_h)
        self.config_max_hp = config.max_hp
        self.config_lives = config.lives
        self.speed = config.speed
        self.run_speed = config.run_speed
        self.run_attack_damage = config.run_attack_damage
        self.jump_attack_damage = config.jump_attack_damage
        self.grab_range = config.grab_range
        self.hit_stun_duration = config.hit_stun_duration
        self.sprite_scale = config.sprite_scale
        self.jump_power = config.jump_power
        self.jump_gravity = config.jump_gravity
        self.air_move_speed = config.air_move_speed
        self.jump_takeoff_frames = config.jump_takeoff_frames
        self.landing_recovery_frames = config.landing_recovery_frames

    # update() works in world coordinates
    # draw() translates to screen coordinates using camera_x
    # Update flow
    def update(self, player_input):
        if self.state == self.DEAD:
            self.lifecycle.update_dead_state(self)
            return

        if self.lifecycle.update_hit_state(self):
            return

        self.update_timers()
        moving = self.movement.update_movement(self, player_input)
        self.action_controller.update(self, player_input)
        self.movement.update_jump_physics(self, player_input)
        self.state_resolver.update_after_movement(self, moving)
        self.grab.update_grabbed_enemy_position(self)
        self.animation_controller.update(self)

    # Timers
    def update_timers(self):
        self.combat.update_timers(self)
        self.grab.update_timers(self)
        self.movement.update_timers()

    # Lifecycle / damage
    def take_damage(self, damage, hit_stun_bonus=0):
        self.lifecycle.take_damage(self, damage, hit_stun_bonus)

    # Movement / bounds
    def apply_world_bounds(self, world_width=None, lane_top=None, lane_bottom=None):
        self.movement.apply_world_bounds(self, world_width, lane_top, lane_bottom)

    # Rendering
    def draw(self, screen, camera_x):
        self.renderer.draw(self, screen, camera_x)

    # Geometry
    def get_left(self):
        return self.get_frame_rect().left

    def get_top(self):
        return self.get_frame_rect().top
    
    def get_right(self):
        return self.get_frame_rect().right
    
    def get_bottom(self):
        return self.get_frame_rect().bottom

    def get_frame_rect(self):
        return self.geometry.get_frame_rect(self)

    def get_hurt_rect(self):
        return self.geometry.get_hurt_rect(self)

    def get_counter_hurt_rect(self):
        # TODO: disable counter_hurt_rect for now, in future, 
        # just remove it for simplification
        return None
        return self.geometry.get_counter_hurt_rect(self)

    # on bottom center
    def get_collision_rect(self):
        return self.geometry.get_collision_rect(self)

    # hit box
    def get_attack_rect(self):
        return self.geometry.get_attack_rect(self)
