from game.level.walkable_area import *
from game.systems.projectile_system import collect_enemy_projectile

def update_enemy_system(game_state):
    player = game_state.player

    for enemy in game_state.enemies:
        old_x = enemy.x
        old_y = enemy.y

        enemy.update(player, game_state.enemies)
        enemy.apply_world_bounds(
            game_state.level.world_width,
            game_state.level.lane_top,
            game_state.level.lane_bottom
        )
        
        if not entity_is_inside_walkable_area(enemy, game_state.level):
            enemy.x = old_x
            enemy.y = old_y
        collect_enemy_projectile(game_state, enemy)