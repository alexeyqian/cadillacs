import pygame
from game.colors import ORANGE_COLOR, WHITE_COLOR, YELLOW_COLOR
from game.effects.hit_spark import HitSpark
from game.effects.floating_text import FloatingText
from game.systems.camera_effect_system import CameraEffectSystem
from game.combat.damage_request import DamageRequest


class CombatSystem:
    @staticmethod
    def damage_enemy(enemy, damage, attacker_x=None, hit_reaction=None):
        if isinstance(damage, DamageRequest):
            request = damage
        else:
            request = DamageRequest(damage, attacker_x, hit_reaction)
        if request.reaction is None:
            enemy.take_damage(request.damage, request.attacker_x)
        else:
            enemy.take_damage(request.damage, request.attacker_x, reaction=request.reaction)

    @staticmethod
    def handle_player_attack(game_state):
        player = game_state.player
        attack_rect = player.get_attack_rect()
        if not attack_rect:
            return
        if not player.combat_controller.can_hit_more_targets(player):
            return
        if player.state == player.GRAB_KNEE:
            _handle_grab_knee_attack(game_state)
            return
        _handle_player_melee_enemy_collision(game_state, attack_rect)
        _handle_player_breakable_collision(game_state, attack_rect)

    @staticmethod
    def handle_player_grab_or_throw(game_state, keys):
        player = game_state.player
        if keys[pygame.K_l]:
            if player.grab_state.grab_pressed:
                return
            player.grab_state.grab_pressed = True
            if player.grab_state.grabbed_enemy:
                player.grab_controller.throw_grabbed_enemy(player)
                return
            for enemy in game_state.enemies:
                if player.grab_controller.can_grab_enemy(player, enemy, game_state.level):
                    player.grab_controller.grab_enemy(player, enemy)
                    break
        else:
            player.grab_state.grab_pressed = False
        if player.grab_state.failed_grab_feedback:
            game_state.floating_texts.append(
                FloatingText(player.x, player.y - 160, "NO GRAB", ORANGE_COLOR))
            player.grab_state.failed_grab_feedback = False

    @staticmethod
    def handle_player_projectile(game_state):
        for projectile in game_state.projectiles:
            if not projectile.active:
                continue
            if _damage_enemy_with_player_projectile(game_state, projectile):
                continue
            _damage_object_with_player_projectile(game_state, projectile)

    @staticmethod
    def handle_enemy_projectile(game_state):
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

    @staticmethod
    def handle_player_thrown_enemy(game_state):
        for thrown_enemy in game_state.enemies:
            if thrown_enemy.state != thrown_enemy.THROWN:
                continue
            thrown_rect = thrown_enemy.get_frame_rect()
            for enemy in game_state.enemies:
                if enemy is thrown_enemy or enemy.state == enemy.DEAD:
                    continue
                if thrown_enemy.reaction_controller.has_thrown_hit(thrown_enemy, enemy):
                    continue
                if game_state.level.get_lane_distance(thrown_enemy.y, enemy.y) > 0:
                    continue
                enemy_hurt_rect = enemy.get_hurt_rect()
                if thrown_rect.colliderect(enemy_hurt_rect):
                    damage = thrown_enemy.reaction_state.throw_damage
                    CombatSystem.damage_enemy(enemy, damage, thrown_enemy.x)
                    game_state.floating_texts.append(
                        FloatingText(enemy.x, enemy.y - 10, str(int(damage)), (255, 150, 0)))
                    thrown_enemy.reaction_controller.mark_thrown_hit(thrown_enemy, enemy)


def _create_hit_spark(game_state, attack_rect, hurt_rect, facing_right=True, color=YELLOW_COLOR):
    spark_x = attack_rect.right if facing_right else attack_rect.left
    game_state.hit_sparks.append(HitSpark(spark_x, attack_rect.top, color))


def _handle_grab_knee_attack(game_state):
    player = game_state.player
    enemy = player.grab_state.grabbed_enemy
    if not enemy or enemy.state == enemy.DEAD:
        return
    if not player.combat_controller.can_hit_target(player, enemy):
        return
    damage = player.combat_controller.attack_result.get_damage(player)
    enemy.take_grab_knee_damage(damage)
    enemy_rect = enemy.get_frame_rect()
    game_state.floating_texts.append(
        FloatingText(enemy_rect.centerx, enemy_rect.top - 10, str(int(damage)), YELLOW_COLOR))
    game_state.score_manager.register_hit()
    player.combat_controller.mark_attack_hit(player, enemy)
    if enemy.state == enemy.DEAD:
        player.grab_state.grabbed_enemy = None


