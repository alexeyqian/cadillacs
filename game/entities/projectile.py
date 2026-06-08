import pygame
from game.settings import *
from game.colors import *
class Projectile:
    def __init__(self, x, y, direction, speed, damage):
        self.x = x
        self.y = y
        self.width = 12
        self.height = 4
        self.direction = direction
        self.speed = speed
        self.damage = damage
        self.active = True

    def update(self):
        self.x += self.speed * self.direction
        if self.x < -100:
            self.active = False
        if self.x > WORLD_WIDTH:
            self.active = False

    def draw(self, screen, camera_x):
        screen_x = self.x - camera_x
        pygame.draw.rect(screen, YELLOW_COLOR,
                (screen_x, self.y, self.width, self.height))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

