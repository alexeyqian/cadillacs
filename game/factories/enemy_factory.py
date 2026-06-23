from game.entities.ferris_enemy import FerrisEnemy
from game.entities.gneiss_enemy import GneissEnemy
from game.entities.blade_enemy import BladeEnemy
from game.entities.black_elmer_enemy import BlackElmerEnemy
from game.entities.walther_enemy import WaltherEnemy
from game.data.enemy_config import DEFAULT_ENEMY_TYPE

class EnemyFactory:
    enemy_classes = {
        "ferris": FerrisEnemy,
        "gneiss": GneissEnemy,
        "blade": BladeEnemy,
        "black_elmer": BlackElmerEnemy,
        "walther": WaltherEnemy,
    }

    @staticmethod
    def create_enemy(enemy_type, x, y, capability_overrides=None):
        enemy_class = EnemyFactory.get_enemy_class(enemy_type)
        enemy = enemy_class(x, y)
        if capability_overrides:
            enemy.apply_capability_overrides(capability_overrides)
        return enemy

    @staticmethod
    def get_enemy_class(enemy_type):
        return EnemyFactory.enemy_classes.get(
            enemy_type,
            EnemyFactory.enemy_classes[DEFAULT_ENEMY_TYPE],
        )

    @staticmethod
    def register_enemy_type(enemy_type, enemy_class):
        EnemyFactory.enemy_classes[enemy_type] = enemy_class

    @staticmethod
    def registered_enemy_types():
        return tuple(EnemyFactory.enemy_classes.keys())
