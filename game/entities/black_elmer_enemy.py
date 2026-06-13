from game.animation.black_elmer_data import *
from game.entities.frame_data_enemy import FrameDataEnemy

class BlackElmerEnemy(FrameDataEnemy):
    def __init__(self, x, y):
        super().__init__(x, y, enemy_type="black_elmer",
                animation_data=BLACK_ELMER_ANIMATIONS,
                anim_fps=BLACK_ELMER_ANIM_FPS,
                sprite_scale=4,
                attack_timing=BLACK_ELMER_ATTACK_TIMING)
