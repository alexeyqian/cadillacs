import pygame
from game.animation.animation import Animation
from game.animation.animation_manager import AnimationManager
from game.animation.asset_loader import AssetLoader
from game.animation.animation_config import *
from game.animation.file_utils import *
from game.assets.placeholder.player_frames import *
from game.settings import *
from game.entities.projectile import Projectile

# Player has: movement, animation, combat, inventory
# pickup/drop weapons should belong to inventory system
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
    GRAB = "GRAB"
    THROW = "THROW"

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
        
        # grab/throw
        self.grabbed_enemy = None
        self.grab_pressed = False
        self.grab_range = 70
        self.throw_timer = 0
        self.throw_duration = 14

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
                PLAYER_WALK["file"],
                PLAYER_WALK["frame_width"],
                PLAYER_WALK["frame_height"],
                PLAYER_WALK["frame_count"]
            )
        else:
            walk_frames = create_walk_frames()
            
        if file_exists(PLAYER_ATTACK["file"]):
            attack_frames = AssetLoader.load_animation(
                PLAYER_ATTACK["file"],
                PLAYER_ATTACK["frame_width"],
                PLAYER_ATTACK["frame_height"],
                PLAYER_ATTACK["frame_count"]
            )
        else:
            attack_frames = create_attack_frames()

        if file_exists(PLAYER_GRAB["file"]):
            grab_frames = AssetLoader.load_animation(
                PLAYER_GRAB["file"],
                PLAYER_GRAB["frame_width"],
                PLAYER_GRAB["frame_height"],
                PLAYER_GRAB["frame_count"]
            )
        else:
            grab_frames = attack_frames

        if file_exists(PLAYER_THROW["file"]):
            throw_frames = AssetLoader.load_animation(
                PLAYER_THROW["file"],
                PLAYER_THROW["frame_width"],
                PLAYER_THROW["frame_height"],
                PLAYER_THROW["frame_count"]
            )
        else:
            throw_frames = attack_frames

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
            self.GRAB, Animation(grab_frames, attack_dur)
        )
        self.animation_manager.add_animation(
            self.THROW, Animation(throw_frames, attack_dur)
        )
        self.animation_manager.add_animation(
            self.HIT, Animation(create_hit_frames(), hit_dur)
        )
        self.animation_manager.add_animation(
            self.DEAD, Animation(create_dead_frames(), 999)
        )


    # update() works in world coordinates
    # draw() translates to screen coordinates using camera_x
    # responsible for: Movement,Animation, State transitions, 
    # Attack state, Hit state, Death state
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

        if self.throw_timer > 0:
            self.throw_timer -= 1

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

        # update state (preserve attack state if attacking)
        if self.is_attacking:
            # keep attack state and animation set by start_attack
            pass
        elif self.throw_timer > 0:
            self.state = self.THROW
        elif self.grabbed_enemy:
            self.state = self.GRAB
        else:
            if moving:
                self.state = self.WALK
                #self.current_animation = self.animations[self.WALK]
            else:
                self.state = self.IDLE
                #self.current_animation = self.animations[self.IDLE]
                
        # keep grabbed enemy in front of player
        if self.grabbed_enemy:
            if self.facing_right:
                self.grabbed_enemy.x = self.x + self.width + 5
            else:
                self.grabbed_enemy.x = self.x - self.grabbed_enemy.width - 5
            
            self.grabbed_enemy.y = self.y

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
        # player's screen x position after camera offset
        screen_x = self.x - camera_x

        # add depth
        # Now moving up/down looks more like a beat'em-up character walking in depth.
        # shadow_rect = pygame.Rect(screen_x,self.y + self.height - 10,self.width,12)
        #pygame.draw.ellipse(screen,(50, 50, 50),shadow_rect)
        # end of depth

        image = self.animation_manager.get_image()
        if not self.facing_right:
            image = pygame.transform.flip(image, True, False)
        # Real sprites are often larger than gameplay hit boxes.
        image = pygame.transform.scale(image, (self.width, self.height))
        screen.blit(image, (screen_x, self.y))

        # weapon section
        if self.weapon:
            weapon_len = 20
            if not self.weapon.is_ranged:
                weapon_len += self.weapon.attack_range_bonus
            weapon_x = screen_x + self.width
            if not self.facing_right:
                weapon_x = screen_x - weapon_len
            
            pygame.draw.rect(screen, (255,255,0),
                (weapon_x, self.y+30,weapon_len,5))

        screen_x = self.x - camera_x

        # debug: draw player's bounding box (world -> screen)
        if SHOW_PLAYER_RECT:
            pygame.draw.rect(screen, (0, 255, 255), (screen_x, self.y, self.width, self.height), 1)

        # attack hitbox debug
        if SHOW_PLAYER_HITBOX:
            attack_rect = self.get_attack_rect()
            if attack_rect:
                pygame.draw.rect(screen, (255, 255, 0),
                    (attack_rect.x - camera_x, attack_rect.y,
                    attack_rect.width, attack_rect.height), 1)

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
        elif self.state == self.GRAB:
            self.animation_manager.play(self.GRAB)
        elif self.state == self.THROW:
            self.animation_manager.play(self.THROW)
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

        if self.weapon and not self.weapon.is_ranged:
            base_damage += self.weapon.damage

        return base_damage

    # hit box
    def get_attack_rect(self): # hitbox
        if not self.is_attacking:
            return None
        # Use symmetric hitbox size and offsets so left/right behave identically
        hit_w = self.attack_hitbox_w
        hit_h = self.attack_hitbox_h
        if self.weapon and not self.weapon.is_ranged:
            hit_w += self.weapon.attack_range_bonus
            hit_h += self.weapon.attack_height_bonus

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
        if not self.weapon.is_ranged:
            return
        if self.weapon.ammo <= 0:
            return

        direction = 1
        if not self.facing_right:
            direction = -1
        projectile = Projectile(self.x+40, self.y+30, direction, self.weapon.damage)
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
