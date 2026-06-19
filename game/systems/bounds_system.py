def apply_level_bounds(character, level):
    character.apply_world_bounds(
        level.world_width,
        level.lane_top,
        level.lane_bottom,
    )


def apply_enemy_level_bounds(game_state):
    for enemy in game_state.enemies:
        apply_level_bounds(enemy, game_state.level)


def apply_player_level_bounds(game_state):
    apply_level_bounds(game_state.player, game_state.level)
