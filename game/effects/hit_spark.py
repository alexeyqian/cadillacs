import pygame

class HitSpark:
    def __init_(self, x, y):
        self.x = x
        self.y = y
        
        self.timer = 12
        self.active = True
        
    def update(self):
        self.timer -= 1
        if self.timer <= 0:
            self.active = False
            
    def draw(self, screen, camera_x):
        screen_x = self.x - camera_x
        radius = self.timer * 2
        
        pygame.draw.circle(
            screen,
            (255, 255, 120),
            (int(screen_x), int(self.y)),
            radius,
            2
        )

        pygame.draw.line(
            screen,
            (255, 255, 255),
            (screen_x - radius, self.y),
            (screen_x + radius, self.y),
            2
        )

        pygame.draw.line(
            screen,
            (255, 255, 255),
            (screen_x, self.y - radius),
            (screen_x, self.y + radius),
            2
        )