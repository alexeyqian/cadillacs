import pygame
from game.settings import WORLD_WIDTH
from game.colors import YELLOW_COLOR
class Projectile:
    def __init__(self, x, y, direction, speed, damage, lane_reach=0):
        self.x = x
        self.y = y
        self.width = 12
        self.height = 4
        self.direction = direction
        self.speed = speed
        self.damage = damage
        self.active = True
        # projectiles remember the lane/depth where they were fired.
        self.lane_y = y
        self.lane_reach = lane_reach

    def update(self, world_width=WORLD_WIDTH):
        self.x += self.speed * self.direction
        if self.x < -100:
            self.active = False
        if self.x > world_width:
            self.active = False

    def draw(self, screen, camera_x):
        screen_x = self.x - camera_x
        pygame.draw.rect(screen, YELLOW_COLOR,
                (screen_x, self.y, self.width, self.height))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
