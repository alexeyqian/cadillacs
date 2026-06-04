import pygame

class Background:
    def __init__(self):
        self.far = None
        self.mid = None
        self.front = None

    def load(self, far_file, mid_file, front_file):
        self.far = pygame.image.load(far_file).convert()
        self.mid = pygame.image.load(mid_file).convert_alpha()
        self.front = pygame.image.load(front_file).convert_alpha()

    def draw(self, screen, camera_x):
        if self.far:
            far_x = -camera_x*0.2
            screen.blit(self.far, (far_x, 0))

        if self.mid:
            mid_x = -camera_x*0.5
            screen.blit(self.mid, (mid_x, 0))

    def draw_foreground(self, screen, camera_x):
        if self.front:
            front_x = -camera_x*0.8
            screen.blit(self.front, (front_x, 0))
