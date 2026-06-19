from game.animation.gneiss_data import GNEISS_ANIMATIONS, GNEISS_ANIM_FPS
from game.entities.enemy import Enemy

class GneissEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, enemy_type="gneiss",
                animation_data=GNEISS_ANIMATIONS,
                anim_fps=GNEISS_ANIM_FPS,
                sprite_scale=4)
