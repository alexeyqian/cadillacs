from game.input.player_input import PlayerInput
from game.controllers.enemy_ai_context import EnemyAIContext
from game.controllers.player_action_context import PlayerActionContext
from game.systems.arena_system import apply_arena_bounds
from game.systems.bounds_system import apply_enemy_level_bounds, apply_player_level_bounds
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

from game.systems.wave_system import update_wave_completion, update_wave_system
from game.systems.sound_system import update_sound

# Frame order: read states -> collect inputs 
# -> enemy decisions and player action request -> movement
# (after this, all positions are finalized)
# -> collision -> combat -> reactions -> cleanup -> presentation
def update_gameplay(game_state, keys):
    # --- READ: determine who can act this frame ---
    player_can_act = game_state.player.can_act()

    # --- LOGIC: decisions → movement → combat → reactions ---
    player_input = PlayerInput(keys)
    player_context = PlayerActionContext(player_input)
    # player action request (done by player)
    if player_can_act:
        update_player_weapon_interaction(game_state, keys) # move to other place
        handle_player_grab_or_throw(game_state, keys) # move to other place
        game_state.player.request_actions(player_context) # todo: should we return action request here?
    # enemy action request (done by ai)
    enemy_context = EnemyAIContext(game_state.level, game_state.player, game_state.enemies)
    for enemy in game_state.enemies:
        enemy.update_ai(enemy_context) # todo: should we return action request here?

    collect_player_projectiles(game_state)
    for enemy in game_state.enemies:
        collect_enemy_projectile(game_state, enemy)

    _update_movement(game_state, player_context, enemy_context)
    _update_collisions(game_state)
    _update_combat(game_state, player_context, enemy_context)
    _update_reactions(game_state)

    # advance timers
    game_state.player.advance_timers()
    for enemy in game_state.enemies:
        enemy.advance_timers()

    _update_loot_and_effects(game_state)
    _update_waves(game_state)
    _cleanup_game_state(game_state)
    _update_presentation(game_state)


def _update_movement(game_state, player_context, enemy_context):
    game_state.player.update_movement(player_context)

    for enemy in game_state.enemies:
        enemy.update_movement(enemy_context)

    apply_player_level_bounds(game_state)
    apply_enemy_level_bounds(game_state)
    apply_arena_bounds(game_state)

    update_projectiles(game_state)


def _update_collisions(game_state):
    x, y = (game_state.player.x, game_state.player.y)

    resolve_enemy_enemy_collisions(game_state)
    resolve_player_enemy_collisions(game_state, x, y)

    apply_player_level_bounds(game_state)
    apply_enemy_level_bounds(game_state)
    apply_arena_bounds(game_state)

    # todo: move to combat system?
    handle_player_projectile_collision(game_state)
    handle_enemy_projectile_collision(game_state)


def _update_combat(game_state, player_context, enemy_context):
    game_state.player.update_attack(player_context)
    # todo: move to player.update_attack()?
    handle_player_attack_collision(game_state)

    for enemy in game_state.enemies:
        enemy.update_attack(enemy_context)


def _update_reactions(game_state):
    game_state.player.update_reactions()

    for enemy in game_state.enemies:
        enemy.update_reactions()

def _update_loot_and_effects(game_state):
    create_explosions_from_objects(game_state)
    create_enemy_loot(game_state)
    create_object_loot(game_state)
    update_loot_pickup(game_state)
    update_life_reward_system(game_state)
    update_effect_system(game_state)
    


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

    update_sound(game_state, game_state.sound_manager)

def _cleanup_game_state(game_state):
    # remove dead enemies
    game_state.enemies[:] = [
        enemy for enemy in game_state.enemies
        if not enemy.is_ready_to_remove()
    ]
    # clean up player projectiles
    game_state.projectiles[:] = [p for p in game_state.projectiles if p.active]
    # clean up enemy projectiles
    game_state.enemy_projectiles[:] = [
        p for p in game_state.enemy_projectiles
        if p.active
    ]
    # clean up breakables
    game_state.objects[:] = [obj for obj in game_state.objects if obj.hp > 0]
    # clean up loots
    game_state.loot_items[:] = [l for l in game_state.loot_items if l.active]
    # clean up hit sparks
    game_state.hit_sparks[:] = [s for s in game_state.hit_sparks if s.active]
    # clean floating text
    game_state.floating_texts[:] = [item for item in game_state.floating_texts if item.active]
    game_state.explosions[:] = [item for item in game_state.explosions if item.active]
