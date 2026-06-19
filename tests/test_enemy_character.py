from game.entities.character import Character
from game.entities.enemy import Enemy


def test_enemy_inherits_from_character():
    assert issubclass(Enemy, Character)
