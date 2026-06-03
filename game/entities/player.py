#from turtle import Screen

import pygame
from game.animation.animation import Animation
from game.animation.animation_manager import AnimationManager
from game.animation.asset_loader import AssetLoader
from game.animation.animation_config import *
from game.animation.file_utils import *
from game.assets.placeholder.player_frames import *
from game.settings import *
from game.entities.projectile import Projectile

class Player:
    IDLE = "IDLE"
    WALK = "WALK"
    ATTACK = "ATTACK" # including 1,2,3
    # punch combo
    ATTACK_1 = "ATTACK_1"
    ATTACK_2 = "ATTACK_2"
    ATTACK_3 = "ATTACK_3"
    HIT = "HIT" # hit by enemies
    DEAD = "DEAD"

    def __init__(self):
        self.x = 200
        self.y = 350
        self.width = 50
        self.height = 80
        self.speed = 5
        self.facing_right = True

        self.is_attacking = False
        self.attack_timer = 0
        self.attack_duration = 12
        self.already_hit_enemy = False # already_hit

        # classic combo system
        # J punch 1, J punch 2, J punch 3
        self.combo_step = 0
        self.combo_timer = 0

        self.state = self.IDLE
        self.max_hp = 100
        self.hp = 100
        self.hit_timer = 0 # hit by enemy

        self.weapon = None
        self.pending_projectile = None
        self.fire_pressed = False  # track K_k edge for single-shot firing
        self.drop_pressed = False  # track K_q edge for single-press drop

        # attack hitbox settings (kept symmetric for left/right)
        self.attack_hitbox_w = PLAYER_HITBOX_W
        self.attack_hitbox_h = 60
        self.attack_hitbox_offset_y = 10
        
        # lane boundaries
        self.lane_top = LANE_TOP
        self.lane_bottom = LANE_BOTTOM
        
        # load frames
        if file_exists(PLAYER_IDLE["file"]):
            idle_frames = AssetLoader.load_animation(
                PLAYER_IDLE["file"],
                PLAYER_IDLE["frame_width"],
                PLAYER_IDLE["frame_height"],
                PLAYER_IDLE["frame_count"]
            )
        else:
            idle_frames = create_idle_frames()

        if file_exists(PLAYER_WALK["file"]):
            walk_frames = AssetLoader.load_animation(
                PLAYER_IDLE["file"],
                PLAYER_IDLE["frame_width"],
                PLAYER_IDLE["frame_height"],
                PLAYER_IDLE["frame_count"]
            )
        else:
            walk_frames = create_walk_frames()
            
        if file_exists(PLAYER_ATTACK["file"]):
            attack_frames = AssetLoader.load_animation(
                PLAYER_IDLE["file"],
                PLAYER_IDLE["frame_width"],
                PLAYER_IDLE["frame_height"],
                PLAYER_IDLE["frame_count"]
            )
        else:
            attack_frames = create_attack_frames()

        # animation manager
        self.animation_manager = AnimationManager()
        # compute frame durations (number of game frames each animation frame should last)
        idle_dur = max(1, int(FPS / ANIM_FPS_IDLE))
        walk_dur = max(1, int(FPS / ANIM_FPS_WALK))
        attack_dur = max(1, int(FPS / ANIM_FPS_ATTACK))
        hit_dur = max(1, int(FPS / ANIM_FPS_HIT))

        self.animation_manager.add_animation(
            self.IDLE, Animation(idle_frames, idle_dur))
        self.animation_manager.add_animation(
            self.WALK, Animation(walk_frames, walk_dur))
        self.animation_manager.add_animation(
            self.ATTACK, Animation(attack_frames, attack_dur)
        )
        self.animation_manager.add_animation(
            self.HIT, Animation(create_hit_frames(), hit_dur)
        )
        self.animation_manager.add_animation(
            self.DEAD, Animation(create_dead_frames(), 999)
        )


    # update() works in world coordinates
    # draw() translateds to screen coordinates using camera_x
    def update(self):
        if self.state == self.DEAD:
            return

        if self.hit_timer > 0:
            self.hit_timer -= 1
            if self.hit_timer == 0:
                self.state = self.IDLE

        if self.combo_timer > 0:
            self.combo_timer -= 1
        else:
            self.combo_step = 0

        # attack timer
        if self.is_attacking:
            self.attack_timer -= 1
            if self.attack_timer <= 0:
                self.is_attacking = False
                if self.state != self.DEAD:
                    self.state = self.IDLE
            # comment out, so still can move during attacking
            #return # skip movement while attacking

        # movements
        keys = pygame.key.get_pressed()
        moving = False
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
            self.facing_right = False
            moving = True
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed
            self.facing_right = True
            moving = True
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= self.speed
            moving = True
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += self.speed
            moving = True

        if keys[pygame.K_j]:
            self.start_attack()

        # fire weapon on key-down only (prevent holding K from firing repeatedly)
        if keys[pygame.K_k]:
            if not self.fire_pressed:
                self.fire_weapon()
                self.fire_pressed = True
        else:
            self.fire_pressed = False

        # drop weapon on key-down only
        if keys[pygame.K_q]:
            if not self.drop_pressed:
                self.drop_weapon()
                self.drop_pressed = True
        else:
            self.drop_pressed = False

        # update state (preserve attack state if attacking)
        if self.is_attacking:
            # keep attack state and animation set by start_attack
            pass
        else:
            if moving:
                self.state = self.WALK
                #self.current_animation = self.animations[self.WALK]
            else:
                self.state = self.IDLE
                #self.current_animation = self.animations[self.IDLE]

        # world boundaries
        # cannot go left of 0
        self.x = max(0, self.x)
        # cannot go right of 2950
        self.x = min(self.x, 3000-self.width)
        # beat'em up lane limits
        # creates the illusion of depth
        # player walks on a horizontal strip, not full screen
        # cannot go above lane_top
        self.y = max(self.lane_top, self.y)
        # cannot go below lane_bottom
        self.y = min(self.lane_bottom, self.y)

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
        # playe's screen x position after camera offset
        screen_x = self.x - camera_x

        # add depth
        # Now moving up/down looks more like a beat'em-up character walking in depth.
        shadow_rect = pygame.Rect(
            screen_x,
            self.y + self.height - 10,
            self.width,
            12
        )

        pygame.draw.ellipse(
            screen,
            (50, 50, 50),
            shadow_rect
        )
        # end of depth

        image = self.animation_manager.get_image()
        if not self.facing_right:
            image = pygame.transform.flip(image, True, False)
        # Real sprites are often larger than gameplay hitboxes.
        image = pygame.transform.scale(image, (self.width, self.height))
        screen.blit(image, (screen_x, self.y))

        # hat: a simple visual on the player's head that points based on facing
        hat_w = int(self.width * 0.3)
        hat_h = max(6, int(self.height * 0.10))
        hat_x = screen_x + (self.width - hat_w) // 2
        hat_y = self.y #self.y - hat_h - 4
        # hat body
        pygame.draw.rect(screen, (180, 30, 30), (hat_x, hat_y, hat_w, hat_h))
        # brim (half-brim shown on side the player is facing)
        brim_w = hat_w + 8
        brim_x = hat_x - 4
        brim_y = hat_y + hat_h
        center_x = hat_x + hat_w // 2
        if self.facing_right:
            # show right half brim
            pygame.draw.rect(screen, (80, 40, 0), (center_x, brim_y, brim_x + brim_w - center_x, 3))
        else:
            # show left half brim
            pygame.draw.rect(screen, (80, 40, 0), (brim_x, brim_y, center_x - brim_x, 3))
        # tip pointing direction
        if self.facing_right:
            tip_pts = [
                (hat_x + hat_w, hat_y),
                (hat_x + hat_w + 10, hat_y + hat_h // 2),
                (hat_x + hat_w, hat_y + hat_h)
            ]
        else:
            tip_pts = [
                (hat_x, hat_y),
                (hat_x - 10, hat_y + hat_h // 2),
                (hat_x, hat_y + hat_h)
            ]
        pygame.draw.polygon(screen, (180, 30, 30), tip_pts)

        # weapon section
        if self.weapon:
            pygame.draw.rect(screen, (255,255,0),
                (screen_x+45, self.y+30,20,5))

        # debug: draw player's bounding box (world -> screen)
        screen_x = self.x - camera_x
        pygame.draw.rect(screen, (0, 255, 255), (screen_x, self.y, self.width, self.height), 2)

        # attack hitbox debug
        attack_rect = self.get_attack_rect()
        if attack_rect:
            pygame.draw.rect(screen, (255, 255, 0),
                (attack_rect.x - camera_x, attack_rect.y,
                 attack_rect.width, attack_rect.height), 2)

        # player health bar (above player)
        hb_x = screen_x
        hb_y = self.y - 16
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

    def update_animation(self):
        if self.state == self.DEAD:
            self.animation_manager.play(self.DEAD)
        elif self.state == self.HIT:
            self.animation_manager.play(self.HIT)
        elif self.state in [self.ATTACK_1, self.ATTACK_2, self.ATTACK_3]:
            self.animation_manager.play(self.ATTACK)
        elif self.state == self.WALK:
            self.animation_manager.play(self.WALK)
        else:
            self.animation_manager.play(self.IDLE)

        self.animation_manager.update()

    def start_attack(self):
        # The current start_attack() prevents attack chaining while an attack is active:
        # we'll replace this with an input buffer system
        if self.is_attacking:
            return

        self.is_attacking = True
        self.attack_timer = self.attack_duration
        self.already_hit_enemy = False

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

    def attack_damage(self):
        base_damage = 10
        if self.state == self.ATTACK_1:
            base_damage = 10
        elif self.state == self.ATTACK_2:
            base_damage = 15
        elif self.state == self.ATTACK_3:
            base_damage = 20

        if self.weapon:
            base_damage += self.weapon.damage

        return base_damage

    # hit box
    def get_attack_rect(self): # hitbox
        if not self.is_attacking:
            return None
        # Use symmetric hitbox size and offsets so left/right behave identically
        hit_w = self.attack_hitbox_w
        hit_h = self.attack_hitbox_h
        hit_y = int(self.y + self.attack_hitbox_offset_y)
        if self.facing_right:
            hit_x = int(self.x + self.width)
        else:
            hit_x = int(self.x - hit_w)
        return pygame.Rect(hit_x, hit_y, hit_w, hit_h)

    def take_damage(self, damage):
        if self.state == self.DEAD:
            return

        self.hp -= damage
        self.state = self.HIT
        self.hit_timer = 20

        if self.hp <= 0:
            self.hp = 0
            self.state = self.DEAD

    def pick_up_weapon(self, weapon):
        self.weapon = weapon
        weapon.picked_up = True


    def drop_weapon(self):
        if self.weapon is None:
            return

        self.weapon.picked_up = False
        self.weapon.x = self.x
        self.weapon.y = self.y + 30
        self.weapon = None

    def fire_weapon(self):
        if self.weapon is None:
            return
        if not self.weapon.is_range:
            return
        if self.weapon.ammo <= 0:
            return

        direction = 1
        if not self.facing_right:
            direction = -1
        projectile = Projectile(self.x+40, self.y+30, direction, self.weapon.damage)
        self.pending_projectile = projectile
        self.weapon.ammo -= 1
