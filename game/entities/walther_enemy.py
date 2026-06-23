from game.animation.walther_data import WALTHER_ANIMATIONS
from game.entities.enemy import Enemy

class WaltherEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, enemy_type="walther",
                animation_data=WALTHER_ANIMATIONS,
                sprite_scale=4)
