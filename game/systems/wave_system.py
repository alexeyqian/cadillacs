from game.level.wave import SpawnWave

def update_wave_system(game_state):
    level = game_state.level
    player = game_state.player
    camera = game_state.camera
    enemies = game_state.enemies

    wave = level.get_current_wave()

    if wave and not wave.started and player.x >= wave.trigger_x:
            # start the wave and initialize pending enemies
            wave.spawn()
            # lock camera only when wave actually starts
            # set lock_x to current camera.x so the viewport does not jump
            level.camera_locked = True
            level.lock_x = camera.x

    if wave and wave.started:
        # for normal Wave and BossWave
        if hasattr(wave, "update_spawn"):
            new_enemies = wave.update_spawn()
            if new_enemies:
                enemies.extend(new_enemies)
        # only for SpawnWave
        if hasattr(wave, "update"):
            enemies.extend(wave.update())