def _handle_player_melee_enemy_collision(game_state, attack_rect):
    player = game_state.player
    lane_reach = player.combat_controller.attack_result.get_lane_reach(player)
    for enemy in game_state.enemies:
        if not player.combat_controller.can_hit_target(player, enemy):
            continue
        enemy_attack_rect = enemy.get_attack_rect()
        if enemy.state == enemy.ATTACK and enemy_attack_rect:
            if _player_attack_clashes_with_enemy(game_state, enemy, attack_rect, enemy_attack_rect, lane_reach):
                player.combat_controller.start_clash_recovery(player)
                enemy.combat_controller.start_clash_recovery(enemy)
                _create_hit_spark(game_state, attack_rect, enemy_attack_rect, player.facing_right, YELLOW_COLOR)
                game_state.floating_texts.append(
                    FloatingText(attack_rect.centerx, attack_rect.top - 18, "CLASH", YELLOW_COLOR))
                return
        if _damage_enemy_with_player_attack(game_state, enemy, attack_rect, lane_reach):
            if not player.combat_controller.can_hit_more_targets(player):
                break


def _player_attack_clashes_with_enemy(game_state, enemy, attack_rect, enemy_attack_rect, player_lane_reach):
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
    if game_state.level.get_lane_distance(player.y, enemy.y) > lane_reach:
        return False
    enemy_hurt_rect = enemy.get_hurt_rect()
    if not enemy_hurt_rect or not attack_rect.colliderect(enemy_hurt_rect):
        return False
    damage = player.combat_controller.attack_result.get_damage(player)
    hit_reaction = player.combat_controller.attack_result.get_hit_reaction(player)
    CombatSystem.damage_enemy(enemy, damage, player.x, hit_reaction)
    enemy_rect = enemy.get_frame_rect()
    game_state.floating_texts.append(
        FloatingText(enemy_rect.centerx, enemy_rect.top - 10, str(int(damage)), (255, 80, 80)))
    game_state.score_manager.register_hit()
    player.combat_controller.mark_attack_hit(player, enemy)
    if enemy.health.hp > 0 and enemy.health.max_hp >= 200:
        CameraEffectSystem.heavy_hit_shake(game_state)
    _create_hit_spark(game_state, attack_rect, enemy.get_hurt_rect(), player.facing_right, WHITE_COLOR)
    return True


def _handle_player_breakable_collision(game_state, attack_rect):
    player = game_state.player
    for obj in game_state.objects:
        if not player.combat_controller.can_hit_target(player, obj):
            continue
        if obj.destroyed:
            continue
        if attack_rect.colliderect(obj.get_rect()):
            obj.take_damage(player.combat_controller.attack_result.get_damage(player))
            player.combat_controller.mark_attack_hit(player, obj)
            if not player.combat_controller.can_hit_more_targets(player):
                break


def _damage_enemy_with_player_projectile(game_state, projectile):
    player = game_state.player
    projectile_rect = projectile.get_rect()
    for enemy in game_state.enemies:
        if game_state.level.get_lane_distance(projectile.lane_y, enemy.y) > projectile.lane_reach:
            continue
        enemy_hurt_rect = enemy.get_hurt_rect()
        if not enemy_hurt_rect or not projectile_rect.colliderect(enemy_hurt_rect):
            continue
        CombatSystem.damage_enemy(enemy, projectile.damage, player.x)
        enemy_rect = enemy.get_frame_rect()
        game_state.floating_texts.append(
            FloatingText(enemy_rect.centerx, enemy_rect.top - 10, str(int(projectile.damage)), (255, 120, 120)))
        game_state.score_manager.register_hit()
        projectile.active = False
        _create_hit_spark(game_state, projectile_rect, enemy_hurt_rect, projectile.direction > 0)
        return True
    return False


def _damage_object_with_player_projectile(game_state, projectile):
    projectile_rect = projectile.get_rect()
    for obj in game_state.objects:
        if not obj.destroyed and projectile_rect.colliderect(obj.get_rect()):
            obj.take_damage(projectile.damage)
            projectile.active = False
            return True
    return False
