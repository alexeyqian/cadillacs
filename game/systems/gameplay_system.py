from game.input.player_input import PlayerInput
from game.systems.arena_system import apply_arena_bounds
from game.systems.bounds_system import apply_enemy_level_bounds, apply_player_level_bounds
from game.systems.camera_system import update_camera_system
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
from game.systems.enemy_system import update_enemy_system
from game.systems.explosive_system import create_explosions_from_objects
from game.systems.life_reward_system import update_life_reward_system
from game.systems.loot_system import (
    create_enemy_loot,
    create_object_loot,
    update_loot_pickup,
)
from game.systems.manager_system import update_manager_system
from game.systems.projectile_system import collect_player_projectiles, update_projectiles
from game.systems.wave_system import update_wave_completion, update_wave_system

# do not put arena lock logic inside player, enemy, camera
# arena system controls temporary battle boundaries
def update_gameplay(game_state, keys):
    update_wave_system(game_state) # may lock camera
    
    old_x = game_state.player.x
    old_y = game_state.player.y
    player_input = PlayerInput(keys)

    # update player
    game_state.player.update(player_input)
    # moved from player.py
    apply_player_level_bounds(game_state)
    
    # update enemies
    update_enemy_system(game_state)

    resolve_enemy_enemy_collisions(game_state)
    apply_enemy_level_bounds(game_state)
    resolve_player_enemy_collisions(game_state, old_x, old_y)
    apply_player_level_bounds(game_state)
    apply_arena_bounds(game_state) # clamps player/enemies if camera locked
    collect_player_projectiles(game_state)
    update_projectiles(game_state)

    # important: handle attack
    handle_player_attack_collision(game_state)

    handle_player_projectile_collision(game_state)
    handle_enemy_projectile_collision(game_state)
    create_explosions_from_objects(game_state)

    create_enemy_loot(game_state)
    create_object_loot(game_state)
    update_loot_pickup(game_state)

    update_wave_completion(game_state)
    update_life_reward_system(game_state)

    # apply arena bounds before camera update
    update_camera_system(game_state) # camera follows player or stays locked

    update_effect_system(game_state)
    update_manager_system(game_state)

    cleanup_game_state(game_state)
