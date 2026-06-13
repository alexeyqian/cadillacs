from game.animation.ferris_data import *
from game.entities.frame_data_enemy import FrameDataEnemy

class FerrisEnemy(FrameDataEnemy):
    def __init__(self, x, y):
        super().__init__(x, y, enemy_type="ferris",
                animation_data=FERRIS_ANIMATIONS,
                anim_fps=FERRIS_ANIM_FPS,
                sprite_scale=4)
