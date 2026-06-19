import pygame

from game.colors import BLUE_COLOR, GREEN_COLOR, RED_COLOR, WHITE_COLOR
from game.components.debug_renderer import CharacterDebugRenderer


class DebugOwner:
    x = 20
    y = 30

    def get_collision_rect(self):
        return pygame.Rect(10, 20, 8, 8)

    def get_frame_rect(self):
        return pygame.Rect(30, 20, 8, 8)

    def get_hurt_rect(self):
        return pygame.Rect(10, 40, 8, 8)

    def get_attack_rect(self):
        return pygame.Rect(30, 40, 8, 8)


def test_debug_renderer_draws_combat_boxes_to_surface():
    surface = pygame.Surface((80, 80))
    owner = DebugOwner()

    CharacterDebugRenderer().draw_combat_boxes(owner, surface, camera_x=0)

    assert surface.get_at((10, 20))[:3] == BLUE_COLOR
    assert surface.get_at((30, 20))[:3] == WHITE_COLOR
    assert surface.get_at((10, 40))[:3] == GREEN_COLOR
    assert surface.get_at((30, 40))[:3] == RED_COLOR
