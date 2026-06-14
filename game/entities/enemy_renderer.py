import pygame

from game.settings import SHOW_ENEMY_RECT
from game.colors import GREEN_COLOR, YELLOW_COLOR


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

        if SHOW_ENEMY_RECT:
            self.draw_debug_boxes(owner, screen, camera_x)

        self.draw_health_bar(owner, screen, camera_x, frame_rect)

    def draw_debug_boxes(self, owner, screen, camera_x):
        body_rect = owner.get_logical_rect()
        hurt_rect = owner.get_hurt_rect()
        collision_rect = owner.get_collision_rect()
        attack_rect = owner.get_attack_rect()

        pygame.draw.rect(screen, (80, 180, 255), (
            collision_rect.x - camera_x,
            collision_rect.y,
            collision_rect.width,
            collision_rect.height
        ), 1)

        pygame.draw.rect(screen, GREEN_COLOR, (
            body_rect.x - camera_x,
            body_rect.y,
            body_rect.width,
            body_rect.height
        ), 1)

        if hurt_rect:
            pygame.draw.rect(screen, (255, 80, 80), (
                hurt_rect.x - camera_x,
                hurt_rect.y,
                hurt_rect.width,
                hurt_rect.height
            ), 1)

        if attack_rect:
            pygame.draw.rect(screen, YELLOW_COLOR, (
                attack_rect.x - camera_x,
                attack_rect.y,
                attack_rect.width,
                attack_rect.height
            ), 1)

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
