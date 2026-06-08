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

    def update(self):
        self.x += self.speed*self.direction
        if self.x < -200:
            self.active = False
        if self.x > 5000:
            self.active = False

    def draw(self, screen, camera_x):
        screen_x = self.x - camera_x

        pygame.draw.ellipse(
            screen, YELLOW_COLOR,
            (screen_x,self.y,self.width,self.height))

        pygame.draw.ellipse(
            screen,WHITE_COLOR,
            (screen_x + 6,self.y + 4,10,6))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


