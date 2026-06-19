import pygame

from game.combat.combat_geometry import combat_box_to_world_rect
from game.settings import (
    PLAYER_COLLISION_H,
    PLAYER_COLLISION_W,
    PLAYER_HURTBOX_H,
    PLAYER_HURTBOX_OFFSET_X,
    PLAYER_HURTBOX_OFFSET_Y,
    PLAYER_HURTBOX_W,
)


class CharacterGeometry:
    def get_frame_rect(self, owner):
        frame = self._get_current_frame(owner)
        if not frame:
            raise ValueError(f"Missing frame data for {owner.state}")

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

        world_y = self._get_visual_y(owner) + offset_y

        return pygame.Rect(
            int(world_x),
            int(world_y),
            int(frame_w),
            int(frame_h),
        )

    def get_collision_rect(self, owner):
        box = pygame.Rect(
            -1 * self._get_collision_box_w(owner) // 2,
            -1 * self._get_collision_box_h(owner),
            self._get_collision_box_w(owner),
            self._get_collision_box_h(owner),
        )
        return self._rect_to_world(owner, box)

    def get_hurt_rect(self, owner):
        box = pygame.Rect(
            self._get_hurt_box_offset_x(owner),
            self._get_hurt_box_offset_y(owner),
            self._get_hurt_box_w(owner),
            self._get_hurt_box_h(owner),
        )
        return self._rect_to_world(owner, box)

    def get_attack_rect(self, owner):
        hitbox = self._get_active_hitbox_data(owner)
        if not hitbox:
            return None

        box = pygame.Rect(
            hitbox.hitbox_offset_x,
            hitbox.hitbox_offset_y,
            hitbox.hitbox_w,
            hitbox.hitbox_h,
        )
        return combat_box_to_world_rect(
            owner.x,
            self._get_attack_anchor_y(owner),
            owner.facing_right,
            box,
        )

    def _get_current_frame(self, owner):
        animation_controller = getattr(owner, "animation_controller", None)
        if animation_controller and hasattr(animation_controller, "get_current_frame"):
            return animation_controller.get_current_frame()
        if hasattr(owner, "get_current_frame_data"):
            return owner.get_current_frame_data()
        return None

    def _get_active_hitbox_data(self, owner):
        combat = getattr(owner, "combat_controller", None)
        if not combat:
            return None
        try:
            return combat.get_active_hitbox_data(owner)
        except TypeError:
            return combat.get_active_hitbox_data()

    def _rect_to_world(self, owner, box):
        return combat_box_to_world_rect(owner.x, owner.y, owner.facing_right, box)

    def _get_attack_anchor_y(self, owner):
        if self._uses_visual_y_for_attack(owner):
            return self._get_visual_y(owner)
        return owner.y

    def _uses_visual_y_for_attack(self, owner):
        current_attack_name = getattr(
            getattr(owner, "combat_controller", None),
            "current_attack_name",
            None,
        )
        return current_attack_name == getattr(owner, "JUMP_ATTACK", None)

    def _get_visual_y(self, owner):
        air = getattr(owner, "air", None)
        if not air:
            return owner.y
        return air.get_visual_y(owner.y)

    def _get_collision_box_w(self, owner):
        return getattr(owner, "collision_box_w", PLAYER_COLLISION_W)

    def _get_collision_box_h(self, owner):
        return getattr(owner, "collision_box_h", PLAYER_COLLISION_H)

    def _get_hurt_box_w(self, owner):
        return getattr(owner, "hurt_box_w", PLAYER_HURTBOX_W)

    def _get_hurt_box_h(self, owner):
        return getattr(owner, "hurt_box_h", PLAYER_HURTBOX_H)

    def _get_hurt_box_offset_x(self, owner):
        return getattr(owner, "hurt_box_offset_x", PLAYER_HURTBOX_OFFSET_X)

    def _get_hurt_box_offset_y(self, owner):
        return getattr(owner, "hurt_box_offset_y", PLAYER_HURTBOX_OFFSET_Y)
