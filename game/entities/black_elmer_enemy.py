from game.animation.black_elmer_data import BLACK_ELMER_ANIMATIONS
from game.entities.enemy import Enemy

class BlackElmerEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, enemy_type="black_elmer",
                animation_data=BLACK_ELMER_ANIMATIONS,
                sprite_scale=4)
