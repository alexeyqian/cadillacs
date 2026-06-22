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
    def __init__(
        self,
        collision_box_w=PLAYER_COLLISION_W,
        collision_box_h=PLAYER_COLLISION_H,
        hurt_box_w=PLAYER_HURTBOX_W,
        hurt_box_h=PLAYER_HURTBOX_H,
        hurt_box_offset_x=PLAYER_HURTBOX_OFFSET_X,
        hurt_box_offset_y=PLAYER_HURTBOX_OFFSET_Y,
    ):
        self.collision_box_w = int(collision_box_w)
        self.collision_box_h = int(collision_box_h)
        self.hurt_box_w = int(hurt_box_w)
        self.hurt_box_h = int(hurt_box_h)
        self.hurt_box_offset_x = int(hurt_box_offset_x)
        self.hurt_box_offset_y = int(hurt_box_offset_y)

    def configure(
        self,
        collision_box_w,
        collision_box_h,
        hurt_box_w,
        hurt_box_h,
        hurt_box_offset_x,
        hurt_box_offset_y,
    ):
        self.collision_box_w = int(collision_box_w)
        self.collision_box_h = int(collision_box_h)
        self.hurt_box_w = int(hurt_box_w)
        self.hurt_box_h = int(hurt_box_h)
        self.hurt_box_offset_x = int(hurt_box_offset_x)
        self.hurt_box_offset_y = int(hurt_box_offset_y)

    def get_frame_rect(self, owner):
        frame = self._get_current_frame(owner)
        if not frame:
            raise ValueError(f"Missing frame data for {owner.state}")

        scale = frame.get_scale(owner.sprite_scale)
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
            -1 * self.collision_box_w // 2,
            -1 * self.collision_box_h,
            self.collision_box_w,
            self.collision_box_h,
        )
        return self._rect_to_world(owner, box)

    def get_hurt_rect(self, owner):
        box = pygame.Rect(
            self.hurt_box_offset_x,
            self.hurt_box_offset_y,
            self.hurt_box_w,
            self.hurt_box_h,
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
        return owner.animation_controller.get_current_frame()

    def _get_active_hitbox_data(self, owner):
        return owner.combat_controller.get_active_hitbox_data()

    def _rect_to_world(self, owner, box):
        return combat_box_to_world_rect(owner.x, owner.y, owner.facing_right, box)

    def _get_attack_anchor_y(self, owner):
        if self._uses_visual_y_for_attack(owner):
            return self._get_visual_y(owner)
        return owner.y

    def _uses_visual_y_for_attack(self, owner):
        return owner.air and owner.combat_controller.current_attack_name == owner.JUMP_ATTACK

    def _get_visual_y(self, owner):
        if not owner.air:
            return owner.y
        return owner.air.get_visual_y(owner.y)
