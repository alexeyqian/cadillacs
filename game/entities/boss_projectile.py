import pygame

class BossProjectile:
    def __init__(self, x, y, direction, damage):
        self.x = x
        self.y = y
        self.direction = direction
        self.damage = damage
        self.speed = 7
        self.width = 28
        self.height = 18
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
            screen,
            (120, 220, 255),
            (screen_x,self.y,self.width,self.height))

        pygame.draw.ellipse(
            screen,
            (255, 255, 255),
            (screen_x + 6,self.y + 4,10,6))
        
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


