from game.settings import *

def apply_arena_bounds(game_state):
    level = game_state.level
    if not level.camera_locked:
        return
    if level.lock_x is None:
        return

    # should move to player's own update() function
    # prevent player escaping arena
    arena_left = level.lock_x
    arena_right = level.lock_x + SCREEN_WIDTH
    clamp_entity(game_state.player, arena_left, arena_right)
    # prevent enemy escaping arena
    for enemy in game_state.enemies:
        if enemy.state == enemy.DEAD:
            continue
        clamp_entity(enemy, arena_left, arena_right)

def clamp_entity(entity, arena_left, arena_right):
    half_w = entity.width // 2
    if entity.x - half_w < arena_left:
        entity.x = arena_left + half_w

    if entity.x + half_w > arena_right:
        entity.x = arena_right - half_w