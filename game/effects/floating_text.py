import pygame

class FloatingText:
    def __init__(self, x, y, text, color=(255,255,0)):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        
        self.timer = 60
        self.active = True
        
    def update(self):
        self.y -= 0.5
        self.timer -= 1
        if self.timer <= 0:
            self.active = False
            
    def draw(self, screen, camera_x):
        font = pygame.font.SysFont(None, 24)
        image = font.render(self.text, True, self.color)
        screen.blit(image, (self.x - camera_x, self.y))