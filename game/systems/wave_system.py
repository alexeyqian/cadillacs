from game.level.wave import SpawnWave

def update_wave_system(game_state):
    level = game_state.level
    player = game_state.player
    
    wave = level.get_current_wave()
    