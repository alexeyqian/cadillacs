from dataclasses import dataclass
from typing import Optional
import pygame
from game.settings import *
from game.colors import *
from game.entities.projectile import Projectile
from game.assets.placeholder.player_frames import *
from game.assets.asset_manager import AssetManager
from game.animation.animation import Animation
from game.animation.animation_manager import AnimationManager
from game.animation.animation_config import *
from game.animation.mustapha_data import MUSTAPHA_ANIMATIONS

@dataclass
class PlayerFrame:
    image: pygame.Surface
    offset: tuple
    hurt_rect: tuple
    attack_rect: Optional[tuple]

class PlayerFrameAnimation:
    def __init__(self, frames, frame_duration=8):
        self.frames = frames
        self.frame_duration = frame_duration
        self.current_frame = 0
        self.timer = 0

    def update(self):
        self.timer += 1
        if self.timer >= self.frame_duration:
            self.timer = 0
            self.current_frame += 1
            if self.current_frame >= len(self.frames):
                self.current_frame = 0

    def get_image(self):
        return self.frames[self.current_frame].image

    def get_frame_data(self):
        return self.frames[self.current_frame]

    def reset(self):
        self.current_frame = 0
        self.timer = 0

    def get_frame_index(self):
        return self.current_frame
    
    # not used yet
    def wrap_surface_frames(self, surfaces):
        frames = []

        for surface in surfaces:
            width = surface.get_width()
            height = surface.get_height()

            frames.append(PlayerFrame(
                image=surface,
                offset=(-width // 2, -height),
                hurt_rect=None,
                attack_rect=None,
            ))

        return frames

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

    def __init__(self):
        self.x = 300
        self.y = 500
        # boxes
        # logical box
        self.width = PLAYER_W
        self.height = PLAYER_H
        self.sprite_scale = 2
        #collision box
        self.collision_box_w = PLAYER_COLLISION_W
        self.collision_box_h = PLAYER_COLLISION_H
        # hurt box
        self.hurtbox_w = PLAYER_HURTBOX_W
        self.hurtbox_h = PLAYER_HURTBOX_H
        self.hurtbox_offset_x = PLAYER_HURTBOX_OFFSET_X
        self.hurtbox_offset_y = PLAYER_HURTBOX_OFFSET_Y
        # attack box
        self.attack_hitbox_w = PLAYER_HITBOX_W
        self.attack_hitbox_h = PLAYER_HITBOX_H
        self.attack_hitbox_offset_y = PLAYER_HITBOX_OFFSET_Y

        self.speed = PLAYER_SPEED
        self.facing_right = True

        self.is_running = False
        self.run_speed = PLAYER_RUN_SPEED
        self.run_active = False
        self.run_direction = 0
        self.run_tap_timer = 0
        self.run_tap_window = max(1, int(RUN_DOUBLE_TAP_TIME * FPS))
        self.left_pressed = False
        self.right_pressed = False
        self.run_attack_damage = 35 # use scaler*normal_damage
        self.run_attack_timer = 0
        self.run_attack_duration = 18
        
        # jump / jump attack
        self.is_jumping = False
        self.jump_pressed = False
        self.jump_attack_pressed = False
        self.ground_y = self.y
        self.vx = 0
        self.vy = 0
        self.jump_power = -20
        self.gravity = 2
        self.air_speed = self.speed * 1.2
        self.air_friction = 0.92
        self.jump_attack_damage = FIST_DAMAGE + 10
        self.jump_attack_duration = self.run_attack_duration

        self.is_attacking = False
        self.attack_timer = 0
        self.attack_duration = 12
        self.already_hit_enemy = False # already_hit

        # classic combo system
        # J punch 1, J punch 2, J punch 3
        self.combo_step = 0
        self.combo_timer = 0

        self.state = self.IDLE
        self.max_hp = PLAYER_MAX_HP
        self.hp = self.max_hp
        self.hit_timer = 0 # hit by enemy
        self.lives = PLAYER_LIVES
        self.respawn_x = self.x
        self.respawn_y = self.y
        self.respawn_timer = 0

        self.weapon = None
        self.pending_projectile = None
        self.fire_pressed = False  # track K_k edge for single-shot firing
        self.drop_pressed = False  # track K_q edge for single-press drop
        
        # grab/throw
        self.grabbed_enemy = None
        self.grab_pressed = False
        self.grab_range = PLAYER_GRAB_RANGE
        self.throw_timer = 0
        self.throw_duration = 14
        self.grab_knee_timer = 0
        self.grab_knee_duration = PLAYER_GRAB_KNEE_DURATION
        self.grab_keen_hit_frame = PLAYER_GRAB_KNEE_HIT_FRAME

        # lane boundaries
        self.lane_top = LANE_TOP
        self.lane_bottom = LANE_BOTTOM
        
        self.animation_manager = AnimationManager()
        self.init_animations()
    
    def get_current_player_frame(self):
        animation = self.animation_manager.current_animation
        # only used for new per-frame metadata
        if hasattr(animation, "get_frame_data"):
            return animation.get_frame_data()
        return None
    
    def load_mustapha_animation(self, animation_key):
        config = MUSTAPHA_ANIMATIONS.get(animation_key)
        if not config:
            # return []
            raise ValueError(f"Missing player animation data: {animation_key}")

        sheet = pygame.image.load(config["file"]).convert_alpha()
        frames = []

        for frame_config in config["frames"]:
            frame_x, frame_y, frame_w, frame_h = frame_config["frame_rect"]

            image = pygame.Surface((frame_w, frame_h), pygame.SRCALPHA)
            image.blit(sheet, (0, 0), (frame_x, frame_y, frame_w, frame_h))

            frames.append(PlayerFrame(
                image=image,
                offset=frame_config["offset"],
                hurt_rect=frame_config.get("hurt_rect"),
                attack_rect=frame_config.get("attack_rect"),
            ))

        return frames

    def init_animations(self):
        idle_frames = self.load_mustapha_animation("idle")
        walk_frames = self.load_mustapha_animation("walk") 
        run_frames = self.load_mustapha_animation("run")
        jump_frames = self.load_mustapha_animation("jump")
        attack_frames = self.load_mustapha_animation("attack")
        run_attack_frames = self.load_mustapha_animation("run_attack")
        jump_attack_frames = self.load_mustapha_animation("jump_attack")
        grab_frames = self.load_mustapha_animation("grab")
        throw_frames = self.load_mustapha_animation("throw")
        grab_knee_frames = self.load_mustapha_animation("grab_knee")
        hit_frames = self.load_mustapha_animation("hit")
        dead_frames = self.load_mustapha_animation("dead")

        # compute frame durations (number of game frames each animation frame should last)
        idle_dur = max(1, int(FPS / ANIM_FPS_IDLE))
        walk_dur = max(1, int(FPS / ANIM_FPS_WALK))
        run_dur = max(1, int(FPS / ANIM_FPS_WALK))
        jump_dur = max(1, int(FPS / ANIM_FPS_WALK))
        attack_dur = max(1, int(FPS / ANIM_FPS_ATTACK))
        run_attack_dur = max(1, int(FPS / ANIM_FPS_RUN_ATTACK))
        jump_attack_dur = max(1, int(FPS / ANIM_FPS_JUMP_ATTACK))
        grab_dur = max(1, int(FPS / ANIM_FPS_GRAB))
        throw_dur = max(1, int(FPS / ANIM_FPS_THROW))
        grab_knee_dur = max(1, int(FPS / ANIM_FPS_THROW))
        hit_dur = max(1, int(FPS / ANIM_FPS_HIT))
        dead_dur = max(1, int(FPS / ANIM_FPS_DEAD))

        # make duration exact
        self.attack_duration = len(attack_frames) * attack_dur
        self.run_attack_duration = len(run_attack_frames) * run_attack_dur
        self.jump_attack_duration = len(jump_attack_frames) * jump_attack_dur
        self.throw_duration = len(throw_frames) * throw_dur
        self.grab_knee_duration = len(throw_frames) * throw_dur

        self.animation_manager.add_animation(
            self.IDLE, PlayerFrameAnimation(idle_frames, idle_dur))
        self.animation_manager.add_animation(
            self.WALK, PlayerFrameAnimation(walk_frames, walk_dur))
        self.animation_manager.add_animation(
            self.RUN, PlayerFrameAnimation(run_frames, run_dur))
        self.animation_manager.add_animation(
            self.JUMP, PlayerFrameAnimation(jump_frames, jump_dur))
        self.animation_manager.add_animation(
            self.ATTACK, PlayerFrameAnimation(attack_frames, attack_dur))
        self.animation_manager.add_animation(
            self.RUN_ATTACK, PlayerFrameAnimation(run_attack_frames, run_attack_dur))
        self.animation_manager.add_animation(
            self.JUMP_ATTACK, PlayerFrameAnimation(jump_attack_frames, jump_attack_dur))
        self.animation_manager.add_animation(
            self.GRAB, PlayerFrameAnimation(grab_frames, grab_dur))
        self.animation_manager.add_animation(
            self.THROW, PlayerFrameAnimation(throw_frames, throw_dur))
        self.animation_manager.add_animation(
            self.GRAB_KNEE, PlayerFrameAnimation(grab_knee_frames, grab_knee_dur))
        self.animation_manager.add_animation(
            self.HIT, PlayerFrameAnimation(hit_frames, hit_dur))
        self.animation_manager.add_animation(
            self.DEAD, PlayerFrameAnimation(dead_frames, dead_dur))

    def get_current_animation_frame_index(self):
        animation = self.animation_manager.current_animation
        if hasattr(animation, "get_frame_index"):
            return animation.get_frame_index()
        return 0

    # update() works in world coordinates
    # draw() translates to screen coordinates using camera_x
    def update(self):
        if self.state == self.DEAD:
            self.update_dead_state()
            return

        self.update_timers()
        keys = pygame.key.get_pressed()
        moving = self.update_movement(keys)
        self.update_action_input(keys)
        self.update_jump_physics(keys)
        self.update_state_after_movement(moving)
        self.update_grabbed_enemy_position()
        #self.apply_world_bounds() # moved to gameplay_system.py
        self.update_animation()

    #World:   [--------------------PLAYER----]
    #                          x=800
    #Screen window starts at camera_x=600:
    #	      [    window    ]
    #	       600          1200
    #Player appears at pixel 200 inside the window → screen_x = 200
    def draw(self, screen, camera_x):
        # camera_x is how far the camera has scrolled.
        # Subtracting it converts the player's world position->screen position
        # player's screen x position after camera offset
        # bottom-center screen x:
        screen_x = self.x - camera_x
        body_left = self.get_left()
        screen_left = body_left - camera_x

        # add depth
        # Now moving up/down looks more like a beat'em-up character walking in depth.
        # shadow_rect = pygame.Rect(screen_x,self.y + self.height - 10,self.width,12)
        #pygame.draw.ellipse(screen,(50, 50, 50),shadow_rect)
        # end of depth

        image = self.animation_manager.get_image()
        scale = self.sprite_scale
        image = pygame.transform.scale(image, (image.get_width()*scale, image.get_height()*scale))
        if not self.facing_right:
            image = pygame.transform.flip(image, True, False)
        
        frame = self.get_current_player_frame()
        #if frame: # for new frame system
        offset_x, offset_y = frame.offset
        offset_x *= scale
        offset_y *= scale
        if self.facing_right:
            sprite_world_x = self.x + offset_x
        else:
            sprite_world_x = self.x - image.get_width() - offset_x
        sprite_y = self.y + offset_y
        screen.blit(image, (sprite_world_x - camera_x, sprite_y))
        #else:
            # Sprite frames can be wider/taller than the gameplay body box.
            # Keep the feet and body anchored to the player's collision rectangle.
        #    sprite_x = screen_left
        #    if not self.facing_right:
        #        sprite_x -= max(0, image.get_width() - self.width)
        #    sprite_y = self.y - image.get_height()
        #    screen.blit(image, (sprite_x, sprite_y))

        # weapon section
        if self.weapon:
            weapon_len = 20
            if not self.weapon.is_ranged:
                weapon_len += self.weapon.hitbox_w_bonus
            weapon_x = screen_x + self.width
            if not self.facing_right:
                weapon_x = screen_x - weapon_len
            
            pygame.draw.rect(screen, (255,255,0),
                (weapon_x, self.y+30,weapon_len,5))

        screen_x = self.x - camera_x

        # green = logical body
        # red = hurt box
        # blue = collision box
        # yellow = attack hitbox
        # debug: draw player's bounding box (world -> screen)
        if SHOW_PLAYER_RECT:
            body_rect = self.get_logical_rect()
            hurt_rect = self.get_hurt_rect()
            collision_rect = self.get_collision_rect()
            attack_rect = self.get_attack_rect()

            pygame.draw.rect(screen,GREEN_COLOR,
                (body_rect.x - camera_x, body_rect.y,
                body_rect.width, body_rect.height), 1)
            pygame.draw.rect(screen,(255, 80, 80),
                (hurt_rect.x - camera_x, hurt_rect.y,
                hurt_rect.width, hurt_rect.height), 1)
            pygame.draw.rect(screen, (80, 180, 255),
                (collision_rect.x - camera_x, collision_rect.y,
                collision_rect.width, collision_rect.height), 1)

            if attack_rect:
                pygame.draw.rect(screen, YELLOW_COLOR,
                    (attack_rect.x - camera_x, attack_rect.y,
                    attack_rect.width, attack_rect.height), 1)

        # player health bar (above player)
        hb_x = screen_left
        hb_y = self.get_top() - 16
        hb_w = self.width
        hb_h = 8
        # background
        pygame.draw.rect(screen, (100, 100, 100), (hb_x, hb_y, hb_w, hb_h))
        # filled portion (clamped between 0 and 1)
        fill_ratio = 0
        try:
            fill_ratio = max(0.0, min(1.0, float(self.hp) / float(self.max_hp)))
        except Exception:
            fill_ratio = 0
        hp_w = int(hb_w * fill_ratio)
        pygame.draw.rect(screen, (0, 255, 0), (hb_x, hb_y, hp_w, hb_h))

    def get_left(self):
        return int(self.x - self.width / 2)

    def get_top(self):
        return self.y - self.height
    
    def get_right(self):
        return int(self.x + self.width / 2)
    
    def get_bottom(self):
        return self.y

    def get_logical_rect(self):
        return pygame.Rect(
            self.get_left(),self.get_top(),
            self.width,self.height)

    def get_hurt_rect(self):
        scale = self.sprite_scale
        frame = self.get_current_player_frame()
        # new for frame-aware logic
        local_x, local_y, w, h = frame.hurt_rect
        offset_x, offset_y = frame.offset
        frame_w = frame.image.get_width()

        # scale
        local_x *= scale
        local_y *= scale
        w *= scale
        h *= scale
        offset_x *= scale
        offset_y *= scale
        frame_w *= scale
        if self.facing_right:
            world_x = self.x + offset_x + local_x
        else:
            mirrored_x = frame_w - local_x - w
            world_x = self.x - frame_w - offset_x + mirrored_x

        world_y = self.y + offset_y + local_y
        return pygame.Rect(int(world_x), int(world_y), int(w), int(h))

        # fallback to old logic
        #return pygame.Rect(
        #    int(self.get_left() + self.hurtbox_offset_x),
        #    int(self.get_top() + self.hurtbox_offset_y),
        #    int(self.hurtbox_w),
        #    int(self.hurtbox_h))

    # on bottom center
    def get_collision_rect(self):
        return pygame.Rect(
            int(self.x - self.collision_box_w/2),
            int(self.y - self.collision_box_h),
            int(self.collision_box_w),
            int(self.collision_box_h)
        )

    # hit box
    def get_attack_rect(self):
        if not self.is_attacking:
            return None
        
        # for new per-frame logic
        frame = self.get_current_player_frame()
        if frame and frame.attack_rect:
            local_x, local_y, w, h = frame.attack_rect
            offset_x, offset_y = frame.offset
            frame_w = frame.image.get_width()

            if self.facing_right:
                world_x = self.x + offset_x + local_x
            else:
                mirrored_x = frame_w - local_x - w
                world_x = self.x - frame_w - offset_x + mirrored_x

            world_y = self.y + offset_y + local_y
            return pygame.Rect(int(world_x), int(world_y), int(w), int(h))

        # fallback for old logic
        body_left = self.get_left()
        body_top = self.get_top()

        # OLD LOGIC
        # Use symmetric hitbox size and offsets so left/right behave identically
        #hit_w = self.attack_hitbox_w
        # giving running attack a longer hitbox
        #if self.state == self.RUN_ATTACK:
        #    hit_w = self.attack_hitbox_w * 1.5
        #if self.state == self.JUMP_ATTACK:
        #    hit_w = self.attack_hitbox_w
        #if self.state == self.GRAB_KNEE:
        #    hit_w = PLAYER_GRAB_KNEE_HITBOX_W
        #    hit_h = PLAYER_GRAB_KNEE_HITBOX_H
        #    hit_y = int(self.get_top() + self.height*0.35)
        #    # tune this hardcode 0.35 and 0.15 later
        #    if self.facing_right:
        #        hit_x = int(self.x + self.width*0.15)
        #    else:
        #        hit_x = int(self.x - hit_w - self.width*0.15)

        #    return pygame.Rect(hit_x, hit_y, hit_w, hit_h)

        #hit_h = self.attack_hitbox_h
        #if self.weapon and not self.weapon.is_ranged:
        #    hit_w += self.weapon.hitbox_w_bonus
        #    hit_h += self.weapon.hitbox_h_bonus

        #hit_y = body_top + self.attack_hitbox_offset_y
        #if self.facing_right:
        #    hit_x = int(self.x + self.width/2)
        #else:
        #    hit_x = int(self.x - self.width/2 - hit_w)
        #return pygame.Rect(hit_x, hit_y, hit_w, hit_h)

    def update_animation(self):
        if self.state == self.IDLE:
            self.animation_manager.play(self.IDLE)
        elif self.state == self.WALK:
            self.animation_manager.play(self.WALK)
        elif self.state == self.RUN:
            self.animation_manager.play(self.RUN)
        elif self.state == self.JUMP:
            self.animation_manager.play(self.JUMP)

        elif self.state in [self.ATTACK_1, self.ATTACK_2, self.ATTACK_3]:
            self.animation_manager.play(self.ATTACK)
        elif self.state == self.RUN_ATTACK:
            self.animation_manager.play(self.RUN_ATTACK)
        elif self.state == self.JUMP_ATTACK:
            self.animation_manager.play(self.JUMP_ATTACK)
        elif self.state == self.GRAB:
            self.animation_manager.play(self.GRAB)
        elif self.state == self.GRAB_KNEE:
            self.animation_manager.play(self.GRAB_KNEE)
        elif self.state == self.THROW:
            self.animation_manager.play(self.THROW)

        elif self.state == self.HIT: # Take hit by enemy
            self.animation_manager.play(self.HIT)
        elif self.state == self.DEAD:
            self.animation_manager.play(self.DEAD)
        else:
            self.animation_manager.play(self.IDLE)

        self.animation_manager.update()

    def update_dead_state(self):
        self.update_respawn()
        self.update_animation()

    def update_timers(self):
        # TODO: hit timer? hit by enemy or attack enemy?
        if self.hit_timer > 0:
            self.hit_timer -= 1
            if self.hit_timer == 0:
                self.state = self.IDLE

        if self.combo_timer > 0:
            self.combo_timer -= 1
        else:
            self.combo_step = 0

        if self.throw_timer > 0:
            self.throw_timer -= 1

        if self.run_tap_timer > 0:
            self.run_tap_timer -= 1
            
        if self.grab_knee_timer > 0:
            self.grab_knee_timer -= 1
            if self.grab_knee_timer <= 0:
                self.is_attacking = False
                self.already_hit_enemy = False
                if self.grabbed_enemy:
                    self.state = self.GRAB
                else:
                    self.state = self.IDLE

        # attack timer
        if self.is_attacking:
            self.attack_timer -= 1
            if self.attack_timer <= 0:
                self.is_attacking = False
                if self.state != self.DEAD:
                    self.state = self.IDLE
            # comment out, so still can move during attacking
            #return # skip movement while attacking

    def update_movement(self, keys):
        moving = False
        if self.is_jumping: # avoid double movement while jumping
            return False

        left_down = keys[pygame.K_LEFT] or keys[pygame.K_a]
        right_down = keys[pygame.K_RIGHT] or keys[pygame.K_d]
        up_down = keys[pygame.K_UP] or keys[pygame.K_w]
        down_down = keys[pygame.K_DOWN] or keys[pygame.K_s]
        shift_down = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]

        horizontal_direction = 0
        if left_down and not right_down:
            horizontal_direction = -1
        elif right_down and not left_down:
            horizontal_direction = 1

        self.update_run_input(left_down, right_down, horizontal_direction)
        self.is_running = horizontal_direction != 0 and (
            shift_down or self.run_active)

        move_speed = self.run_speed if self.is_running else self.speed

        if left_down:
            self.x -= move_speed
            self.facing_right = False
            moving = True
        if right_down:
            self.x += move_speed
            self.facing_right = True
            moving = True
        if up_down:
            self.y -= self.speed
            moving = True
        if down_down:
            self.y += self.speed
            moving = True

        return moving

    def update_run_input(self, left_down, right_down, horizontal_direction):
        if horizontal_direction == 0:
            self.run_active = False
            self.left_pressed = left_down
            self.right_pressed = right_down
            return

        left_just_pressed = left_down and not self.left_pressed
        right_just_pressed = right_down and not self.right_pressed

        if left_just_pressed:
            self.check_run_double_tap(-1)
        elif right_just_pressed:
            self.check_run_double_tap(1)

        if self.run_active and self.run_direction != horizontal_direction:
            self.run_active = False

        self.left_pressed = left_down
        self.right_pressed = right_down

    def check_run_double_tap(self, direction):
        if self.run_direction == direction and self.run_tap_timer > 0:
            self.run_active = True

        self.run_direction = direction
        self.run_tap_timer = self.run_tap_window

    def update_jump_physics(self, keys):
        if not self.is_jumping:
            return
        
        # allow small air control
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vx = -self.air_speed
            self.facing_right = False
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vx = self.air_speed
            self.facing_right = True
            
        self.x += self.vx
        self.y += self.vy
        self.vx *= self.air_friction
        self.vy += self.gravity

        if self.y >= self.ground_y:
            self.y = self.ground_y
            self.vx = 0
            self.vy = 0
            self.is_jumping = False
            self.jump_attack_pressed = False
            
            if self.state in [self.JUMP, self.JUMP_ATTACK]:
                self.state = self.IDLE

    def update_action_input(self, keys):
        # jump key
        if keys[pygame.K_SPACE]:
            if not self.jump_pressed:
                self.start_jump(keys)
                self.jump_pressed = True
        else:
            self.jump_pressed = False

        # attacking keys
        if keys[pygame.K_j]:
            if self.is_jumping:
                if not self.jump_attack_pressed:
                    self.start_jump_attack()
                    self.jump_attack_pressed = True
            else:
                if self.grabbed_enemy:
                    self.start_grab_knee_attack()
                else:
                    self.start_attack()
        else:
            self.jump_attack_pressed = False

        # fire weapon on key-down only (prevent holding K from firing repeatedly)
        if keys[pygame.K_k]:
            if not self.fire_pressed:
                self.fire_weapon()
                self.fire_pressed = True
        else:
            self.fire_pressed = False

    def update_state_after_movement(self, moving):
        # update state (preserve attack state if attacking)
        if self.is_attacking:
            return
            #pass # keep attack state and animation set by start_attack
        if self.is_jumping:
            if self.state != self.JUMP_ATTACK:
                self.state = self.JUMP
            return

        elif self.throw_timer > 0:
            self.state = self.THROW
        elif self.grab_knee_timer > 0:
            self.state = self.GRAB_KNEE
        elif self.grabbed_enemy:
            self.state = self.GRAB
        else:
            if moving and self.is_running:
                self.state = self.RUN
            elif moving:
                    self.state = self.WALK
            else:
                self.state = self.IDLE

    def update_grabbed_enemy_position(self):
        # keep grabbed enemy in front of player
        if self.grabbed_enemy:
            grab_offset = (self.width + self.grabbed_enemy.width) / 2 + 5
            if self.facing_right:
                self.grabbed_enemy.x = self.x + grab_offset
            else:
                self.grabbed_enemy.x = self.x - grab_offset
            self.grabbed_enemy.y = self.y

    def apply_world_bounds(self, world_width=None, lane_top=None, lane_bottom=None):
        if world_width is None:
            world_width = WORLD_WIDTH
        if lane_top is None:
            lane_top = self.lane_top
        if lane_bottom is None:
            lane_bottom = self.lane_bottom

        # world boundaries
        half_w = int(self.width / 2)
        self.x = max(half_w, self.x) # cannot go left of window
        self.x = min(self.x, world_width - half_w) # cannot go right window
        # beat'em up lane limitsL creates the illusion of depth
        # player walks on a horizontal strip, not full screen
        self.y = max(lane_top, self.y) # cannot go above lane_top
        self.y = min(lane_bottom, self.y) # cannot go below lane_bottom

    #######################

    def start_jump(self, keys):
        if self.is_jumping:
            return
        if self.is_attacking:
            return
        if self.grabbed_enemy:
            return
        self.is_jumping = True
        self.ground_y = self.y
        self.vy = self.jump_power
        self.vx = 0
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vx = -self.air_speed
            self.facing_right = False
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vx = self.air_speed
            self.facing_right = True

        self.state = self.JUMP

    def start_jump_attack(self):
        if not self.is_jumping:
            return
        if self.is_attacking:
            return
        self.is_attacking = True
        self.attack_timer = self.jump_attack_duration
        self.already_hit_enemy = False
        self.state = self.JUMP_ATTACK
    
    def start_attack(self):
        # The current start_attack() prevents attack chaining while an attack is active:
        # we'll replace this with an input buffer system
        if self.is_attacking:
            return

        # for default walking attack
        self.is_attacking = True
        self.attack_timer = self.attack_duration
        self.already_hit_enemy = False

        # for running attack
        if self.is_running:
            self.attack_timer = self.run_attack_duration
            self.combo_timer = 0
            self.combo_step = 0
            self.state = self.RUN_ATTACK
            return

        if self.combo_timer > 0:
            self.combo_step += 1
        else:
            self.combo_step = 1
        
        self.combo_step = min(self.combo_step, 3)
        self.combo_timer = 30 # time window to continue the combo
        # state
        if self.combo_step == 1:
            self.state = self.ATTACK_1
        elif self.combo_step == 2:
            self.state = self.ATTACK_2
        else:
            self.state = self.ATTACK_3

    def start_grab_knee_attack(self):
        if not self.grabbed_enemy:
            return
        if self.is_attacking:
            return
        self.is_attacking = True
        self.attack_timer = self.grab_knee_duration
        self.grab_knee_timer = self.grab_knee_duration
        self.already_hit_enemy = False
        self.state = self.GRAB_KNEE

    def attack_damage(self):
        base_damage = FIST_DAMAGE
        if self.state == self.ATTACK_1:
            base_damage = FIST_DAMAGE
        elif self.state == self.ATTACK_2:
            base_damage = FIST_DAMAGE + 4
        elif self.state == self.ATTACK_3:
            base_damage = FIST_DAMAGE + 8
        elif self.state == self.RUN_ATTACK:
            base_damage = FIST_DAMAGE + 6
        elif self.state == self.JUMP_ATTACK:
            base_damage = FIST_DAMAGE + 6
        elif self.state == self.GRAB_KNEE:
            base_damage = PLAYER_GRAB_KNEE_DAMAGE

        if self.weapon and not self.weapon.is_ranged:
            base_damage += self.weapon.damage

        return base_damage

    def take_damage(self, damage):
        if self.state == self.DEAD:
            return

        try:
            damage = float(damage)
        except (TypeError, ValueError):
            return

        self.hp -= damage
        self.state = self.HIT
        self.hit_timer = 20

        if self.hp <= 0:
            self.hp = 0
            self.lost_life()
            #self.state = self.DEAD

    def lost_life(self):
        self.lives -= 1
        if self.lives <= 0:
            self.state = self.DEAD
            return
        self.state = self.DEAD
        self.respawn_timer = 90
        
    def update_respawn(self):
        if self.state != self.DEAD:
            return
        if self.lives <= 0:
            return
        if self.respawn_timer > 0:
            self.respawn_timer -= 1
        if self.respawn_timer <= 0:
            self.respawn()
            
    def respawn(self):
        self.hp = self.max_hp
        self.x = self.respawn_x
        self.y = self.respawn_y
        self.ground_y = self.respawn_y
        self.vx = 0
        self.vy = 0
        self.is_jumping = False
        self.state = self.IDLE
        self.is_attacking = False
        self.grabbed_enemy = None

    def pick_up_weapon(self, weapon):
        self.weapon = weapon
        weapon.picked_up = True

    def drop_weapon(self):
        if self.weapon is None:
            return

        self.weapon.picked_up = False
        self.weapon.x = self.x - 80
        self.weapon.y = self.y + 80
        self.weapon = None

    def fire_weapon(self):
        if self.weapon is None:
            return
        if not self.weapon.is_ranged:
            return
        if self.weapon.ammo <= 0:
            return

        direction = 1
        if not self.facing_right:
            direction = -1
        
        muzzle_x = self.x + (40 if self.facing_right else -40)
        muzzle_y = self.get_top() + 105
        projectile = Projectile(muzzle_x, muzzle_y, direction, PROJECTILE_SPEED, self.weapon.damage)
        self.pending_projectile = projectile
        self.weapon.ammo -= 1
        
    def can_grab_enemy(self, enemy):
        if enemy.state == enemy.DEAD:
            return False
        if enemy.state == enemy.GRABBED:
            return False
        
        dx = abs(enemy.x - self.x)
        dy = abs(enemy.y - self.y)
        return dx <= self.grab_range and dy <= 40
    
    def grab_enemy(self, enemy):
        self.grabbed_enemy = enemy
        enemy.grabbed_by_player()
        self.state = self.GRAB
        
    def throw_grabbed_enemy(self):
        if self.grabbed_enemy is None:
            return
        
        direction = 1
        if not self.facing_right:
            direction = -1
        self.grabbed_enemy.thrown_by_player(direction)
        
        self.grabbed_enemy = None
        self.throw_timer = self.throw_duration
        self.state = self.THROW
