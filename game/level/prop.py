import pygame


class Prop:
    def __init__(self,x,y,image_file,layer="back",scale=1.0):
        self.x = x
        self.y = y
        self.layer = layer
        self.image = pygame.image.load(image_file).convert_alpha()

        if scale != 1.0:
            w = int(self.image.get_width() * scale)
            h = int(self.image.get_height() * scale)
            self.image = pygame.transform.scale(self.image,(w, h))

    def draw(self, screen, camera_x):
        screen.blit(self.image, (self.x - camera_x,self.y))