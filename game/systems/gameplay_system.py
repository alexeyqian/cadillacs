from game.input.player_input import PlayerInput
from game.controllers.enemy_ai_context import EnemyAIContext
from game.controllers.player_action_context import PlayerActionContext
from game.systems.arena_system import ArenaSystem
from game.systems.bounds_system import BoundsSystem
from game.systems.collision_system import CollisionSystem
from game.systems.combat_system import CombatSystem
from game.systems.effect_system import EffectSystem
from game.systems.explosive_system import ExplosiveSystem
from game.systems.inventory_system import InventorySystem
from game.systems.life_reward_system import LifeRewardSystem
from game.systems.loot_system import LootSystem
from game.systems.projectile_system import ProjectileSystem
from game.systems.sound_system import SoundSystem
from game.systems.wave_system import WaveSystem

def update_gameplay(game_state, keys):
    player_can_act = game_state.player.can_act()
    old_player_x, old_player_y = game_state.player.x, game_state.player.y  # capture before movement

    _update_decisions(game_state, keys, player_can_act)
    _update_movement(game_state, player_can_act)
    _update_collisions(game_state, old_player_x, old_player_y)
    _update_combat(game_state, keys, player_can_act)
    ExplosiveSystem.create_explosions(game_state)  # damage enemies before reactions
    _update_reactions(game_state)
    _update_states(game_state)

    # todo: move to end
    _advance_timers(game_state, player_can_act)

    LootSystem.create_enemy_loot(game_state) # adds kill score
    LootSystem.create_object_loot(game_state) # add loot score
    # todo: move to next tick
    LootSystem.update_pickup(game_state)
    InventorySystem.pickup_weapon(game_state)
    # todo: move to somewhere
    LifeRewardSystem.update(game_state) # # ← here, sees latest score
    EffectSystem.update(game_state)
    # todo: move to somewhere
    ExplosiveSystem.update(game_state)

    _cleanup(game_state)
    _update_waves(game_state)
    _update_presentation(game_state)


def _update_decisions(game_state, keys, player_can_act):
    player_context = PlayerActionContext(PlayerInput(keys))
    game_state._player_context = player_context  # passed to movement/combat

    if player_can_act:
        game_state.player.request_actions(player_context)

    enemy_context = EnemyAIContext(game_state.level, game_state.player, game_state.enemies)
    game_state._enemy_context = enemy_context  # passed to movement/combat

    for enemy in game_state.enemies:
        enemy.update_ai(enemy_context)

    ProjectileSystem.collect_player(game_state)
    for enemy in game_state.enemies:
        ProjectileSystem.collect_enemy(game_state, enemy)


def _update_movement(game_state, player_can_act):
    player_context = game_state._player_context
    enemy_context = game_state._enemy_context

    if player_can_act:
        game_state.player.update_movement(player_context)
    for enemy in game_state.enemies:
        enemy.update_movement(enemy_context)

    BoundsSystem.apply_player_level(game_state)
    BoundsSystem.apply_enemy_level(game_state)
    ArenaSystem.apply_bounds(game_state)

    ProjectileSystem.update(game_state)


def _update_collisions(game_state, old_player_x, old_player_y):
    CollisionSystem.resolve_enemy_enemy(game_state)
    CollisionSystem.resolve_player_enemy(game_state, old_player_x, old_player_y)

    BoundsSystem.apply_player_level(game_state)
    BoundsSystem.apply_enemy_level(game_state)
    ArenaSystem.apply_bounds(game_state)

    player = game_state.player
    player.grab_controller.try_auto_grab(player, game_state.enemies, game_state.level)


def _update_combat(game_state, keys, player_can_act):
    if player_can_act:
        game_state.player.update_attack(game_state._player_context)
    CombatSystem.handle_player_attack(game_state)
    for enemy in game_state.enemies:
        enemy.update_attack(game_state._enemy_context)
    
    # todo: move to combat?
    CombatSystem.handle_player_projectile(game_state)
    CombatSystem.handle_enemy_projectile(game_state)


def _update_reactions(game_state):
    game_state.player.update_reactions()
    for enemy in game_state.enemies:
        enemy.update_reactions()


def _update_states(game_state):
    for enemy in game_state.enemies:
        enemy.update_state()


def _advance_timers(game_state, player_can_act):
    if player_can_act:
        game_state.player.advance_timers()
    for enemy in game_state.enemies:
        enemy.advance_timers()


def _cleanup(game_state):
    game_state.enemies[:] = [e for e in game_state.enemies if not e.is_ready_to_remove()]
    game_state.projectiles[:] = [p for p in game_state.projectiles if p.active]
    game_state.enemy_projectiles[:] = [p for p in game_state.enemy_projectiles if p.active]
    game_state.objects[:] = [o for o in game_state.objects if o.hp > 0]
    game_state.loot_items[:] = [l for l in game_state.loot_items if l.active]
    game_state.hit_sparks[:] = [s for s in game_state.hit_sparks if s.active]
    game_state.floating_texts[:] = [t for t in game_state.floating_texts if t.active]
    game_state.explosions[:] = [e for e in game_state.explosions if e.active]


def _update_waves(game_state):
    WaveSystem.update_completion(game_state)
    WaveSystem.update(game_state)


def _update_presentation(game_state):
    for text in game_state.floating_texts:
        text.update()
    game_state.score_manager.update()
    game_state.announcement_manager.update()
    game_state.stage_clear_manager.update()
    game_state.player.update_animation()
    for enemy in game_state.enemies:
        enemy.update_animation()
    SoundSystem.update(game_state, game_state.sound_manager)
