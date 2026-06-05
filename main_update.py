import pygame
from game.settings import *

def main_update(screen, camera, level, player, enemies, 
                    weapons, projectiles, enemy_projectiles, objects, loot_items):
    # update player
    player.update()
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
        if hasattr(enemy, "pending_projectile"):
            if enemy.pending_projectile:
                enemy_projectiles.append(enemy.pending_projectile)
                enemy.pending_projectile = None

    # update player projectiles
    for projectile in projectiles:
        projectile.update()

    # update enemy projectiles
    for projectile in enemy_projectiles:
        projectile.update()

    # update camera
    if level.camera_locked:
        camera.update(player, level.lock_x)
    else:
        camera.update(player)
