import pygame
from game.settings import *
from game.colors import *

class EnemyProjectile:
    def __init__(self, x, y, direction, speed, damage):
        # x, y means center of the object rect
        self.x = x
        self.y = y
        self.width = 16
        self.height = 16
        self.direction = direction
        self.speed = speed
        self.damage = damage

        self.active = True

    def update(self, world_width=WORLD_WIDTH):
        self.x += self.speed * self.direction
        if self.x <= -100:
            self.active = False
        if self.x > world_width:
            self.active = False

    def draw(self, screen, camera_x):
        pygame.draw.circle(screen, YELLOW_COLOR,
            (int(self.x-camera_x), int(self.y)), 8)

    def get_rect(self):
        return pygame.Rect(
            self.x-self.width//2, self.y-self.height//2, 
            self.width, self.height)

