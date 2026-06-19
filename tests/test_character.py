import pytest

from game.entities.character import Character
from game.entities.game_object import GameObject


class FakeGeometry:
    def get_frame_rect(self, owner):
        return ("frame", owner.x, owner.y)

    def get_collision_rect(self, owner):
        return ("collision", owner.x, owner.y)

    def get_hurt_rect(self, owner):
        return ("hurt", owner.x, owner.y)

    def get_attack_rect(self, owner):
        return ("attack", owner.x, owner.y)


class FakeMovement:
    def __init__(self):
        self.calls = []

    def apply_world_bounds(self, owner, world_width=None, lane_top=None, lane_bottom=None):
        self.calls.append((owner, world_width, lane_top, lane_bottom))


class FakeRenderer:
    def __init__(self):
        self.calls = []

    def draw(self, owner, screen, camera_x):
        self.calls.append((owner, screen, camera_x))


def test_character_extends_game_object_with_shared_fields():
    character = Character(
        x=10,
        y=20,
        width=30,
        height=40,
        state="IDLE",
        facing_right=False,
        speed=5,
        sprite_scale=3,
    )

    assert isinstance(character, GameObject)
    assert character.x == 10
    assert character.y == 20
    assert character.width == 30
    assert character.height == 40
    assert character.state == "IDLE"
    assert character.facing_right is False
    assert character.speed == 5
    assert character.sprite_scale == 3
    assert character.active is True
    assert character.visible is True


def test_character_delegates_geometry_methods_to_geometry_component():
    character = Character(10, 20)
    character.geometry = FakeGeometry()

    assert character.get_frame_rect() == ("frame", 10, 20)
    assert character.get_collision_rect() == ("collision", 10, 20)
    assert character.get_hurt_rect() == ("hurt", 10, 20)
    assert character.get_attack_rect() == ("attack", 10, 20)


def test_character_delegates_world_bounds_to_movement_component():
    character = Character()
    character.movement = FakeMovement()

    character.apply_world_bounds(world_width=1000, lane_top=300, lane_bottom=800)

    assert character.movement.calls == [(character, 1000, 300, 800)]


def test_character_delegates_draw_to_renderer_when_visible():
    character = Character()
    character.renderer = FakeRenderer()

    character.draw(screen="screen", camera_x=12)

    assert character.renderer.calls == [(character, "screen", 12)]


def test_character_skips_draw_when_not_visible():
    character = Character()
    character.visible = False
    character.renderer = FakeRenderer()

    character.draw(screen="screen", camera_x=12)

    assert character.renderer.calls == []


def test_character_reports_missing_required_component():
    character = Character()

    with pytest.raises(AttributeError, match="requires a geometry component"):
        character.get_frame_rect()
