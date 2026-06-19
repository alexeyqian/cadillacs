import pygame

from game.colors import BLUE_COLOR, GREEN_COLOR, RED_COLOR, WHITE_COLOR


class CharacterDebugRenderer:
    def draw_combat_boxes(self, owner, screen, camera_x, line_width=1):
        collision_rect = owner.get_collision_rect()
        body_rect = owner.get_frame_rect()
        hurt_rect = owner.get_hurt_rect()
        attack_rect = owner.get_attack_rect()

        pygame.draw.rect(screen, BLUE_COLOR, (
            collision_rect.x - camera_x,
            collision_rect.y,
            collision_rect.width,
            collision_rect.height,
        ), line_width)
        pygame.draw.circle(
            screen,
            WHITE_COLOR,
            (int(owner.x - camera_x), int(owner.y)),
            3,
        )
        pygame.draw.rect(screen, WHITE_COLOR, (
            body_rect.x - camera_x,
            body_rect.y,
            body_rect.width,
            body_rect.height,
        ), line_width)
        pygame.draw.rect(screen, GREEN_COLOR, (
            hurt_rect.x - camera_x,
            hurt_rect.y,
            hurt_rect.width,
            hurt_rect.height,
        ), line_width)

        if attack_rect:
            pygame.draw.rect(screen, RED_COLOR, (
                attack_rect.x - camera_x,
                attack_rect.y,
                attack_rect.width,
                attack_rect.height,
            ), line_width)
