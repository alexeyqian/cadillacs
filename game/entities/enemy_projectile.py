import pygame
from game.settings import WORLD_WIDTH
from game.colors import WHITE_COLOR, YELLOW_COLOR

class EnemyProjectile:
    def __init__(self, x, y, direction, speed, damage, 
                lane_reach=0, width=16, height=16, shape='circle',
                lane_y=None):
        # x, y means center of the object rect
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.direction = direction
        self.speed = speed
        self.damage = damage
        self.lane_y = y if lane_y is None else lane_y
        self.lane_reach = lane_reach
        self.shape = shape
        self.active = True

    def update(self, world_width=WORLD_WIDTH):
        self.x += self.speed * self.direction
        if self.x <= -100:
            self.active = False
        if self.x > world_width:
            self.active = False

    def draw(self, screen, camera_x):
        screen_x = self.x - camera_x - self.width // 2
        screen_y = self.y - self.height // 2

        if self.shape == "ellipse":
            pygame.draw.ellipse(
                screen,
                YELLOW_COLOR,
                (screen_x, screen_y, self.width, self.height)
            )
            pygame.draw.ellipse(
                screen,
                WHITE_COLOR,
                (screen_x + 6, screen_y + 4, 10, 6)
            )
            return

        pygame.draw.circle(
            screen,
            YELLOW_COLOR,
            (int(self.x - camera_x), int(self.y)),
            max(4, self.width // 2)
        )

    def get_rect(self):
        return pygame.Rect(
            self.x-self.width//2, self.y-self.height//2, 
            self.width, self.height)
