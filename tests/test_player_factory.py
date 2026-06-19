from game.entities.mustapha_player import MustaphaPlayer
from game.entities.player_config import DEFAULT_PLAYER_TYPE, get_player_config
from game.entities.player_factory import PlayerFactory


class FakePlayer:
    pass


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
