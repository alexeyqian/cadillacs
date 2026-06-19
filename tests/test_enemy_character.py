from game.entities.character import Character
from game.entities.enemy import Enemy


def test_enemy_inherits_from_character():
    assert issubclass(Enemy, Character)


def test_enemy_uses_character_shared_api_methods():
    assert Enemy.draw is Character.draw
    assert Enemy.apply_world_bounds is Character.apply_world_bounds
    assert Enemy.get_frame_rect is Character.get_frame_rect
    assert Enemy.get_collision_rect is Character.get_collision_rect
    assert Enemy.get_hurt_rect is Character.get_hurt_rect
    assert Enemy.get_attack_rect is Character.get_attack_rect
