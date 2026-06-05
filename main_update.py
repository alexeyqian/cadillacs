import pygame
from game.settings import *
from game.systems.projectile_system import *

def main_update(game_state):
    screen = game_state.screen
    camera = game_state.camera
    level = game_state.level
    player = game_state.player
    enemies = game_state.enemies
    weapons = game_state.weapons
    projectiles = game_state.projectiles
    enemy_projectiles = game_state.enemy_projectiles
    objects = game_state.objects
    loot_items = game_state.loot_items
    hit_sparks = game_state.hit_sparks

    # update player
    player.update()
    collect_player_projectiles(game_state)

    # should move to player's own update() function
    # prevent escaping arena
    if level.camera_locked:
        left_wall = level.lock_x
        right_wall = level.lock_x + SCREEN_WIDTH - player.width
        if player.x < left_wall:
            player.x = left_wall
        if player.x > right_wall:
            player.x = right_wall

    # update enemies
    for enemy in enemies:
        enemy.update(player, enemies)
        collect_enemy_projectile(game_state, enemy)

    update_projectiles(game_state)
        
    # update hit sparks
    for spark in hit_sparks:
        spark.update()

    # update camera
    if level.camera_locked:
        camera.update(player, level.lock_x)
    else:
        camera.update(player)
