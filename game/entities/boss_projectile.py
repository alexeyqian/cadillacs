import pygame
from game.colors import *

class BossProjectile:
    def __init__(self, x, y, direction, speed, damage):
        self.x = x
        self.y = y
        self.direction = direction
        self.damage = damage
        self.speed = speed
        self.width = 30
        self.height = 15
        self.active = True
        self.lane_y = y

    def update(self, world_width):
        self.x += self.speed * self.direction
        if self.x < -200:
            self.active = False
        if self.x > world_width:
            self.active = False

    # center of rect, not bottom center
    def draw(self, screen, camera_x):
        screen_x = self.x - camera_x - self.width//2
        screen_y = self.y - self.height // 2

        pygame.draw.ellipse(
            screen, YELLOW_COLOR,
            (screen_x, screen_y, self.width, self.height))

        pygame.draw.ellipse(
            screen,WHITE_COLOR,
            (screen_x + 6, screen_y + 4, 10, 6))

    def get_rect(self):
        return pygame.Rect(self.x-self.width//2, self.y-self.height//2, 
                        self.width, self.height)


