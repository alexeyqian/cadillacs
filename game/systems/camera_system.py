def update_camera_system(game_state):
    level = game_state.level
    camera = game_state.camera
    player = game_state.player
    
    if level.camera_locked:
        camera.update(player, level.lock_x)
    else:
        camera.update(player)