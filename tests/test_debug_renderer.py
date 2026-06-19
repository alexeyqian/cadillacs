import pygame

from game.colors import BLUE_COLOR, GREEN_COLOR, RED_COLOR, WHITE_COLOR
import game.settings as settings
from game.components.debug_renderer import CharacterDebugRenderer
from game.components.enemy_renderer import EnemyRenderer
from game.components.player_renderer import PlayerRenderer


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


class CountingDebugRenderer:
    def __init__(self):
        self.calls = 0

    def draw_combat_boxes(self, owner, screen, camera_x, line_width=1):
        self.calls += 1


class FakeFrame:
    offset = (0, 0)
    image = pygame.Surface((2, 2), pygame.SRCALPHA)


class FakeAnimationController:
    def get_current_frame_data(self):
        return FakeFrame()

    def get_image(self):
        return pygame.Surface((2, 2), pygame.SRCALPHA)


class FakeCombatController:
    def get_attack_timing_label(self, owner):
        return ""


class FakeFlanking:
    def has_target(self):
        return False


class EnemyDebugOwner:
    x = 20
    y = 30
    state = "IDLE"
    facing_right = True
    sprite_scale = 1
    animation_controller = FakeAnimationController()
    combat_controller = FakeCombatController()
    health = type("Health", (), {"hp": 1, "max_hp": 1})()
    flanking = FakeFlanking()

    def get_frame_rect(self):
        return pygame.Rect(20, 30, 2, 2)


def test_debug_renderer_draws_combat_boxes_to_surface():
    surface = pygame.Surface((80, 80))
    owner = DebugOwner()

    CharacterDebugRenderer().draw_combat_boxes(owner, surface, camera_x=0)

    assert surface.get_at((10, 20))[:3] == BLUE_COLOR
    assert surface.get_at((30, 20))[:3] == WHITE_COLOR
    assert surface.get_at((10, 40))[:3] == GREEN_COLOR
    assert surface.get_at((30, 40))[:3] == RED_COLOR


def test_player_renderer_reads_runtime_debug_flag(monkeypatch):
    surface = pygame.Surface((80, 80))
    debug_renderer = CountingDebugRenderer()
    monkeypatch.setattr(settings, "SHOW_COMBAT_BOXES", True)
    monkeypatch.setattr(
        "game.components.player_renderer.CharacterDebugRenderer",
        lambda: debug_renderer,
    )

    PlayerRenderer().draw_player_debug_boxes(surface, camera_x=0, player=DebugOwner())

    assert debug_renderer.calls == 1


def test_enemy_renderer_reads_runtime_debug_flag(monkeypatch):
    surface = pygame.Surface((80, 80))
    debug_renderer = CountingDebugRenderer()
    monkeypatch.setattr(settings, "SHOW_COMBAT_BOXES", True)
    monkeypatch.setattr(
        "game.components.enemy_renderer.CharacterDebugRenderer",
        lambda: debug_renderer,
    )

    EnemyRenderer().draw(EnemyDebugOwner(), surface, camera_x=0)

    assert debug_renderer.calls == 1
