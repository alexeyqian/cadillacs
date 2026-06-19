import pygame
from game.colors import *
from game.effects.hit_spark import HitSpark
from game.effects.floating_text import FloatingText
from game.systems.camera_effect_system import *

def create_hit_spark(game_state, attack_rect, hurt_rect, facing_right=True, color=YELLOW_COLOR):
    if facing_right:
        spark_x = attack_rect.right
    else:
        spark_x = attack_rect.left
    spark_y = attack_rect.top
    game_state.hit_sparks.append(HitSpark(spark_x, spark_y, color))

def get_enemy_frame_rect(enemy):
    if hasattr(enemy, "get_frame_rect"):
        return enemy.get_frame_rect()
    return enemy.get_logical_rect()


def damage_enemy(enemy, damage, attacker_x, hit_reaction=None):
    # Most production enemies now accept HitReaction. Some lightweight tests and
    # older enemy-like objects still expose the previous positional API.
    if hit_reaction is None:
        enemy.take_damage(damage, attacker_x)
        return

    try:
        enemy.take_damage(damage, attacker_x, reaction=hit_reaction)
    except TypeError:
        enemy.take_damage(
            damage,
            attacker_x,
            hit_reaction.knockback_velocity,
            hit_reaction.stun_frames,
        )


# todo: refactoring to be easy to understand and maintainable
def handle_player_attack_collision(game_state):
    player = game_state.player
    enemies = game_state.enemies
    objects = game_state.objects

    attack_rect = player.get_attack_rect()
    if not attack_rect:
        return
    if not player.combat.can_hit_more_targets():
        return

    player_attack_lane_reach = player.combat.get_attack_lane_reach(player)

    if player.state == player.GRAB_KNEE:
        enemy = player.grab.grabbed_enemy
        if enemy and enemy.state != enemy.DEAD and player.combat.can_hit_target(enemy):
            damage = player.combat.get_attack_damage(player)
            enemy.take_grab_knee_damage(damage)
            enemy_rect = get_enemy_frame_rect(enemy)
            game_state.floating_texts.append(
                FloatingText(enemy_rect.centerx, enemy_rect.top - 10, str(int(damage)), YELLOW_COLOR)
            )
            game_state.score_manager.register_hit()
            player.combat.mark_attack_hit(enemy)
            if enemy.state == enemy.DEAD:
                player.grab.grabbed_enemy = None
        return


    # attack enemies
    for enemy in enemies:
        if not player.combat.can_hit_target(enemy):
            continue

        # CLASH BLOCK
        # add a simple clash/parry when player and enemy attack boxes collide.
        # if the player’s fist meets the enemy’s active fist, nobody takes damage. Both attacks cancel. 
        # It prevents the player from always winning by punching into enemy attack frames.
        enemy_attack_rect = enemy.get_attack_rect()
        if enemy.state == enemy.ATTACK and enemy_attack_rect:
            lane_distance = game_state.level.get_lane_distance(player.y, enemy.y)
            clash_lane_reach = max(
                player_attack_lane_reach,
                enemy.combat.get_attack_data(enemy).lane_reach,
            )
            if (lane_distance <= clash_lane_reach
                and enemy.is_attack_active()
                and attack_rect.colliderect(enemy_attack_rect)):
                # Expected behavior
                # Clash -> player gets 8 frames recovery
                # Clash -> enemy gets 12 frames recovery
                # Both sides separate mentally for a beat
                # No one takes damage
                player.combat.start_clash_recovery(player)
                enemy.start_clash_recovery()
                create_hit_spark(game_state, attack_rect, enemy_attack_rect, player.facing_right, YELLOW_COLOR)
                # used for debug
                game_state.floating_texts.append(
                    FloatingText(attack_rect.centerx,
                        attack_rect.top - 18,
                        "CLASH", YELLOW_COLOR))
                return

        # NORMAL DAMAGE BLOCK
        lane_distance = game_state.level.get_lane_distance(player.y, enemy.y)
        if lane_distance > player_attack_lane_reach:
            continue
        enemy_hurt_rect = enemy.get_hurt_rect()
        if enemy_hurt_rect and attack_rect.colliderect(enemy_hurt_rect):
            damage = player.combat.get_attack_damage(player)
            hit_reaction = player.combat.get_attack_hit_reaction(player)
            damage_enemy(enemy, damage, player.x, hit_reaction)
            enemy_rect = get_enemy_frame_rect(enemy)
            game_state.floating_texts.append(FloatingText(enemy_rect.centerx, enemy_rect.top - 10, str(int(damage)), (255,80,80)))
            game_state.score_manager.register_hit() # for combo score
            player.combat.mark_attack_hit(enemy)
            if enemy.health.hp >0 and enemy.health.max_hp >= 200:
                heavy_hit_shake(game_state)
            enemy_rect = enemy.get_hurt_rect()
            create_hit_spark(game_state, attack_rect, enemy_rect, player.facing_right, WHITE_COLOR)
            if not player.combat.can_hit_more_targets():
                break

    # attack breakables
    for obj in objects:
        if not player.combat.can_hit_target(obj):
            continue
        if obj.destroyed:
            continue
        if attack_rect.colliderect(obj.get_rect()):
            obj.take_damage(player.combat.get_attack_damage(player))
            player.combat.mark_attack_hit(obj)
            if not player.combat.can_hit_more_targets():
                break

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
            # So player bullets hit same-lane enemies only.
            lane_distance = game_state.level.get_lane_distance(projectile.lane_y, enemy.y)
            if lane_distance > projectile.lane_reach:
                continue
            enemy_hurt_rect = enemy.get_hurt_rect()
            if enemy_hurt_rect and projectile_rect.colliderect(enemy_hurt_rect):
                damage = projectile.damage
                damage_enemy(enemy, damage, player.x)
                enemy_rect = get_enemy_frame_rect(enemy)
                game_state.floating_texts.append(FloatingText(enemy_rect.centerx, enemy_rect.top - 10, str(int(damage)), (255,120,120)))
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
            if player.grab.can_grab_enemy(player, enemy, game_state.level):
                player.grab.grab_enemy(player, enemy)
                break
    else:
        player.grab.grab_pressed = False
    
    # add visual feedback for failed grab
    if player.grab.failed_grab_feedback:
        game_state.floating_texts.append(
            FloatingText(player.x, player.y - 160,
                "NO GRAB", ORANGE_COLOR))
        player.grab.failed_grab_feedback = False

