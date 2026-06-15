import pygame
from game.colors import *
from game.effects.hit_spark import HitSpark
from game.effects.floating_text import FloatingText
from game.systems.camera_effect_system import *
from game.entities.boss_enemy import BossEnemy

def create_hit_spark(game_state, attack_rect, hurt_rect, facing_right=True):
    if facing_right:
        spark_x = attack_rect.right
    else:
        spark_x = attack_rect.left
    spark_y = attack_rect.top
    game_state.hit_sparks.append(HitSpark(spark_x, spark_y))

# todo: refactoring to be easy to understand and maintainable
def handle_player_attack_collision(game_state):
    player = game_state.player
    enemies = game_state.enemies
    objects = game_state.objects

    attack_rect = player.get_attack_rect()
    if not attack_rect:
        return
    if player.combat.already_hit_enemy:
        return

    if player.state == player.GRAB_KNEE:
        enemy = player.grab.grabbed_enemy
        if enemy and enemy.state != enemy.DEAD:
            damage = player.combat.attack_damage(player)
            enemy.take_grab_knee_damage(damage)
            enemy_rect = enemy.get_logical_rect()
            game_state.floating_texts.append(
                FloatingText(enemy_rect.centerx, enemy_rect.top - 10, str(damage), YELLOW_COLOR)
            )
            game_state.score_manager.register_hit()
            player.combat.already_hit_enemy = True
            if enemy.state == enemy.DEAD:
                player.grab.grabbed_enemy = None
        return


    # attack enemies
    for enemy in enemies:
        # add a simple clash/parry when player and enemy attack boxes collide.
        # if the player’s fist meets the enemy’s active fist, nobody takes damage. Both attacks cancel. 
        # It prevents the player from always winning by punching into enemy attack frames.
        enemy_attack_rect = enemy.get_attack_rect()
        if enemy.state == enemy.ATTACK and enemy_attack_rect:
            if attack_rect.colliderect(enemy_attack_rect):
                player.combat.cancel_attack()
                if player.state != player.DEAD:
                    player.state_machine.change_to(player, player.IDLE)
                enemy.state = enemy.PATROL
                enemy.attack_has_hit = False
                enemy.attack_cooldown = max(enemy.attack_cooldown, 20)
                create_hit_spark(game_state, attack_rect, enemy_attack_rect, player.facing_right)
                return

        enemy_hurt_rect = enemy.get_hurt_rect()
        if enemy_hurt_rect and attack_rect.colliderect(enemy_hurt_rect):
            damage = player.combat.attack_damage(player)
            enemy.take_damage(damage, player.x)
            enemy_rect = enemy.get_logical_rect()
            game_state.floating_texts.append(FloatingText(enemy_rect.centerx, enemy_rect.top - 10, str(damage), (255,80,80)))
            game_state.score_manager.register_hit() # for combo score
            player.combat.already_hit_enemy = True
            if enemy.health.hp >0 and enemy.health.max_hp >= 200:
                heavy_hit_shake(game_state)
            if isinstance(enemies, BossEnemy):
                boss_hit_shake(game_state)
            enemy_rect = enemy.get_hurt_rect()
            create_hit_spark(game_state, attack_rect, enemy_rect, player.facing_right)
            break # ?? useless, only can attack one enemy at a time?

    # attack breakables
    for obj in objects:
        if obj.destroyed:
            continue
        if attack_rect.colliderect(obj.get_rect()):
            obj.take_damage(player.combat.attack_damage(player))
            
def handle_player_projectile_collision(game_state):
    player = game_state.player
    enemies = game_state.enemies
    objects = game_state.objects
    projectiles = game_state.projectiles

    for projectile in projectiles:
        if not projectile.active:
            continue

        projectile_rect = projectile.get_rect()
        # projectile hit enemy
        for enemy in enemies:
            enemy_hurt_rect = enemy.get_hurt_rect()
            if enemy_hurt_rect and projectile_rect.colliderect(enemy_hurt_rect):
                damage = projectile.damage
                enemy.take_damage(damage, player.x)
                enemy_rect = enemy.get_logical_rect()
                game_state.floating_texts.append(FloatingText(enemy_rect.centerx, enemy_rect.top - 10, str(damage), (255,120,120)))
                game_state.score_manager.register_hit() # for combo score
                projectile.active = False
                create_hit_spark(
                    game_state,
                    projectile_rect,
                    enemy_hurt_rect,
                    projectile.direction > 0,
                )
                break

        # projectile hit breakable
        for obj in objects:
            if obj.destroyed:
                continue

            if projectile_rect.colliderect(obj.get_rect()):
                obj.take_damage(projectile.damage)
                projectile.active = False
                break

def handle_player_grab_or_throw(game_state, keys):
    player = game_state.player

    if keys[pygame.K_l]:
        if player.grab.grab_pressed:
            return
        player.grab.grab_pressed = True

        if player.grab.grabbed_enemy:
            player.grab.throw_grabbed_enemy(player)
            return
        
        for enemy in game_state.enemies:
            if player.grab.can_grab_enemy(player, enemy):
                player.grab.grab_enemy(player, enemy)
                break
    else:
        player.grab.grab_pressed = False

def handle_player_thrown_enemy_collision(game_state):
    for thrown_enemy in game_state.enemies:
        if thrown_enemy.state != thrown_enemy.THROWN:
            continue
        thrown_rect = thrown_enemy.get_logical_rect()
        for enemy in game_state.enemies:
            if enemy is thrown_enemy:
                continue
            if enemy.state == enemy.DEAD:
                continue
            # avoid process already hitted enemies because of thrown
            if id(enemy) in thrown_enemy.thrown_hit_targets:
                continue

            enemy_hurt_rect = enemy.get_hurt_rect()
            if thrown_rect.colliderect(enemy_hurt_rect):
                damage = enemy.thrown_damage
                enemy.lifecycle.take_damage(damage, thrown_enemy.x)
                enemy_rect = enemy.get_logical_rect()
                game_state.floating_texts.append(FloatingText(enemy_rect.centerx, enemy_rect.top - 10, str(damage), (255,150,0)))
                thrown_enemy.thrown_hit_targets.add(id(enemy))
