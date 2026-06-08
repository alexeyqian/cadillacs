import pygame
from game.assets.asset_manager import AssetManager

class Prop:
    def __init__(self,x,y,image_file,layer="back",scale=1.0):
        self.x = x
        self.y = y
        self.layer = layer
        self.image = AssetManager.load_image(image_file, alpha=True)

        if scale != 1.0:
            w = int(self.image.get_width() * scale)
            h = int(self.image.get_height() * scale)
            self.image = pygame.transform.scale(self.image,(w, h))

    def draw(self, screen, camera_x):
        screen.blit(self.image, (self.x - camera_x,self.y))