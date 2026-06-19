from game.systems.bounds_system import apply_level_bounds
from game.systems.projectile_system import collect_enemy_projectile

def update_enemy_system(game_state):
    player = game_state.player

    for enemy in game_state.enemies:
        enemy.update(game_state.level, player, game_state.enemies)
        apply_level_bounds(enemy, game_state.level)

        collect_enemy_projectile(game_state, enemy)
