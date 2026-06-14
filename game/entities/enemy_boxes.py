import pygame
from game.settings import WORLD_WIDTH

class EnemyBoxMixin:
    def apply_world_bounds(self, world_width=None, lane_top=None, lane_bottom=None):
        if world_width is None:
            world_width = WORLD_WIDTH
        if lane_top is None or lane_bottom is None:
            raise ValueError("Enemy.apply_world_bounds requires lane_top and lane_bottom")

        self.hitboxes.apply_world_bounds(self, world_width, lane_top, lane_bottom)

    # on bottom center
    def get_collision_rect(self):
        return self.hitboxes.get_collision_rect(self)
