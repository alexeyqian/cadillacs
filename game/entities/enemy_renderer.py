import pygame
import game.settings as settings
from game.settings import SHOW_COMBAT_BOXES
from game.colors import *


class EnemyRenderer:
    def draw(self, owner, screen, camera_x):
        frame = owner.get_current_frame_data()

        if not frame:
            raise ValueError(f"Missing frame data for enemy state: {owner.state}")

        image = owner.animation_controller.get_image()

        scale = owner.sprite_scale
        image = pygame.transform.scale(
            image,
            (
                image.get_width() * scale,
                image.get_height() * scale
            )
        )

        if not owner.facing_right:
            image = pygame.transform.flip(image, True, False)

        frame_rect = owner.get_frame_rect()
        screen.blit(image, (frame_rect.x - camera_x, frame_rect.y))

        if settings.SHOW_COMBAT_BOXES:
            self.draw_debug_boxes(owner, screen, camera_x)

        self.draw_health_bar(owner, screen, camera_x, frame_rect)

    # todo: dup? merge with player's same function
    def draw_debug_boxes(self, owner, screen, camera_x):
        collision_rect = owner.get_collision_rect()
        body_rect = owner.get_logical_rect()
        hurt_rect = owner.get_hurt_rect()
        attack_rect = owner.get_attack_rect()

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
            (int(owner.x - camera_x), int(owner.y)),
            3
        )

        # white = full animation frame / visual reference
        pygame.draw.rect(screen, WHITE_COLOR, (
            body_rect.x - camera_x,
            body_rect.y,
            body_rect.width,
            body_rect.height
        ), 1)

        # green = current animation frame hurt box
        if hurt_rect:
            pygame.draw.rect(screen, GREEN_COLOR, (
                hurt_rect.x - camera_x,
                hurt_rect.y,
                hurt_rect.width,
                hurt_rect.height
            ), 1)

        # red = current animation frame attack box
        if attack_rect:
            pygame.draw.rect(screen, RED_COLOR, (
                attack_rect.x - camera_x,
                attack_rect.y,
                attack_rect.width,
                attack_rect.height
            ), 1)
            
        phase_name = owner.get_attack_phase_name()
        if phase_name:
            font = pygame.font.SysFont(None, 20)
            label = font.render(phase_name, True, YELLOW_COLOR)
            screen.blit(label, (int(owner.x - camera_x - 28), int(owner.y - 180)))
            
        if owner.flank_target_side:
            font = pygame.font.SysFont(None, 20)
            label = font.render(f"FLANK {owner.flank_target_side.upper()}", True, WHITE_COLOR)
            screen.blit(label, (int(owner.x - camera_x - 42), int(owner.y - 225)))

    def draw_health_bar(self, owner, screen, camera_x, frame_rect):
        bar_width = 50
        bar_x = int(owner.x - camera_x - bar_width / 2)
        hp_width = int(bar_width * (owner.health.hp / owner.health.max_hp))
        hp_height = 12

        pygame.draw.rect(
            screen,
            (120, 120, 120),
            (bar_x, frame_rect.y - hp_height, bar_width, 6)
        )
        pygame.draw.rect(
            screen,
            (255, 0, 0),
            (bar_x, frame_rect.y - hp_height, hp_width, 6)
        )
