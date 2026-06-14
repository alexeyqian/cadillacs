import pygame

from game.colors import GREEN_COLOR, YELLOW_COLOR
from game.settings import SHOW_ENEMY_RECT


class EnemyRendererMixin:
    def draw(self, screen, camera_x):
        screen_left = self.get_left() - camera_x

        image = self.animation_manager.get_image()
        if self.facing_right:
            image = pygame.transform.flip(image, True, False)
        if self.state == self.DEAD:
            image = self.animation_manager.get_image().copy()
            image.set_alpha(120) # draw dead enemy darker
        if self.state == self.KNOCKDOWN: # knockdown show enemy sideways
            image = pygame.transform.rotate(image, 90)
            image = pygame.transform.scale(image, (self.height, self.width))
        else:
            image = pygame.transform.scale(image, (self.width, self.height))

        # Center the scaled image inside the enemy bounding box so it visually aligns
        img_w, img_h = image.get_size()
        blit_x = screen_left + (self.width - img_w) // 2
        blit_y = self.y - img_h
        screen.blit(image, (blit_x, blit_y))

        if SHOW_ENEMY_RECT:
            body_rect = self.get_logical_rect()
            hurt_rect = self.get_hurt_rect()
            collision_rect = self.get_collision_rect()

            pygame.draw.rect(screen,GREEN_COLOR,
                (body_rect.x - camera_x, body_rect.y,
                body_rect.width, body_rect.height), 1)
            pygame.draw.rect(screen,(255, 80, 80),
                (hurt_rect.x - camera_x, hurt_rect.y,
                hurt_rect.width, hurt_rect.height), 1)
            pygame.draw.rect(screen, (80, 180, 255),
                (collision_rect.x - camera_x, collision_rect.y,
                collision_rect.width, collision_rect.height), 1)

            attack_rect = self.get_attack_rect()
            if attack_rect:
                pygame.draw.rect(screen, YELLOW_COLOR,
                    (attack_rect.x - camera_x, attack_rect.y,
                    attack_rect.width, attack_rect.height), 1)

        # health bar background
        bar_width = 50
        bar_x = int(self.x - camera_x - bar_width / 2)
        hp_width = int(bar_width * (self.hp / self.max_hp))
        hp_height = 12
        # todo: fix hardcode 50 and 6 here
        pygame.draw.rect(
            screen, (120, 120, 120),
            (bar_x, self.get_top() - hp_height, bar_width, 6))
        # health bar

        pygame.draw.rect(
            screen, (255, 0, 0),
            (bar_x, self.get_top() - hp_height, hp_width, 6))
