import pygame

class Projectile:
    def __init__(self, x, y, direction, damage):
        self.x = x
        self.y = y
        self.direction = direction
        self.damage = damage
        self.speed = 10
        self.width = 12
        self.height = 4
        self.active = True

    def update(self):
        self.x += self.speed * self.direction
        if self.x < -100:
            self.active = False
        if self.x > 5000:
            self.active = False

    def draw(self, screen, camera_x):
        screen_x = self.x - camera_x
        pygame.draw.rect(screen, (255,255,0),
                (screen_x, self.y, self.width, self.height))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

