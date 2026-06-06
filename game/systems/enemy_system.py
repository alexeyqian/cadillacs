from game.systems.projectile_system import collect_enemy_projectile

def update_enemy_system(game_state):
    player = game_state.player

    for enemy in game_state.enemies:
        enemy.update(player, game_state.enemies)
        collect_enemy_projectile(game_state, enemy)