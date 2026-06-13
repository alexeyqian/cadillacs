from game.animation.gneiss_data import *
from game.entities.frame_data_enemy import FrameDataEnemy

class GneissEnemy(FrameDataEnemy):
    def __init__(self, x, y):
        super().__init__(x, y, enemy_type="gneiss",
                animation_data=GNEISS_ANIMATIONS,
                anim_fps=GNEISS_ANIM_FPS,
                sprite_scale=4)
