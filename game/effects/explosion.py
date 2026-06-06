import pygame

class Explosion:
    def __init__(self, x, y, radius=180):
        self.x = x
        self.y = y
        self.radius = radius
        self.timer = 20
        self.active = True
        
    def update(self):
        self.timer -= 1
        if self.timer <= 0:
            self.active = False
            
    def draw(self, screen, camera_x):
        screen_x = self.x - camera_x
        current_radius = int(self.radius*(self.timer/20))
        pygame.draw.circle(screen, (255,180,0),
            (int(screen_x), int(self.y)),
            current_radius, 4)
        pygame.draw.circle(screen, (255,60,0),
            (int(screen_x), int(self.y)),
            current_radius // 2, 4)