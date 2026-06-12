from game.entities.enemy import Enemy
from game.entities.enemy_config import get_enemy_config


class BasicMeleeEnemy(Enemy):
    def __init__(self, x, y, enemy_type="normal"):
        super().__init__(
            x,
            y,
            enemy_config=get_enemy_config(enemy_type),
        )
