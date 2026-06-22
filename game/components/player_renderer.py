import pygame
import game.settings as settings
from game.components.debug_renderer import CharacterDebugRenderer

class PlayerRenderer:
    #World:   [--------------------PLAYER----]
    #                          x=800
    #Screen window starts at camera_x=600:
    #	      [    window    ]
    #	       600          1200
    #Player appears at pixel 200 inside the window → screen_x = 200
    def draw(self, owner, screen, camera_x):
        # camera_x is how far the camera has scrolled.
        # Subtracting it converts the player's world position->screen position
        # player's screen x position after camera offset
        # bottom-center screen x:
        # add depth
        # Now moving up/down looks more like a beat'em-up character walking in depth.
        # shadow_rect = pygame.Rect(screen_x,self.y + self.height - 10,self.width,12)
        #pygame.draw.ellipse(screen,(50, 50, 50),shadow_rect)
        # end of depth
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

        visual_y = owner.air.get_visual_y(owner.y) if owner.air else owner.y
        sprite_y = visual_y + offset_y
        screen.blit(image, (sprite_world_x - camera_x, sprite_y))

        self.draw_player_debug_boxes(screen, camera_x, owner)

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
