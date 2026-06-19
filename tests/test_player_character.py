from game.entities.character import Character
from game.entities.player import Player


def test_player_inherits_from_character():
    assert issubclass(Player, Character)
