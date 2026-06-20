from game.input.player_input import PlayerInput
from game.systems.arena_system import apply_arena_bounds
from game.systems.bounds_system import apply_enemy_level_bounds, apply_player_level_bounds
from game.systems.cleanup_system import cleanup_game_state
from game.systems.collision_system import (
    resolve_enemy_enemy_collisions,
    resolve_player_enemy_collisions,
)
from game.systems.combat_system import (
    handle_enemy_projectile_collision,
    handle_player_attack_collision,
    handle_player_projectile_collision,
)
from game.systems.effect_system import update_effect_system
from game.systems.explosive_system import create_explosions_from_objects
from game.systems.life_reward_system import update_life_reward_system
from game.systems.loot_system import (
    create_enemy_loot,
    create_object_loot,
    update_loot_pickup,
)
from game.systems.manager_system import update_manager_system
from game.systems.player_input_system import update_player_input_system
from game.systems.projectile_system import (
    collect_enemy_projectile,
    collect_player_projectiles,
    update_projectiles,
)
from game.systems.wave_system import update_wave_completion, update_wave_system

def update_gameplay(game_state, keys):
    # 1. Input Collection
    player_input = PlayerInput(keys)

    # 2. Timer / Cooldown Advance
    player_can_act = not game_state.player.update_lifecycle_state()
    game_state.player.update_timers()
    update_manager_system(game_state)

    active_enemies = []
    for enemy in game_state.enemies:
        if enemy.update_special_lifecycle():
            continue
        enemy.update_timers()
        if enemy.update_hit_state():
            continue
        active_enemies.append(enemy)

    # 3. AI / State Decisions
    for enemy in active_enemies:
        enemy.update_ai_state(game_state.level, game_state.player, game_state.enemies)

    # 4. Player Input -> Action Requests
    if player_can_act:
        update_player_input_system(game_state, keys)
        game_state.player.request_actions(player_input)

    # 5. Movement
    old_x = game_state.player.x
    old_y = game_state.player.y
    if player_can_act:
        moving = game_state.player.update_movement(player_input)
        game_state.player.update_jump_physics(player_input)
        game_state.player.update_state_after_movement(moving)
        game_state.player.update_grabbed_enemy_position()

    for enemy in active_enemies:
        enemy.apply_knockback()
        enemy.update_movement_state(game_state.level, game_state.player, game_state.enemies)

    update_projectiles(game_state)
    apply_enemy_level_bounds(game_state)
    apply_player_level_bounds(game_state)
    apply_arena_bounds(game_state)

    # 6. Collision Detection & Resolution
    resolve_enemy_enemy_collisions(game_state)
    resolve_player_enemy_collisions(game_state, old_x, old_y)
    apply_player_level_bounds(game_state)
    apply_arena_bounds(game_state)
    handle_player_projectile_collision(game_state)
    handle_enemy_projectile_collision(game_state)

    # 7-8. Combat — Hitbox vs Hurtbox, then Damage/Reactions
    handle_player_attack_collision(game_state)
    for enemy in active_enemies:
        if enemy.state == enemy.DEAD:
            continue
        enemy.update_animation()
        enemy.update_attack_state(game_state.level, game_state.player)

    # 9. Entity Lifecycle — Spawn & Cleanup
    collect_player_projectiles(game_state)
    for enemy in game_state.enemies:
        collect_enemy_projectile(game_state, enemy)
    create_explosions_from_objects(game_state)
    create_enemy_loot(game_state)
    create_object_loot(game_state)
    update_loot_pickup(game_state)
    update_wave_system(game_state) # may lock camera and spawn enemies for next frame
    update_wave_completion(game_state)
    update_life_reward_system(game_state)
    update_effect_system(game_state)
    cleanup_game_state(game_state)

    # Presentation state before camera/render.
    if player_can_act:
        game_state.player.update_animation()
    for enemy in active_enemies:
        if enemy.state != enemy.ATTACK:
            enemy.update_animation()

