import pygame
from game.assets.asset_manager import AssetManager

class Background:
    def __init__(self,far_file,mid_file,front_file):
        self.far = AssetManager.load_image(far_file, alpha=False)
        self.mid = AssetManager.load_image(mid_file, alpha=True)
        self.front = AssetManager.load_image(front_file, alpha=True)

    def draw_layer(self,screen,image,camera_x,scroll_speed, offset_y=0):
        image_width = image.get_width()
        x = -camera_x * scroll_speed

        # repeat image horizontally
        while x > 0:
            x -= image_width

        while x < screen.get_width():
            # todo: remove the offset
            screen.blit(image, (x, 0+offset_y))
            x += image_width

    def draw_back(self,screen,camera_x):
        self.draw_layer(screen,self.far,camera_x,0.25)
        self.draw_layer(screen,self.mid,camera_x,0.55, 120)

    def draw_front(self,screen,camera_x):
        self.draw_layer(screen,self.front,camera_x,0.85)