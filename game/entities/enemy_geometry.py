import pygame
from game.settings import *
from game.entities.combat_geometry import combat_box_to_world_rect


class EnemyGeometry:
    def get_collision_rect(self, owner):
        return self._enemy_rect_to_world(owner,
                pygame.Rect(-1 * owner.collision_box_w // 2, -1 * owner.collision_box_h,
                owner.collision_box_w, owner.collision_box_h))
    
    def get_hurt_rect(self, owner):
        return self._enemy_rect_to_world(owner,
                pygame.Rect(owner.hurt_box_offset_x, owner.hurt_box_offset_y,
                owner.hurt_box_w, owner.hurt_box_h))

    def get_attack_rect(self, owner):
        if owner.state == owner.ATTACK:
            hitbox = owner.combat.get_active_hitbox_data(owner)
            if hitbox:
                return combat_box_to_world_rect(
                    owner.x, owner.y, owner.facing_right, hitbox)
        return None

    def get_frame_rect(self, owner):
        frame = owner.get_current_frame_data()
        if not frame:
            raise ValueError(f"Missing frame data for enemy state: {owner.state}")

        scale = owner.sprite_scale
        frame_w = frame.image.get_width() * scale
        frame_h = frame.image.get_height() * scale
        offset_x, offset_y = frame.offset
        offset_x *= scale
        offset_y *= scale

        if owner.facing_right:
            world_x = owner.x + offset_x
        else:
            world_x = owner.x - frame_w - offset_x

        world_y = owner.y + offset_y
        return pygame.Rect(int(world_x), int(world_y), int(frame_w), int(frame_h))

    def _enemy_rect_to_world(self, owner, box):
        return combat_box_to_world_rect(owner.x, owner.y, owner.facing_right, box)
