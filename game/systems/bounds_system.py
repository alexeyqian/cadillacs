from game.settings import SCREEN_WIDTH, PLAYER_SCREEN_EDGE_MARGIN


class BoundsSystem:
    @staticmethod
    def apply_player_level(game_state):
        _apply_level_bounds(game_state.player, game_state.level)

    @staticmethod
    def apply_enemy_level(game_state):
        for enemy in game_state.enemies:
            _apply_level_bounds(enemy, game_state.level)

    @staticmethod
    def apply_player_camera(game_state):
        player = game_state.player
        camera_x = game_state.camera.x
        half_w = player.width // 2
        margin = PLAYER_SCREEN_EDGE_MARGIN
        player.x = max(camera_x + half_w + margin,
                       min(player.x, camera_x + SCREEN_WIDTH - half_w - margin))


def _apply_level_bounds(character, level):
    character.apply_world_bounds(level.world_width, level.lane_top, level.lane_bottom)
