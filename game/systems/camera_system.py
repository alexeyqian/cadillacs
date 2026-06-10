from game.settings import PLAYER_SCREEN_EDGE_MARGIN, SCREEN_WIDTH

def update_camera_system(game_state):
    level = game_state.level
    camera = game_state.camera
    player = game_state.player
    
    if level.camera_locked:
        camera.update(player, level.world_width, level.lock_x)
    else:
        camera.update(player, level.world_width)
        keep_player_inside_camera_view(player, camera)

def keep_player_inside_camera_view(player, camera):
    left_limit = camera.x
    right_limit = camera.x + SCREEN_WIDTH - player.width - PLAYER_SCREEN_EDGE_MARGIN

    if player.x < left_limit:
        player.x = left_limit
    if player.x > right_limit:
        player.x = right_limit
