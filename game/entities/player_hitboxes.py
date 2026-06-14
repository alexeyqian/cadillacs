import pygame


class PlayerHitboxes:
    def get_frame_rect(self, owner):
        frame = owner.get_current_player_frame()
        if not frame:
            raise ValueError(f"Missing player frame data for {owner.state}")

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

        return pygame.Rect(
            int(world_x),
            int(world_y),
            int(frame_w),
            int(frame_h)
        )

    def get_hurt_rect(self, owner):
        frame = owner.get_current_player_frame()
        local_x, local_y, w, h = frame.hurt_rect
        return self._frame_local_rect_to_world(owner, frame, local_x, local_y, w, h)

    def get_collision_rect(self, owner):
        return pygame.Rect(
            int(owner.x - owner.collision_box_w / 2),
            int(owner.y - owner.collision_box_h),
            int(owner.collision_box_w),
            int(owner.collision_box_h)
        )

    def get_attack_rect(self, owner):
        if not owner.is_attacking:
            return None

        frame = owner.get_current_player_frame()
        if frame and frame.attack_rect:
            local_x, local_y, w, h = frame.attack_rect
            return self._frame_local_rect_to_world(owner, frame, local_x, local_y, w, h)

        return None

    def _frame_local_rect_to_world(self, owner, frame, local_x, local_y, w, h):
        scale = owner.sprite_scale
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