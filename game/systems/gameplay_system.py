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
from game.systems.player_input_system import update_player_input_system
from game.systems.projectile_system import (
    collect_enemy_projectile,
    collect_player_projectiles,
    update_projectiles,
)
from game.systems.wave_system import update_wave_completion, update_wave_system

# Frame order: timers -> intentions -> movement -> collision -> combat -> reactions -> lifecycle.
# Camera and render happen after gameplay in main.py.
def update_gameplay(game_state, keys):
    # 1. Convert Player Keys Input to game logic input
    player_input = PlayerInput(keys)
    # 2-3. Lifecycle Guards, then Timer / Cooldown Advance
    player_can_act, active_enemies = _advance_lifecycle_and_timers(game_state)

    # 4-5. Enemy Decisions, then Player Action Requests
    _update_enemy_decisions(game_state, active_enemies)
    _request_player_actions(game_state, keys, player_input, player_can_act)

    # 6-9. Movement -> Collision -> Combat -> Reactions
    # Characters move voluntarily (running, jumping, chasing)
    # Characters are clamped to level/arena bounds
    # Projectiles move
    # Projectile collisions are checked
    # Hitbox/hurtbox overlap detected, damage and knockback velocity set
    # Knockback velocity applied as position change (consequence of this frame's hits)
    old_player_position = _update_character_movement(
        game_state,
        player_input,
        player_can_act,
        active_enemies,
    )
    _update_projectile_movement(game_state)
    _resolve_collisions(game_state, old_player_position)
    _update_combat(game_state, active_enemies, player_can_act)
    _update_reactions(game_state, active_enemies, player_can_act)

    # 10. Spawn / Cleanup, then presentation state before camera/render
    _update_lifecycle(game_state)
    _update_presentation(game_state)


def _advance_lifecycle_and_timers(game_state):
    player_is_blocked = (
        game_state.player.update_lifecycle_state()
        or game_state.player.update_reactions()
    )
    player_can_act = not player_is_blocked
    if player_can_act:
        game_state.player.advance_timers()

    active_enemies = []
    for enemy in game_state.enemies:
        if enemy.update_lifecycle_state():
            continue
        if enemy.update_reactions():
            continue
        enemy.advance_timers()
        active_enemies.append(enemy)

    # TODO: move to other places?
    game_state.score_manager.update()
    game_state.announcement_manager.update()
    game_state.stage_clear_manager.update()

    return player_can_act, active_enemies


def _update_enemy_decisions(game_state, active_enemies):
    for enemy in active_enemies:
        enemy.update_ai(game_state.level, game_state.player, game_state.enemies)


def _request_player_actions(game_state, keys, player_input, player_can_act):
    if not player_can_act:
        return

    update_player_input_system(game_state, keys)
    game_state.player.request_actions(player_input)

def _update_character_movement(game_state, player_input, player_can_act, active_enemies):
    old_player_position = (game_state.player.x, game_state.player.y)

    if player_can_act:
        game_state.player.update_movement(player_input)

    for enemy in active_enemies:
        enemy.update_movement(game_state.level, game_state.player, game_state.enemies)

    apply_enemy_level_bounds(game_state)
    apply_player_level_bounds(game_state)
    apply_arena_bounds(game_state)

    return old_player_position


def _update_projectile_movement(game_state):
    update_projectiles(game_state)


def _resolve_collisions(game_state, old_player_position):
    old_x, old_y = old_player_position

    resolve_enemy_enemy_collisions(game_state)
    resolve_player_enemy_collisions(game_state, old_x, old_y)
    apply_player_level_bounds(game_state)
    apply_arena_bounds(game_state)
    handle_player_projectile_collision(game_state)
    handle_enemy_projectile_collision(game_state)


def _update_combat(game_state, active_enemies, player_can_act):
    if player_can_act:
        game_state.player.update_attack()
    handle_player_attack_collision(game_state)

    for enemy in active_enemies:
        if enemy.state == enemy.DEAD:
            continue
        enemy.update_attack(game_state.level, game_state.player)


def _update_reactions(game_state, active_enemies, player_can_act):
    if player_can_act:
        game_state.player.update_reactions()

    for enemy in active_enemies:
        enemy.update_reactions()


def _update_lifecycle(game_state):
    # collected projectiles in this frame, 
    # then hurt players/enemies in future frames
    collect_player_projectiles(game_state)
    for enemy in game_state.enemies:
        collect_enemy_projectile(game_state, enemy)

    create_explosions_from_objects(game_state)
    create_enemy_loot(game_state)
    create_object_loot(game_state)

    update_loot_pickup(game_state)
    update_life_reward_system(game_state)
    update_effect_system(game_state)

    cleanup_game_state(game_state)
    # complete current wave using cleaned enemy list
    update_wave_completion(game_state)
    # spawn/start next wave late, for next frame logic
    # If cleanup has not run yet,
    # dead/removable enemies still count and can delay spawning by one frame.
    update_wave_system(game_state)


def _update_presentation(game_state):
    game_state.player.update_animation()

    for enemy in game_state.enemies:
        enemy.update_animation()
