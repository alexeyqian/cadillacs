import pygame
from game.entities.combat_geometry import combat_box_to_world_rect


class EnemyHitboxes:
    # beat'em up lane limits creates the illusion of depth
    # player walks on a horizontal strip, not full screen
    def apply_world_bounds(self, owner, world_width, lane_top, lane_bottom):
        half_w = owner.collision_box_w // 2
        owner.x = max(half_w, owner.x)
        owner.x = min(owner.x, world_width - half_w)
        owner.y = max(lane_top, owner.y)
        owner.y = min(lane_bottom, owner.y)

    def get_collision_rect(self, owner):
        return pygame.Rect(
            int(owner.x - owner.collision_box_w / 2),
            int(owner.y - owner.collision_box_h),
            int(owner.collision_box_w),
            int(owner.collision_box_h)
        )

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
        frame = owner.get_current_frame_data()
        if not frame or not frame.hurt_rect:
            return pygame.Rect(int(owner.x), int(owner.y), 0, 0)

        return self._get_in_frame_box_rect(owner, frame.hurt_rect)

    def get_attack_rect(self, owner):
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

        frame = owner.get_current_frame_data()
        if not frame or not frame.attack_rect:
            return None

        return self._get_in_frame_box_rect(owner, frame.attack_rect)

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
    
