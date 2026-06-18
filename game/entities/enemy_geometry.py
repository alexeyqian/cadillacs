import pygame
from game.settings import *
from game.entities.combat_geometry import combat_box_to_world_rect


class EnemyGeometry:
    def get_collision_rect(self, owner):
        return self._enemy_rect_to_world(owner,
                pygame.Rect(-1 * owner.collision_box_w // 2, -1 * owner.collision_box_h,
                owner.collision_box_w, owner.collision_box_h))
    #deprecated
    def get_collision_rect_old(self, owner):
        return pygame.Rect(
            int(owner.x - owner.collision_box_w / 2),
            int(owner.y - owner.collision_box_h),
            int(owner.collision_box_w),
            int(owner.collision_box_h)
        )

    def _enemy_rect_to_world(self, owner, box):
        return combat_box_to_world_rect(owner.x, owner.y, owner.facing_right, box)

    # deprecated
    def get_frame_rect(self, owner):
        frame = owner.get_current_frame_data()
        if not frame:
            raise ValueError(f"Missing frame data for enemy state: {owner.state}")

        scale = owner.sprite_scale
        offset_x, offset_y = frame.offset
        frame_w = frame.image.get_width() * scale
        frame_h = frame.image.get_height() * scale
        offset_x *= scale
        offset_y *= scale

        if owner.facing_right:
            world_x = owner.x + offset_x
        else:
            world_x = owner.x - frame_w - offset_x

        world_y = owner.y + offset_y
        return pygame.Rect(int(world_x), int(world_y), int(frame_w), int(frame_h))

    def get_hurt_rect(self, owner):
        return self._enemy_rect_to_world(owner,
                pygame.Rect(ENEMY_HURTBOX_OFFSET_X, ENEMY_HURTBOX_OFFSET_Y,
                ENEMY_HURTBOX_W, ENEMY_HURTBOX_H))
    # deprecated
    def get_hurt_rect_old(self, owner):
        frame = owner.get_current_frame_data()
        if not frame or not frame.hurt_rect:
            return pygame.Rect(int(owner.x), int(owner.y), 0, 0)

        return self._get_in_frame_box_rect(owner, frame.hurt_rect)

    def get_attack_rect(self, owner):
        return self._enemy_rect_to_world(owner,
                pygame.Rect(ENEMY_HIT_BOX_OFFSET_X, ENEMY_HIT_BOX_OFFSET_Y,
                ENEMY_HITBOX_W, ENEMY_HITBOX_H))
    # DEPRECATED
    def get_attack_rect_old(self, owner):
        if owner.state == owner.ATTACK:
            combat_hitbox = owner.combat.get_active_hitbox_data(owner)
            if combat_hitbox:
                return combat_box_to_world_rect(
                    owner.x,
                    owner.y,
                    owner.facing_right,
                    combat_hitbox
                )
            return None

        return None

    def _get_in_frame_box_rect(self, owner, local_rect):
        frame = owner.get_current_frame_data()
        scale = owner.sprite_scale

        local_x, local_y, w, h = local_rect
        offset_x, offset_y = frame.offset
        frame_w = frame.image.get_width()

        local_x *= scale
        local_y *= scale
        w *= scale
        h *= scale
        offset_x *= scale
        offset_y *= scale
        frame_w *= scale

        if owner.facing_right:
            world_x = owner.x + offset_x + local_x
        else:
            mirrored_x = frame_w - local_x - w
            world_x = owner.x - frame_w - offset_x + mirrored_x

        world_y = owner.y + offset_y + local_y
        return pygame.Rect(int(world_x), int(world_y), int(w), int(h))
    
