import pygame
from game.settings import WORLD_WIDTH

class EnemyBoxMixin:
    def apply_world_bounds(self, world_width=None, lane_top=None, lane_bottom=None):
        if world_width is None:
            world_width = WORLD_WIDTH
        if lane_top is None or lane_bottom is None:
            raise ValueError("Enemy.apply_world_bounds requires lane_top and lane_bottom")

        # world boundaries
        half_w = self.collision_box_w // 2
        self.x = max(half_w, self.x) # cannot go left of window
        self.x = min(self.x, world_width - half_w) # cannot go right window
        # beat'em up lane limits creates the illusion of depth
        # player walks on a horizontal strip, not full screen
        self.y = max(lane_top, self.y) # cannot go above lane_top
        self.y = min(lane_bottom, self.y) # cannot go below lane_bottom

    # on bottom center
    def get_collision_rect(self):
        return pygame.Rect(
            int(self.x - self.collision_box_w/2),
            int(self.y - self.collision_box_h),
            int(self.collision_box_w),
            int(self.collision_box_h)
        )

        frame = self.get_current_frame_data()

        if frame:
            if not frame.attack_rect:
                return None

            scale = self.sprite_scale

            local_x, local_y, w, h = frame.attack_rect
            offset_x, offset_y = frame.offset
            frame_w = frame.image.get_width()

            local_x *= scale
            local_y *= scale
            w *= scale
            h *= scale
            offset_x *= scale
            offset_y *= scale
            frame_w *= scale

            if self.facing_right:
                world_x = self.x + offset_x + local_x
            else:
                mirrored_x = frame_w - local_x - w
                world_x = self.x - frame_w - offset_x + mirrored_x

            world_y = self.y + offset_y + local_y

            return pygame.Rect(
                int(world_x),
                int(world_y),
                int(w),
                int(h)
            )

        return None
