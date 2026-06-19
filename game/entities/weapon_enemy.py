from game.entities.enemy import Enemy
from game.data.enemy_config import get_enemy_config


class WeaponEnemy(Enemy):
    def __init__(self, x, y, enemy_type="blade"):
        super().__init__(x, y, enemy_config=get_enemy_config(enemy_type))