def handle_player_thrown_enemy_collision(game_state):
    for thrown_enemy in game_state.enemies:
        if thrown_enemy.state != thrown_enemy.THROWN:
            continue
        thrown_rect = get_enemy_frame_rect(thrown_enemy)
        for enemy in game_state.enemies:
            if enemy is thrown_enemy:
                continue
            if enemy.state == enemy.DEAD:
                continue
            # avoid process already hit enemies because of thrown
            thrown_hit_targets = (
                thrown_enemy.lifecycle_state.thrown_hit_targets
                if hasattr(thrown_enemy, "lifecycle_state")
                else thrown_enemy.thrown_hit_targets
            )
            if id(enemy) in thrown_hit_targets:
                continue
            # throw collision only hits enemies in the same lane for now.
            lane_distance = game_state.level.get_lane_distance(thrown_enemy.y, enemy.y)
            if lane_distance > 0:
                continue

            enemy_hurt_rect = enemy.get_hurt_rect()
            if thrown_rect.colliderect(enemy_hurt_rect):
                damage = (
                    thrown_enemy.lifecycle_state.throw_damage
                    if hasattr(thrown_enemy, "lifecycle_state")
                    else getattr(thrown_enemy, "throw_damage", 0)
                )
                damage_enemy(enemy, damage, thrown_enemy.x)
                enemy_rect = get_enemy_frame_rect(enemy)
                game_state.floating_texts.append(FloatingText(enemy_rect.centerx, enemy_rect.top - 10, str(int(damage)), (255,150,0)))
                thrown_hit_targets.add(id(enemy))

def handle_enemy_projectile_collision(game_state):
    player = game_state.player
    player_hurt_rect = player.get_hurt_rect()

    for projectile in game_state.enemy_projectiles:
        if not projectile.active:
            continue

        lane_distance = game_state.level.get_lane_distance(projectile.lane_y, player.y)
        if lane_distance > projectile.lane_reach:
            continue

        if projectile.get_rect().colliderect(player_hurt_rect):
            player.take_damage(projectile.damage)
            projectile.active = False
