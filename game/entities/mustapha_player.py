from game.animation.mustapha_data import MUSTAPHA_ANIMATIONS
from game.entities.player import Player


class MustaphaPlayer(Player):
    def __init__(self):
        super().__init__(
            player_type="mustapha",
            animation_data=MUSTAPHA_ANIMATIONS,
        )
