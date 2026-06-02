#from turtle import Screen

import pygame
from game.animation.animation import Animation
from game.assets.placeholder.player_frames import *


class Player:
    IDLE = "IDLE"
    WALK = "WALK"
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
        
        frames = create_player_frames()
        self.animations = {
            self.IDLE: Animation(frames, frame_duration=20),
            self.WALK: Animation(frames, frame_duration=8),
            self.ATTACK_1: Animation(frames, frame_duration=4),
            #self.ATTACK_2: Animation(frames, frame_duration=4),
            #self.ATTACK_3: Animation(frames, frame_duration=4)
        }
        self.current_animation = self.animations[self.IDLE]

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
            return # skip movement while attacking

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
                
        # update state
        if moving:
            self.state = self.WALK
            self.current_animation = self.animations[self.WALK]
        else:
            self.state = self.IDLE
            self.current_animation = self.animations[self.IDLE]

        # world boundaries
        # cannot go left of 0
        self.x = max(0, self.x)
        # cannot go right of 2950
        self.x = min(self.x, 3000-self.width)
        # beat'em up lane limits
        # creates the illusion of depth
        # player walks on a horizontal strip, not full screen
        # cannot go above y=250
        self.y = max(250, self.y)
        # cannot go below y=450
        self.y = min(450, self.y)
        
        self.current_animation.update()


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

        image = self.current_animation.get_image()
        if not self.facing_right:
            image = pygame.transform.flip(image, True, False)
        screen.blit(image, (screen_x, self.y))
        
        #body_color = (180, 40,40) # default body color
        #if self.state == self.DEAD:
        #    body_color = (80, 80, 80)
        #elif self.state == self.HIT:
        #    body_color = (255, 255, 255)
        # add attacking visual feedback
        #elif self.state in [self.ATTACK_1, self.ATTACK_2, self.ATTACK_3]:
        #    body_color = (255, 180, 0)
        #elif self.state == self.WALK:
        #    body_color = (220, 40, 40)

        #pygame.draw.rect(screen, body_color,
        #    (screen_x, self.y, self.width,self.height))
        
        # attack hitbox debug
        attack_rect = self.get_attack_rect()
        if attack_rect:
            pygame.draw.rect(screen, (255, 255, 0),
                (attack_rect.x - camera_x, attack_rect.y, 
                 attack_rect.width, attack_rect.height), 2)

    def start_attack(self):
        # The current start_attack() prevents attack chaining while an attack is active:
        # we'll replace this with an input buffer system
        if self.is_attacking:
            return

        self.is_attacking = True
        self.current_animation = self.animations[self.ATTACK_1] # default to first attack animation
        self.current_animation.reset()
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
        if self.state == self.ATTACK_1:
            return 15
        elif self.state == self.ATTACK_2:
            return 20
        elif self.state == self.ATTACK_3:
            return 35

        return 0

    # hit box
    def get_attack_rect(self): # hitbox
        if not self.is_attacking:
            return None
        if self.facing_right:
            return pygame.Rect(
                self.x + self.width,
                self.y + 10,
                50, 40)
        else:
            return pygame.Rect(
                self.x - 50,
                self.y + 10,
                50, 40)

    def take_damage(self, damage):
        if self.state == self.DEAD:
            return

        self.hp -= damage
        self.state = self.HIT
        self.hit_timer = 20

        if self.hp <= 0:
            self.hp = 0
            self.state = self.DEAD

