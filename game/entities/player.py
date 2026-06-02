from turtle import Screen

import pygame

class Player:
    def __init__(self):
        self.x = 200
        self.y = 350
        self.width = 50
        self.height = 80
        self.speed = 5

        self.is_attacking = False
        self.attack_timer = 0
        self.attack_duration = 15
        self.already_hit = False
        self.facing_right = True

    # update() works in world coordinates
    # draw() translateds to screen coordinates using camera_x
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
            self.facing_right = False	
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
            self.facing_right = True
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed

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

        if keys[pygame.K_j]:
            if not self.is_attacking:
                self.start_attack()

        if self.is_attacking:
            self.attack_timer -= 1
            if self.attack_timer <= 0:
                self.is_attacking = False


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

        body_color = (220, 40,40)
        # add attacking visual feedback
        if self.is_attacking:
            body_color = (255, 180, 0)

        pygame.draw.rect(screen, body_color,
            (screen_x, self.y, self.width,self.height))
        
        # draw attack hitbox
        attack_rect = self.get_attack_rect()
        if attack_rect:
            pygame.draw.rect(screen, (255, 255, 0),
                (attack_rect.x - camera_x, attack_rect.y, 
                 attack_rect.width, attack_rect.height), 2)

    def start_attack(self):
        self.is_attacking = True
        self.attack_timer = self.attack_duration
        self.already_hit = False

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

