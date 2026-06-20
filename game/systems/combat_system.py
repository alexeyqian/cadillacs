import pygame
from game.colors import ORANGE_COLOR, WHITE_COLOR, YELLOW_COLOR
from game.effects.hit_spark import HitSpark
from game.effects.floating_text import FloatingText
from game.systems.camera_effect_system import heavy_hit_shake
from game.combat.damage_request import DamageRequest

def _create_hit_spark(game_state, attack_rect, hurt_rect, facing_right=True, color=YELLOW_COLOR):
    if facing_right:
        spark_x = attack_rect.right
    else:
        spark_x = attack_rect.left
    spark_y = attack_rect.top
    game_state.hit_sparks.append(HitSpark(spark_x, spark_y, color))

def damage_enemy(enemy, damage, attacker_x=None, hit_reaction=None):
    if isinstance(damage, DamageRequest):
        request = damage
    else:
        request = DamageRequest(damage, attacker_x, hit_reaction)

    if request.reaction is None:
        enemy.take_damage(request.damage, request.attacker_x)
        return

    enemy.take_damage(request.damage, request.attacker_x, reaction=request.reaction)


def handle_player_attack_collision(game_state):
    player = game_state.player
    attack_rect = player.get_attack_rect()
    if not attack_rect:
        return
    if not player.combat_controller.can_hit_more_targets():
        return

    if player.state == player.GRAB_KNEE:
        _handle_grab_knee_collision(game_state)
        return

    _handle_player_melee_enemy_collision(game_state, attack_rect)
    _handle_player_breakable_collision(game_state, attack_rect)


def _handle_grab_knee_collision(game_state):
    player = game_state.player
    enemy = player.grab_controller.grabbed_enemy
    if not enemy or enemy.state == enemy.DEAD:
        return
    if not player.combat_controller.can_hit_target(enemy):
        return

    damage = player.combat_controller.attack_result.get_damage(player)
    enemy.take_grab_knee_damage(damage)
    enemy_rect = enemy.get_frame_rect()
    game_state.floating_texts.append(
        FloatingText(enemy_rect.centerx, enemy_rect.top - 10, str(int(damage)), YELLOW_COLOR)
    )
    game_state.score_manager.register_hit()
    player.combat_controller.mark_attack_hit(enemy)
    if enemy.state == enemy.DEAD:
        player.grab_controller.grabbed_enemy = None


def _handle_player_melee_enemy_collision(game_state, attack_rect):
    player = game_state.player
    lane_reach = player.combat_controller.attack_result.get_lane_reach(player)

    for enemy in game_state.enemies:
        if not player.combat_controller.can_hit_target(enemy):
            continue

        # CLASH BLOCK
        # add a simple clash/parry when player and enemy attack boxes collide.
        # if the player’s fist meets the enemy’s active fist, nobody takes damage. Both attacks cancel. 
        # It prevents the player from always winning by punching into enemy attack frames.
        enemy_attack_rect = enemy.get_attack_rect()
        if enemy.state == enemy.ATTACK and enemy_attack_rect:
            if _player_attack_clashes_with_enemy(
                game_state,
                enemy,
                attack_rect,
                enemy_attack_rect,
                lane_reach,
            ):
                # Expected behavior
                # Clash -> player gets 8 frames recovery
                # Clash -> enemy gets 12 frames recovery
                # Both sides separate mentally for a beat
                # No one takes damage
                player.combat_controller.start_clash_recovery(player)
                enemy.combat_controller.start_clash_recovery(enemy)
                _create_hit_spark(game_state, attack_rect, enemy_attack_rect, player.facing_right, YELLOW_COLOR)
                # used for debug
                game_state.floating_texts.append(
                    FloatingText(attack_rect.centerx,
                        attack_rect.top - 18,
                        "CLASH", YELLOW_COLOR))
                return

        # NORMAL DAMAGE BLOCK
        if _damage_enemy_with_player_attack(game_state, enemy, attack_rect, lane_reach):
            if not player.combat_controller.can_hit_more_targets():
                break


def _player_attack_clashes_with_enemy(
    game_state,
    enemy,
    attack_rect,
    enemy_attack_rect,
    player_lane_reach,
):
    player = game_state.player
    lane_distance = game_state.level.get_lane_distance(player.y, enemy.y)
    clash_lane_reach = max(
        player_lane_reach,
        enemy.combat_controller.get_attack_data(enemy).lane_reach,
    )
    return (
        lane_distance <= clash_lane_reach
        and enemy.combat_controller.is_attack_active(enemy)
        and attack_rect.colliderect(enemy_attack_rect)
    )


