import pygame

from game.animation.frame_animation import FrameData
from game.data.enemy_config import DEFAULT_ENEMY_TYPE, get_enemy_config
from game.entities.enemy_state import EnemyState
from game.factories.enemy_factory import EnemyFactory
from game.entities.ferris_enemy import FerrisEnemy


class FakeEnemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def fake_frame_animation(animation_data, animation_key):
    return [FrameData(pygame.Surface((1, 1), pygame.SRCALPHA), (0, 0))]


def test_enemy_factory_uses_registered_enemy_classes():
    original_classes = EnemyFactory.enemy_classes.copy()
    try:
        EnemyFactory.register_enemy_type("test_enemy", FakeEnemy)

        enemy = EnemyFactory.create_enemy("test_enemy", 10, 20)

        assert isinstance(enemy, FakeEnemy)
        assert enemy.x == 10
        assert enemy.y == 20
    finally:
        EnemyFactory.enemy_classes = original_classes


def test_enemy_factory_falls_back_to_default_enemy_class():
    assert EnemyFactory.get_enemy_class("unknown") is FerrisEnemy
    assert EnemyFactory.get_enemy_class("unknown") is EnemyFactory.get_enemy_class(
        DEFAULT_ENEMY_TYPE
    )


def test_enemy_config_uses_default_fallback():
    fallback_config = get_enemy_config("unknown")

    assert fallback_config.enemy_id == DEFAULT_ENEMY_TYPE


def test_enemy_factory_builds_default_enemy_runtime_groups(monkeypatch):
    monkeypatch.setattr(
        "game.controllers.frame_animation_controller.load_frame_animation",
        fake_frame_animation,
    )

    enemy = EnemyFactory.create_enemy(DEFAULT_ENEMY_TYPE, 100, 200)

    # State
    assert enemy.state == EnemyState.IDLE
    assert enemy.life_cycle is not None

    # Capabilities
    assert enemy.health is not None
    assert enemy.geometry is not None
    assert enemy.geometry.collision_box_w == get_enemy_config(DEFAULT_ENEMY_TYPE).collision_box_w
    assert enemy.geometry.hurt_box_w == get_enemy_config(DEFAULT_ENEMY_TYPE).hurt_box_w
    assert enemy.movement is not None
    assert enemy.movement.spawn_x == 100
    assert enemy.movement.speed == get_enemy_config(DEFAULT_ENEMY_TYPE).speed
    assert enemy.movement.patrol_distance == get_enemy_config(DEFAULT_ENEMY_TYPE).patrol_distance
    assert enemy.movement.detect_range == get_enemy_config(DEFAULT_ENEMY_TYPE).detect_range
    assert enemy.flanking is not None

    # Controllers
    assert enemy.combat_controller is not None
    assert enemy.reaction_controller is not None
    assert enemy.lifecycle_controller is not None
    assert enemy.state_controller is not None
    assert enemy.loot_controller is not None

    # Presentation
    assert enemy.animation_controller is not None
    assert enemy.renderer is not None
