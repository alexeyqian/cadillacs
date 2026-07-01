from game.systems.explosive_system import update_explosions

def update_effect_system(game_state):
    for spark in game_state.hit_sparks:
        spark.update()
    # todo: move to combat?
    update_explosions(game_state)