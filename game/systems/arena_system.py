from game.settings import *

def apply_arena_bounds(game_state):
    level = game_state.level
    player = game_state.player
    
    if not level.camera_locked:
        return

    # should move to player's own update() function
    # prevent escaping arena
    left_wall = level.lock_x
    right_wall = level.lock_x + SCREEN_WIDTH - player.width
    if player.x < left_wall:
        player.x = left_wall
    if player.x > right_wall:
        player.x = right_wall