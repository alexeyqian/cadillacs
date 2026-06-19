from game.entities.entity import Entity
from game.entities.game_object import GameObject


def test_game_object_stores_basic_world_fields():
    obj = GameObject(10, 20, 30, 40)

    assert obj.x == 10
    assert obj.y == 20
    assert obj.width == 30
    assert obj.height == 40
    assert obj.active is True
    assert obj.visible is True


def test_entity_import_remains_compatible():
    obj = Entity(10, 20)

    assert isinstance(obj, GameObject)
    assert obj.x == 10
    assert obj.y == 20
    assert obj.width == 0
    assert obj.height == 0
