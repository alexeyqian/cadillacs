from game.animation.mustapha_data import MUSTAPHA_ANIMATIONS, MUSTAPHA_ANIM_FPS
from game.entities.player import Player


class MustaphaPlayer(Player):
    def __init__(self):
        super().__init__(
            player_type="mustapha",
            animation_data=MUSTAPHA_ANIMATIONS,
            anim_fps=MUSTAPHA_ANIM_FPS,
        )
