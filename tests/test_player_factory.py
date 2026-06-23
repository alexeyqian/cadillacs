import pygame

from game.animation.frame_animation import FrameData
from game.entities.mustapha_player import MustaphaPlayer
from game.entities.player_state import PlayerState
from game.data.player_config import DEFAULT_PLAYER_TYPE, get_player_config
from game.factories.player_factory import PlayerFactory


class FakePlayer:
    pass


def fake_frame_animation(animation_data, animation_key):
    frame_count = animation_data[animation_key].get("frames_count", 1)
    return [
        FrameData(pygame.Surface((1, 1), pygame.SRCALPHA), (0, 0))
        for _ in range(frame_count)
    ]


def test_player_factory_uses_registered_player_classes():
    original_classes = PlayerFactory.player_classes.copy()
    try:
        PlayerFactory.register_player_type("test_player", FakePlayer)

        player = PlayerFactory.create_player("test_player")

        assert isinstance(player, FakePlayer)
    finally:
        PlayerFactory.player_classes = original_classes


def test_player_factory_falls_back_to_default_player_class():
    assert PlayerFactory.get_player_class("unknown") is MustaphaPlayer
    assert PlayerFactory.get_player_class("unknown") is PlayerFactory.get_player_class(
        DEFAULT_PLAYER_TYPE
    )


def test_player_factory_registers_mustapha_player_type():
    assert PlayerFactory.get_player_class("mustapha") is MustaphaPlayer
    assert "mustapha" in PlayerFactory.registered_player_types()


def test_player_config_uses_default_fallback():
    config = get_player_config("unknown")

    assert config.player_id == DEFAULT_PLAYER_TYPE
    assert config.display_name == "Mustapha"


def test_player_factory_builds_default_player_runtime_groups(monkeypatch):
    monkeypatch.setattr(
        "game.controllers.frame_animation_controller.load_frame_animation",
        fake_frame_animation,
    )

    player = PlayerFactory.create_player()

    # State and input
    assert player.state == PlayerState.IDLE
    assert player.air is not None
    assert player.state_machine is not None
    assert player.intent is not None
    assert player.input_buffer is not None
    assert player.input_state is not None

    # Capabilities
    assert player.health is not None
    assert player.movement is not None
    assert player.movement.run.run_attack_min_distance == get_player_config(
        DEFAULT_PLAYER_TYPE
    ).run_attack_min_distance
    assert player.weapon_slot is not None
    assert player.events is not None
    assert player.geometry is not None
    assert player.geometry.collision_box_w == get_player_config(DEFAULT_PLAYER_TYPE).collision_box_w
    assert player.geometry.hurt_box_w == get_player_config(DEFAULT_PLAYER_TYPE).hurt_box_w

    # Controllers
    assert player.combat_controller is not None
    assert player.action_controller is not None
    assert player.grab_controller is not None
    assert player.state_controller is not None
    assert player.lifecycle_controller is not None

    # Presentation
    assert player.animation_controller is not None
    assert player.renderer is not None
