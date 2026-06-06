from game.systems.explosive_system import update_explosions

def update_effect_system(game_state):
    for spark in game_state.hit_sparks:
        spark.update()
    for text in game_state.floating_texts:
        text.update()
    update_explosions(game_state)