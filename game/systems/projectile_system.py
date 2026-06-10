import pygame

def collect_player_projectiles(game_state):
    player = game_state.player
    projectiles = game_state.projectiles

    if player.pending_projectile:
        projectiles.append(player.pending_projectile)
        player.pending_projectile = None

def collect_enemy_projectile(game_state, enemy):
    if hasattr(enemy, "pending_projectile"):
        if enemy.pending_projectile:
            game_state.enemy_projectiles.append(enemy.pending_projectile)
            enemy.pending_projectile = None
        
def update_projectiles(game_state):
    # update player projectiles
    for projectile in game_state.projectiles:
        projectile.update(game_state.level.world_width)

    # update enemy projectiles
    for projectile in game_state.enemy_projectiles:
        projectile.update(game_state.level.world_width)

def handle_enemy_projectile_collision(game_state):
    player = game_state.player
    player_hurt_rect = player.get_hurt_rect()

    for projectile in game_state.enemy_projectiles:
        if not projectile.active:
            continue

        if projectile.get_rect().colliderect(player_hurt_rect):
            player.take_damage(projectile.damage)
            projectile.active = False
