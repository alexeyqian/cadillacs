import pygame

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 80
        self.speed = 2
        self.hp = 100
        self.state = "CHASE"

        self.knockback_velocity = 0
        # enemy gets briefly white when hit
        self.hit_timer = 0

    def update(self, player):
        dx = player.x - self.x
        dy = player.y - self.y

        distance_x = abs(dx)
        
        if distance_x > 80:
            self.state = "CHASE"
        else:
            self.state = "ATTACK"

        # stop near player
        if distance_x > 60:
            if dx > 0:
                self.x += self.speed
            elif dx < 0:
                self.x -= self.speed
        
        #follow depth lane
        if abs(dy)>10:
            if dy > 0:
                self.y += self.speed
            elif dy < 0:
                self.y -= self.speed

        # knock back settings
        if self.knockback_velocity != 0:
            self.x += self.knockback_velocity
            self.knockback_velocity *= 0.8
            if abs(self.knockback_velocity) < 0.5:
                self.knockback_velocity = 0

        if self.hit_timer:
            self.hit_timer -= 1

    def draw(self, screen, camera_x):
        screen_x = self.x - camera_x
        # shadow
        pygame.draw.ellipse(
            screen, (50, 50, 50),
            (
                screen_x,
                self.y + self.height - 10,
                self.width,
                12
            )
        )
        # body
        body_color = (220, 40, 220)
        if self.hit_timer > 0:
            body_color = (255, 255, 255)
        elif self.state == "CHASE":
            body_color = (40, 40, 220)

        pygame.draw.rect(
            screen, body_color,
            (
                screen_x,
                self.y,
                self.width,
                self.height
            )
        )
        
        # health bar background
        pygame.draw.rect(
            screen, (120, 120, 120),
            (
                screen_x,
                self.y - 12,
                50,
                6
            )
        )
        # health bar
        hp_width = int(50 * (self.hp / 100))
        pygame.draw.rect(
            screen, (255, 0, 0),
            (
                screen_x,
                self.y - 12,
                hp_width,
                6
            )
        )

    def take_damage(self, damage, attacker_x):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0

        if attacker_x < self.x:
            self.knockback_velocity = 8
        else:
            self.knockback_velocity = -8

        self.hit_timer = 10


