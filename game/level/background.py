import pygame
from game.managers.asset_manager import AssetManager

class Background:
    def __init__(self,far_file, mid_file = None, front_file = None):
        self.far = AssetManager.load_image(far_file, alpha=False)
        self.mid = AssetManager.load_image(mid_file, alpha=True) if mid_file else None
        self.front = AssetManager.load_image(front_file, alpha=True) if front_file else None

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

    def draw_far_and_mid(self, screen, camera_x):
        screen.blit(self.far, (-camera_x, 0))
        if self.mid:
            screen.blit(self.mid, (-camera_x, 0))

    def draw_front(self, screen, camera_x):
        if self.front:
            screen.blit(self.front, (-camera_x, 0))