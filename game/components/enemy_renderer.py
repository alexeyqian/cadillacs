import pygame
import game.settings as settings
from game.colors import WHITE_COLOR, YELLOW_COLOR
from game.components.debug_renderer import CharacterDebugRenderer

class EnemyRenderer:
    def draw(self, owner, screen, camera_x):
        frame = owner.animation_controller.get_current_frame_data()
        if not frame:
            raise ValueError(f"Missing frame data for enemy state: {owner.state}")

        image = owner.animation_controller.get_image()
        scale = owner.sprite_scale
        image = pygame.transform.scale(image,
            (image.get_width() * scale,
            image.get_height() * scale))
        if not owner.facing_right:
            image = pygame.transform.flip(image, True, False)

        frame_rect = owner.get_frame_rect()
        screen.blit(image, (frame_rect.x - camera_x, frame_rect.y))
        self.draw_health_bar(owner, screen, camera_x, frame_rect)

        if settings.SHOW_COMBAT_BOXES:
            self.draw_debug_boxes(owner, screen, camera_x)
            self.draw_debug_other(owner, screen, camera_x)

    def draw_health_bar(self, owner, screen, camera_x, frame_rect):
        bar_width = 50
        bar_x = int(owner.x - camera_x - bar_width / 2)
        hp_width = int(bar_width * (owner.health.hp / owner.health.max_hp))
        hp_height = 12

        pygame.draw.rect(screen,(120, 120, 120),
            (bar_x, frame_rect.y - hp_height, bar_width, 6)
        )
        pygame.draw.rect(screen,(255, 0, 0),
            (bar_x, frame_rect.y - hp_height, hp_width, 6))

    def draw_debug_boxes(self, owner, screen, camera_x):
        CharacterDebugRenderer().draw_combat_boxes(owner, screen, camera_x)

    def draw_debug_other(self, owner, screen, camera_x):
        timing_label = owner.combat_controller.get_attack_timing_label(owner)
        if timing_label:
            font = pygame.font.SysFont(None, 20)
            label = font.render(timing_label, True, YELLOW_COLOR)
            screen.blit(label, (int(owner.x - camera_x - 28), int(owner.y - 180)))
            
        if owner.flanking.has_target():
            font = pygame.font.SysFont(None, 20)
            label = font.render(f"FLANK {owner.flanking.target_side.upper()}", True, WHITE_COLOR)
            screen.blit(label, (int(owner.x - camera_x - 42), int(owner.y - 225)))