def _damage_enemy_with_player_attack(game_state, enemy, attack_rect, lane_reach):
    player = game_state.player
    lane_distance = game_state.level.get_lane_distance(player.y, enemy.y)
    if lane_distance > lane_reach:
        return False

    enemy_hurt_rect = enemy.get_hurt_rect()
    if not enemy_hurt_rect or not attack_rect.colliderect(enemy_hurt_rect):
        return False

    damage = player.combat_controller.attack_result.get_damage(player)
    hit_reaction = player.combat_controller.attack_result.get_hit_reaction(player)
    damage_enemy(enemy, damage, player.x, hit_reaction)
    enemy_rect = enemy.get_frame_rect()
    game_state.floating_texts.append(
        FloatingText(enemy_rect.centerx, enemy_rect.top - 10, str(int(damage)), (255, 80, 80))
    )
    game_state.score_manager.register_hit() # for combo score
    player.combat_controller.mark_attack_hit(enemy)
    if enemy.health.hp > 0 and enemy.health.max_hp >= 200:
        heavy_hit_shake(game_state)
    enemy_rect = enemy.get_hurt_rect()
    _create_hit_spark(game_state, attack_rect, enemy_rect, player.facing_right, WHITE_COLOR)
    return True


def _handle_player_breakable_collision(game_state, attack_rect):
    player = game_state.player

    for obj in game_state.objects:
        if not player.combat_controller.can_hit_target(obj):
            continue
        if obj.destroyed:
            continue
        if attack_rect.colliderect(obj.get_rect()):
            obj.take_damage(player.combat_controller.attack_result.get_damage(player))
            player.combat_controller.mark_attack_hit(obj)
            if not player.combat_controller.can_hit_more_targets():
                break

def handle_player_projectile_collision(game_state):
    for projectile in game_state.projectiles:
        if not projectile.active:
            continue

        projectile_rect = projectile.get_rect()
        if _damage_enemy_with_player_projectile(game_state, projectile, projectile_rect):
            continue

        _damage_object_with_player_projectile(game_state, projectile, projectile_rect)


def _damage_enemy_with_player_projectile(game_state, projectile, projectile_rect):
    player = game_state.player
    for enemy in game_state.enemies:
        # So player bullets hit same-lane enemies only.
        lane_distance = game_state.level.get_lane_distance(projectile.lane_y, enemy.y)
        if lane_distance > projectile.lane_reach:
            continue

        enemy_hurt_rect = enemy.get_hurt_rect()
        if not enemy_hurt_rect or not projectile_rect.colliderect(enemy_hurt_rect):
            continue

        damage_enemy(enemy, projectile.damage, player.x)
        enemy_rect = enemy.get_frame_rect()
        game_state.floating_texts.append(
            FloatingText(enemy_rect.centerx, enemy_rect.top - 10, str(int(projectile.damage)), (255, 120, 120))
        )
        game_state.score_manager.register_hit() # for combo score
        projectile.active = False
        _create_hit_spark(
            game_state,
            projectile_rect,
            enemy_hurt_rect,
            projectile.direction > 0,
        )
        return True

    return False


def _damage_object_with_player_projectile(game_state, projectile, projectile_rect):
    for obj in game_state.objects:
        if obj.destroyed:
            continue

        if projectile_rect.colliderect(obj.get_rect()):
            obj.take_damage(projectile.damage)
            projectile.active = False
            return True

    return False

def handle_player_grab_or_throw(game_state, keys):
    player = game_state.player

    if keys[pygame.K_l]:
        if player.grab_controller.grab_pressed:
            return
        player.grab_controller.grab_pressed = True

        if player.grab_controller.grabbed_enemy:
            player.grab_controller.throw_grabbed_enemy(player)
            return
        
        for enemy in game_state.enemies:
            if player.grab_controller.can_grab_enemy(player, enemy, game_state.level):
                player.grab_controller.grab_enemy(player, enemy)
                break
    else:
        player.grab_controller.grab_pressed = False
    
    # add visual feedback for failed grab
    if player.grab_controller.failed_grab_feedback:
        game_state.floating_texts.append(
            FloatingText(player.x, player.y - 160,
                "NO GRAB", ORANGE_COLOR))
        player.grab_controller.failed_grab_feedback = False

def handle_player_thrown_enemy_collision(game_state):
    for thrown_enemy in game_state.enemies:
        if thrown_enemy.state != thrown_enemy.THROWN:
            continue
        thrown_rect = thrown_enemy.get_frame_rect()
        for enemy in game_state.enemies:
            if enemy is thrown_enemy:
                continue
            if enemy.state == enemy.DEAD:
                continue
            # avoid process already hit enemies because of thrown
            if thrown_enemy.life_cycle.has_thrown_hit(enemy):
                continue
            # throw collision only hits enemies in the same lane for now.
            lane_distance = game_state.level.get_lane_distance(thrown_enemy.y, enemy.y)
            if lane_distance > 0:
                continue

            enemy_hurt_rect = enemy.get_hurt_rect()
            if thrown_rect.colliderect(enemy_hurt_rect):
                damage = thrown_enemy.life_cycle.throw_damage
                damage_enemy(enemy, damage, thrown_enemy.x)
                enemy_rect = enemy.get_frame_rect()
                game_state.floating_texts.append(FloatingText(enemy_rect.centerx, enemy_rect.top - 10, str(int(damage)), (255,150,0)))
                thrown_enemy.life_cycle.mark_thrown_hit(enemy)

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
