import pygame

class EnemyProjectile:
    def __init__(self, x, y, direction, damage):
        self.x = x
        self.y = y
        self.direction = direction
        self.damage = damage

        self.speed = 6
        self.width = 16
        self.height = 16
        self.active = True

    def update(self):
        self.x += self.speed * self.direction
        if self.x <= -100:
            self.active = False
        if self.x > 5000:
            self.active = False

    def draw(self, screen, camera_x):
        pygame.draw.circle(screen, (255, 50, 50),
            (int(self.x-camera_x), int(self.y)), 8)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

