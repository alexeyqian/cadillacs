from game.animation.walther_data import WALTHER_ANIMATIONS, WALTHER_ANIM_FPS
from game.entities.enemy import Enemy

class WaltherEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, enemy_type="walther",
                animation_data=WALTHER_ANIMATIONS,
                anim_fps=WALTHER_ANIM_FPS,
                sprite_scale=4)
