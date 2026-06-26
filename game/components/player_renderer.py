import pygame
import game.settings as settings
from game.components.debug_renderer import CharacterDebugRenderer

# Fraction of sprite height from the top where the hand sits.
# Tune per weapon type if needed.
_HAND_Y_FRACTION = 0.45
# Horizontal offset inward from the leading edge of the sprite (pixels, pre-scale).
_HAND_X_INSET = 20
# Scale applied to weapon overlay relative to sprite scale.
_WEAPON_OVERLAY_SCALE = 1.0

# States where the weapon is baked into the attack animation — no overlay drawn.
_ATTACK_STATES = {"ATTACK", "ATTACK2", "ATTACK3", "RUN_ATTACK", "JUMP_ATTACK",
                  "ATTACK_KNIFE", "ATTACK_PISTOL"}

# A renderer is stateless presentation code, not a state driver. so not rename it to RenderController
# "controller" in this codebase means something specific: it holds behavior logic that drives state transitions (AI, lifecycle, combat). 
class PlayerRenderer:
    def draw(self, owner, screen, camera_x):
        frame = owner.animation_controller.get_current_frame()
        image = owner.animation_controller.get_image()
        scale = frame.get_scale(owner.sprite_scale)
        image = pygame.transform.scale(
            image,
            (int(image.get_width() * scale), int(image.get_height() * scale))
        )

        if not owner.facing_right:
            image = pygame.transform.flip(image, True, False)

        offset_x, offset_y = frame.offset
        offset_x *= scale
        offset_y *= scale

        if owner.facing_right:
            sprite_world_x = owner.x + offset_x
        else:
            sprite_world_x = owner.x - image.get_width() - offset_x

        visual_y = owner.movement.air.get_visual_y(owner.y) if owner.movement.air else owner.y
        sprite_y = visual_y + offset_y
        screen.blit(image, (sprite_world_x - camera_x, sprite_y))

        self._draw_weapon_overlay(owner, screen, camera_x,
                                sprite_world_x, sprite_y, image.get_width(), image.get_height(), scale)
        self.draw_player_debug_boxes(screen, camera_x, owner)

    def _draw_weapon_overlay(self, owner, screen, camera_x,
                            sprite_world_x, sprite_y, sprite_w, sprite_h, scale):
        anim_state = owner.animation_controller.get_animation_state(owner)
        if anim_state in _ATTACK_STATES:
            return

        weapon = owner.weapon_slot.weapon
        if weapon is None:
            return

        overlay = weapon.get_overlay_image(_WEAPON_OVERLAY_SCALE * scale)
        if overlay is None:
            return

        hand_x, hand_y = self._get_hand_position(
            owner, sprite_world_x, sprite_y, sprite_w, sprite_h, scale, anim_state)

        if not owner.facing_right:
            overlay = pygame.transform.flip(overlay, True, False)

        screen.blit(overlay, (hand_x - camera_x, hand_y - overlay.get_height() // 2))

    def _get_hand_position(self, owner, sprite_world_x, sprite_y,
                        sprite_w, sprite_h, scale, anim_state):
        frame_index = owner.animation_controller.get_current_frame_index()
        anim_config = owner.animation_controller.animation_data.get(anim_state, {})
        hand_anchors = anim_config.get("hand_anchors")

        if hand_anchors and frame_index < len(hand_anchors):
            # hand_anchors are in facing-right space, relative to bottom-center (owner.x, owner.y).
            anchor_x, anchor_y = hand_anchors[frame_index]
            visual_y = owner.movement.air.get_visual_y(owner.y) if owner.movement.air else owner.y
            if owner.facing_right:
                hand_x = owner.x + anchor_x * scale
            else:
                hand_x = owner.x - anchor_x * scale
            hand_y = visual_y + anchor_y * scale
        else:
            # Fallback: fixed fraction of sprite dimensions.
            if owner.facing_right:
                hand_x = sprite_world_x + sprite_w - _HAND_X_INSET * scale
            else:
                hand_x = sprite_world_x + _HAND_X_INSET * scale
            hand_y = sprite_y + sprite_h * _HAND_Y_FRACTION

        return hand_x, hand_y

    def draw_health_bar(self, owner, screen, screen_x):
        hb_w = owner.width
        hb_h = 8
        hb_x = int(screen_x - hb_w / 2)
        hb_y = owner.get_top() - 16

        pygame.draw.rect(screen, (100, 100, 100), (hb_x, hb_y, hb_w, hb_h))

        fill_ratio = max(0.0, min(1.0, float(owner.health.hp) / float(owner.health.max_hp)))
        hp_w = int(hb_w * fill_ratio)
        pygame.draw.rect(screen, (0, 255, 0), (hb_x, hb_y, hp_w, hb_h))

    def draw_player_debug_boxes(self, screen, camera_x, player):
        if not settings.SHOW_COMBAT_BOXES:
            return

        CharacterDebugRenderer().draw_combat_boxes(
            player,
            screen,
            camera_x,
            line_width=2,
        )
