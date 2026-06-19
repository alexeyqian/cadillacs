from game.entities.mustapha_player import MustaphaPlayer
from game.data.player_config import DEFAULT_PLAYER_TYPE


class PlayerFactory:
    player_classes = {
        "mustapha": MustaphaPlayer,
    }

    @staticmethod
    def create_player(player_type=DEFAULT_PLAYER_TYPE):
        player_class = PlayerFactory.get_player_class(player_type)
        return player_class()

    @staticmethod
    def get_player_class(player_type):
        return PlayerFactory.player_classes.get(
            player_type,
            PlayerFactory.player_classes[DEFAULT_PLAYER_TYPE],
        )

    @staticmethod
    def register_player_type(player_type, player_class):
        PlayerFactory.player_classes[player_type] = player_class

    @staticmethod
    def registered_player_types():
        return tuple(PlayerFactory.player_classes.keys())
