from game.entities.character import Character
from game.entities.player import Player


def test_player_inherits_from_character():
    assert issubclass(Player, Character)


def test_player_uses_character_shared_api_methods():
    assert Player.draw is Character.draw
    assert Player.apply_world_bounds is Character.apply_world_bounds
    assert Player.get_frame_rect is Character.get_frame_rect
    assert Player.get_collision_rect is Character.get_collision_rect
    assert Player.get_hurt_rect is Character.get_hurt_rect
    assert Player.get_attack_rect is Character.get_attack_rect
