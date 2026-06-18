import pygame
from game.settings import *
from game.entities.combat_geometry import combat_box_to_world_rect


class PlayerGeometry:
    # todo: deprecated
    def get_frame_rect(self, owner):
        frame = owner.animation_controller.get_current_frame()
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

        world_y = self._get_visual_y(owner) + offset_y

        return pygame.Rect(
            int(world_x),
            int(world_y),
            int(frame_w),
            int(frame_h)
        )

    def get_hurt_rect(self, owner):
        return self._player_rect_to_world(owner,
                pygame.Rect(PLAYER_HURTBOX_OFFSET_X, PLAYER_HURTBOX_OFFSET_Y,
                PLAYER_HURTBOX_W, PLAYER_HURTBOX_H))
    
    def get_counter_hurt_rect(self, owner):
        combat_counter_hurtbox = owner.combat.get_active_counter_hurtbox_data()
        if combat_counter_hurtbox:
            return self._counter_hurt_rect_to_world(owner, combat_counter_hurtbox)
        return None

    def get_collision_rect(self, owner):
        return self._player_rect_to_world(owner,
                pygame.Rect(-1 * PLAYER_COLLISION_W//2, -1*PLAYER_COLLISION_H,
                PLAYER_COLLISION_W, PLAYER_COLLISION_H))
    # todo: deprecated
    def get_collision_rect_old(self, owner):
        return pygame.Rect(
            int(owner.x - owner.collision_box_w / 2),
            int(owner.y - owner.collision_box_h),
            int(owner.collision_box_w),
            int(owner.collision_box_h)
        )

    def get_attack_rect(self, owner):
        combat_hitbox = owner.combat.get_active_hitbox_data()
        if combat_hitbox:
            return self._attack_hitbox_to_world(owner, combat_hitbox)
        return None

    def _player_rect_to_world(self, owner, box):
        return combat_box_to_world_rect(owner.x, owner.y, owner.facing_right, box)

    def _attack_hitbox_to_world(self, owner, attack):
        anchor_y = owner.y
        if owner.combat.current_attack_name == getattr(owner, "JUMP_ATTACK", None):
            anchor_y = self._get_visual_y(owner)
        box = pygame.Rect(
            attack.hitbox_offset_x,
            attack.hitbox_offset_y,
            attack.hitbox_w,
            attack.hitbox_h,
        )
        return combat_box_to_world_rect(owner.x, anchor_y, owner.facing_right, box)

    def _counter_hurt_rect_to_world(self, owner, attack):
        box = pygame.Rect(
            attack.counter_hurtbox_offset_x,
            attack.counter_hurtbox_offset_y,
            attack.counter_hurtbox_w,
            attack.counter_hurtbox_h,
        )
        return self._attack_rect_to_world(owner, box)

    def _attack_rect_to_world(self, owner, box):
        anchor_y = owner.y
        if owner.combat.current_attack_name == getattr(owner, "JUMP_ATTACK", None):
            anchor_y = self._get_visual_y(owner)
        return combat_box_to_world_rect(owner.x, anchor_y, owner.facing_right, box)

    def _get_visual_y(self, owner):
        air = getattr(owner, "air", None)
        if not air:
            return owner.y
        return air.get_visual_y(owner.y)
