import pygame
import game.settings as settings
from game.settings import *
from game.colors import *

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
        screen_x = owner.x - camera_x

        image = owner.animation_controller.get_image()
        scale = owner.sprite_scale
        image = pygame.transform.scale(
            image,
            (image.get_width() * scale, image.get_height() * scale)
        )

        if not owner.facing_right:
            image = pygame.transform.flip(image, True, False)

        frame = owner.animation_controller.get_current_frame()
        offset_x, offset_y = frame.offset
        offset_x *= scale
        offset_y *= scale

        if owner.facing_right:
            sprite_world_x = owner.x + offset_x
        else:
            sprite_world_x = owner.x - image.get_width() - offset_x

        air = getattr(owner, "air", None)
        visual_y = air.get_visual_y(owner.y) if air else owner.y
        sprite_y = visual_y + offset_y
        screen.blit(image, (sprite_world_x - camera_x, sprite_y))

        #self.draw_health_bar(owner, screen, screen_x)
        self.draw_player_debug_boxes(screen, camera_x, owner)

    def draw_health_bar(self, owner, screen, screen_x):
        hb_w = owner.width
        hb_h = 8
        hb_x = int(screen_x - hb_w / 2)
        hb_y = owner.get_top() - 16

        pygame.draw.rect(screen, (100, 100, 100), (hb_x, hb_y, hb_w, hb_h))

        try:
            fill_ratio = max(0.0, min(1.0, float(owner.health.hp) / float(owner.health.max_hp)))
        except Exception:
            fill_ratio = 0

        hp_w = int(hb_w * fill_ratio)
        pygame.draw.rect(screen, (0, 255, 0), (hb_x, hb_y, hp_w, hb_h))

    def draw_player_debug_boxes(self, screen, camera_x, player):
        if not settings.SHOW_COMBAT_BOXES:
            return

        collision_rect = player.get_collision_rect()
        body_rect = player.get_frame_rect()
        hurt_rect = player.get_hurt_rect()
        #counter_hurt_rect = player.get_counter_hurt_rect()
        attack_rect = player.get_attack_rect()

        # blue = collision / feet box
        pygame.draw.rect(screen, BLUE_COLOR, (
            collision_rect.x - camera_x,
            collision_rect.y,
            collision_rect.width,
            collision_rect.height
        ), 1)
        # small feet anchor marker
        pygame.draw.circle(
            screen,
            WHITE_COLOR,
            (int(player.x - camera_x), int(player.y)),
            3
        )

        # white = full animation frame / visual reference
        pygame.draw.rect(screen, WHITE_COLOR, (
            body_rect.x - camera_x,
            body_rect.y,
            body_rect.width,
            body_rect.height
        ), 1)

        pygame.draw.rect(screen, GREEN_COLOR, (
            hurt_rect.x - camera_x,
            hurt_rect.y,
            hurt_rect.width,
            hurt_rect.height
        ), 2)

        #pygame.draw.rect(screen, ORANGE_COLOR, (
        #    counter_hurt_rect.x - camera_x,
        #    counter_hurt_rect.y,
        #    counter_hurt_rect.width,
        #    counter_hurt_rect.height
        #), 2)

        pygame.draw.rect(screen, RED_COLOR, (
            attack_rect.x - camera_x,
            attack_rect.y,
            attack_rect.width,
            attack_rect.height
        ), 2)

        #timing_label = player.combat.get_attack_timing_label()
        #if timing_label:
        #    font = pygame.font.SysFont(None, 20)
        #    label = font.render(timing_label, True, YELLOW_COLOR)
        #    screen.blit(label, (int(player.x - camera_x - 42), int(player.y - 210)))

