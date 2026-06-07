from game.settings import *

def apply_arena_bounds(game_state):
    level = game_state.level
    player = game_state.player

    if not level.camera_locked:
        return

    # should move to player's own update() function
    # prevent player escaping arena
    left_wall = level.lock_x
    right_wall = level.lock_x + SCREEN_WIDTH # - player.width
    clamp_entity(game_state.player, left_wall, right_wall)
    # prevent enemy escaping arena
    for enemy in game_state.enemies:
        clamp_entity(enemy, left_wall, right_wall)

def clamp_entity(entity, left_wall, right_wall):
    if entity.x < left_wall:
        entity.x = left_wall

    if entity.x + entity.width > right_wall:
        entity.x = right_wall - entity.width