from game.data.enemy_config import DEFAULT_ENEMY_TYPE, get_enemy_config
from game.factories.enemy_factory import EnemyFactory
from game.entities.ferris_enemy import FerrisEnemy
from game.entities.raptor_enemy import RaptorEnemy


class FakeEnemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y


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


def test_enemy_factory_registers_raptor_enemy_type():
    assert EnemyFactory.get_enemy_class("raptor") is RaptorEnemy
    assert "raptor" in EnemyFactory.registered_enemy_types()


def test_enemy_config_has_raptor_data_and_default_fallback():
    raptor_config = get_enemy_config("raptor")
    fallback_config = get_enemy_config("unknown")

    assert raptor_config.enemy_id == "raptor"
    assert raptor_config.display_name == "Raptor"
    assert raptor_config.archetype == "leaper"
    assert fallback_config.enemy_id == DEFAULT_ENEMY_TYPE
