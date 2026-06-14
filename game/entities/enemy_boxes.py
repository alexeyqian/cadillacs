import pygame
from game.settings import WORLD_WIDTH

class EnemyBoxMixin:
    def apply_world_bounds(self, world_width=None, lane_top=None, lane_bottom=None):
        # todo: remove these lines of temp code
        if world_width is None:
            world_width = WORLD_WIDTH
        if lane_top is None:
            lane_top = self.lane_top
        if lane_bottom is None:
            lane_bottom = self.lane_bottom

        # world boundaries
        half_w = self.width // 2
        self.x = max(half_w, self.x) # cannot go left of window
        self.x = min(self.x, world_width - half_w) # cannot go right window
        # beat'em up lane limits creates the illusion of depth
        # player walks on a horizontal strip, not full screen
        self.y = max(lane_top, self.y) # cannot go above lane_top
        self.y = min(lane_bottom, self.y) # cannot go below lane_bottom

    def get_left(self):
        return int(self.x - self.width / 2)

    def get_top(self):
        return self.y - self.height

    def get_right(self):
        return int(self.x + self.width / 2)

    def get_bottom(self):
        return self.y
    
    # on bottom center
    def get_collision_rect(self):
        return pygame.Rect(
            int(self.x - self.collision_box_w/2),
            int(self.y - self.collision_box_h),
            int(self.collision_box_w),
            int(self.collision_box_h)
        )

    # sprite frame rect
    def get_logical_rect(self):
        return pygame.Rect(
            int(self.get_left()),
            int(self.get_top()),
            int(self.width),
            int(self.height)
        )

    def get_hurt_rect(self):
        return pygame.Rect(
            int(self.get_left() + self.hurtbox_offset_x),
            int(self.get_top() + self.hurtbox_offset_y),
            int(self.hurtbox_w),
            int(self.hurtbox_h))
        
    # hit box
    def get_attack_rect(self):
        body_left = self.get_left()
        body_top = self.get_top()

        # Use symmetric hitbox size and offsets so left/right behave identically
        hit_w = self.attack_hitbox_w
        # giving running attack a longer hitbox
        #if self.state == self.RUN_ATTACK:
        #    hit_w = self.attack_hitbox_w * 1.5
        hit_h = self.attack_hitbox_h
        #if self.weapon and not self.weapon.is_ranged:
        #    hit_w += self.weapon.hitbox_w_bonus
        #    hit_h += self.weapon.hitbox_h_bonus

        hit_y = body_top + self.attack_hitbox_offset_y
        if self.facing_right:
            hit_x = int(self.x + self.width/2)
        else:
            hit_x = int(self.x - self.width/2 - hit_w)

        return pygame.Rect(hit_x, hit_y, hit_w, hit_h)