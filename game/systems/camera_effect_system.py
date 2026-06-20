def heavy_hit_shake(game_state):

    game_state.camera.shake(
        strength=6,
        duration=8
    )


def explosion_shake(game_state):

    game_state.camera.shake(
        strength=12,
        duration=15
    )
