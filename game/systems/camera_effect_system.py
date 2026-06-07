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


def boss_hit_shake(game_state):

    game_state.camera.shake(
        strength=10,
        duration=10
    )


def boss_death_shake(game_state):

    game_state.camera.shake(
        strength=20,
        duration=30
    )