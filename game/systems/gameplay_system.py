from game.input.player_input import PlayerInput
from game.controllers.enemy_ai_context import EnemyAIContext
from game.controllers.player_action_context import PlayerActionContext
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
    handle_player_grab_or_throw,
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
from game.systems.inventory_system import update_player_weapon_interaction
from game.systems.projectile_system import (
    collect_enemy_projectile,
    collect_player_projectiles,
    update_projectiles,
)
from game.systems.lifecycle_system import advance_enemy_frame_state, advance_player_frame_state
from game.systems.wave_system import update_wave_completion, update_wave_system

# Frame order: frame-state -> decisions -> movement -> collision -> combat -> reactions -> cleanup -> presentation
# Camera and render happen after gameplay in main.py.
def update_gameplay(game_state, keys):
    player_input = PlayerInput(keys)
    player_context = PlayerActionContext(player_input)

    player_can_act = advance_player_frame_state(game_state)
    active_enemies = advance_enemy_frame_state(game_state)
    enemy_context = EnemyAIContext(game_state.level, game_state.player, game_state.enemies)

    _update_decisions(game_state, keys, player_context, player_can_act, active_enemies, enemy_context)
    old_player_position = _update_movement(game_state, player_context, player_can_act, active_enemies, enemy_context)
    _update_collisions(game_state, old_player_position)
    _update_combat(game_state, player_context, active_enemies, player_can_act, enemy_context)
    _update_reactions(game_state, player_can_act)
    _update_spawn_and_cleanup(game_state)
    _update_presentation(game_state)


def _update_decisions(game_state, keys, player_context, player_can_act, active_enemies, enemy_context):
    for enemy in active_enemies:
        enemy.update_ai(enemy_context)

    if player_can_act:
        update_player_weapon_interaction(game_state, keys)
        handle_player_grab_or_throw(game_state, keys)
        game_state.player.request_actions(player_context)


def _update_movement(game_state, player_context, player_can_act, active_enemies, enemy_context):
    old_player_position = (game_state.player.x, game_state.player.y)

    if player_can_act:
        game_state.player.update_movement(player_context)

    for enemy in active_enemies:
        enemy.update_movement(enemy_context)

    apply_enemy_level_bounds(game_state)
    apply_player_level_bounds(game_state)
    apply_arena_bounds(game_state)

    update_projectiles(game_state)

    return old_player_position


def _update_collisions(game_state, old_player_position):
    old_x, old_y = old_player_position

    resolve_enemy_enemy_collisions(game_state)
    resolve_player_enemy_collisions(game_state, old_x, old_y)
    apply_player_level_bounds(game_state)
    apply_arena_bounds(game_state)
    handle_player_projectile_collision(game_state)
    handle_enemy_projectile_collision(game_state)


def _update_combat(game_state, player_context, active_enemies, player_can_act, enemy_context):
    if player_can_act:
        game_state.player.update_attack(player_context)
    handle_player_attack_collision(game_state)

    for enemy in active_enemies:
        enemy.update_attack(enemy_context)


def _update_reactions(game_state, player_can_act):
    if player_can_act:
        game_state.player.update_reactions()

    for enemy in game_state.enemies:
        enemy.update_reactions()


def _update_spawn_and_cleanup(game_state):
    _collect_projectiles(game_state)
    _update_loot_and_effects(game_state)
    _update_waves(game_state)


def _collect_projectiles(game_state):
    collect_player_projectiles(game_state)
    for enemy in game_state.enemies:
        collect_enemy_projectile(game_state, enemy)


def _update_loot_and_effects(game_state):
    create_explosions_from_objects(game_state)
    create_enemy_loot(game_state)
    create_object_loot(game_state)
    update_loot_pickup(game_state)
    update_life_reward_system(game_state)
    update_effect_system(game_state)
    cleanup_game_state(game_state)


def _update_waves(game_state):
    # complete current wave using cleaned enemy list
    update_wave_completion(game_state)
    # spawn/start next wave after cleanup so dead enemies don't delay spawning
    update_wave_system(game_state)


def _update_presentation(game_state):
    game_state.score_manager.update()
    game_state.announcement_manager.update()
    game_state.stage_clear_manager.update()
    game_state.player.update_animation()

    for enemy in game_state.enemies:
        enemy.update_animation()
