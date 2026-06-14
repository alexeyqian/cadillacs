from game.settings import *
from game.tuning import scale_frames
from game.entities.player_config import get_player_config
from game.entities.player_hitboxes import PlayerHitboxes
from game.entities.player_health import PlayerHealth
from game.entities.player_weapon_slot import PlayerWeaponSlot
from game.entities.player_movement import PlayerMovement
from game.entities.player_combat import PlayerCombat
from game.entities.player_grab_controller import PlayerGrabController
from game.entities.player_animation_controller import PlayerAnimationController
from game.entities.player_render import PlayerRenderer
from game.entities.player_action_controller import PlayerActionController

class Player:
    IDLE = "IDLE"
    WALK = "WALK"
    RUN="RUN"
    ATTACK = "ATTACK" # including 1,2,3
    RUN_ATTACK="RUN_ATTACK"
    JUMP = "JUMP"
    JUMP_ATTACK="JUMP_ATTACK"
    # punch combo
    ATTACK_1 = "ATTACK_1"
    ATTACK_2 = "ATTACK_2"
    ATTACK_3 = "ATTACK_3"
    HIT = "HIT" # hit by enemies
    DEAD = "DEAD"
    GRAB = "GRAB"
    GRAB_KNEE="GRAB_KNEE"
    THROW = "THROW"

    def __init__(self, player_type, animation_data, anim_fps):
        self.x = 300
        self.y = 500
        self.player_type = player_type
        self.state = self.IDLE
        self.apply_player_config(get_player_config(player_type))
        self.health = PlayerHealth(self.config_max_hp, self.config_lives, self.hit_stun_duration)

        self.facing_right = True

        self.movement = PlayerMovement(self.speed)
        self.movement.ground_y = self.y
        self.run_attack_timer = 0
        self.run_attack_duration = 18
        self.jump_attack_pressed = False
        self.jump_attack_duration = self.run_attack_duration
        self.respawn_x = self.x
        self.respawn_y = self.y

        self.combat = PlayerCombat()
        self.weapon_slot = PlayerWeaponSlot()
        self.action_controller = PlayerActionController()
        self.grab = PlayerGrabController()
        self.hitboxes = PlayerHitboxes()
        self.animation_controller = PlayerAnimationController(self, animation_data, anim_fps)
        self.renderer = PlayerRenderer()

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
        self.hit_stun_duration = scale_frames(config.hit_stun_duration)
        self.sprite_scale = config.sprite_scale
    
    def get_current_player_frame(self):
        return self.animation_controller.get_current_frame()

    def get_current_animation_frame_index(self):
        return self.animation_controller.get_current_frame_index()

    # update() works in world coordinates
    # draw() translates to screen coordinates using camera_x
    def update(self, player_input):
        if self.state == self.DEAD:
            self.update_dead_state()
            return

        if self.update_hit_state():
            return

        self.update_timers()
        moving = self.update_movement(player_input)
        self.action_controller.update(self, player_input)
        self.update_jump_physics(player_input)
        self.update_state_after_movement(moving)
        self.update_grabbed_enemy_position()
        #self.apply_world_bounds() # moved to gameplay_system.py
        self.update_animation()


    def draw(self, screen, camera_x):
        self.renderer.draw(self, screen, camera_x)

    def get_left(self):
        return self.get_frame_rect().left

    def get_top(self):
        return self.get_frame_rect().top
    
    def get_right(self):
        return self.get_frame_rect().right
    
    def get_bottom(self):
        return self.get_frame_rect().bottom

    def get_frame_rect(self):
        return self.hitboxes.get_frame_rect(self)

    # TODO: deprecated
    def get_logical_rect(self):
        return self.get_frame_rect()

    def get_hurt_rect(self):
        return self.hitboxes.get_hurt_rect(self)

    # on bottom center
    def get_collision_rect(self):
        return self.hitboxes.get_collision_rect(self)

    # hit box
    def get_attack_rect(self):
        return self.hitboxes.get_attack_rect(self)

    def update_animation(self):
        self.animation_controller.update(self)

    def update_dead_state(self):
        self.update_respawn()
        self.update_animation()

    def update_hit_state(self):
        if self.health.hit_timer <= 0:
            return False

        still_in_hit_stun = self.health.update_hit_timer()
        if still_in_hit_stun:
            self.state = self.HIT
        else:
            self.state = self.IDLE

        self.update_animation()
        return True

    def update_timers(self):
        self.combat.update_timers(self)
        self.grab.update_timers(self)
        self.movement.update_timers()

    def update_movement(self, player_input):
        return self.movement.update_movement(self, player_input)

    def update_jump_physics(self, player_input):
        return self.movement.update_jump_physics(self, player_input)

    def update_state_after_movement(self, moving):
        # update state (preserve attack state if attacking)
        if self.combat.is_attacking:
            return
            #pass # keep attack state and animation set by start_attack
        if self.movement.is_jumping:
            if self.state != self.JUMP_ATTACK:
                self.state = self.JUMP
            return

        elif self.grab.throw_timer > 0:
            self.state = self.THROW
        elif self.grab.grab_knee_timer > 0:
            self.state = self.GRAB_KNEE
        elif self.grab.grabbed_enemy:
            self.state = self.GRAB
        else:
            if moving and self.movement.is_running:
                self.state = self.RUN
            elif moving:
                    self.state = self.WALK
            else:
                self.state = self.IDLE

    def update_grabbed_enemy_position(self):
        self.grab.update_grabbed_enemy_position(self)

    def apply_world_bounds(self, world_width=None, lane_top=None, lane_bottom=None):
        self.movement.apply_world_bounds(self, world_width, lane_top, lane_bottom)

    def start_jump(self, player_input):
        self.movement.start_jump(self, player_input)

    def start_jump_attack(self):
        self.combat.start_jump_attack(self)
    
    def start_attack(self):
        self.combat.start_attack(self)

    def start_grab_knee_attack(self):
        self.combat.start_grab_knee_attack(self)

    def attack_damage(self):
        return self.combat.attack_damage(self)

    def take_damage(self, damage):
        if self.state == self.DEAD:
            return

        lost_life = self.health.take_damage(damage)
        self.state = self.HIT

        if lost_life:
            self.lost_life()

    def lost_life(self):
        self.state = self.DEAD
        
    def update_respawn(self):
        if self.state != self.DEAD:
            return
        if self.health.lives <= 0:
            return
        if self.health.update_respawn_timer():
            self.respawn()
            
    def respawn(self):
        self.health.reset_for_respawn()
        self.x = self.respawn_x
        self.y = self.respawn_y
        self.movement.ground_y = self.respawn_y
        self.movement.vx = 0
        self.movement.vy = 0
        self.movement.is_jumping = False
        self.state = self.IDLE
        self.combat.is_attacking = False
        self.grab.grabbed_enemy = None

    def pick_up_weapon(self, weapon):
        self.weapon_slot.pick_up(weapon)

    def drop_weapon(self):
        self.weapon_slot.drop(self)

    def fire_weapon(self):
        self.weapon_slot.fire(self)
        
    def can_grab_enemy(self, enemy):
        return self.grab.can_grab_enemy(self, enemy)
    
    def grab_enemy(self, enemy):
        self.grab.grab_enemy(self, enemy)
        
    def throw_grabbed_enemy(self):
        self.grab.throw_grabbed_enemy(self)
