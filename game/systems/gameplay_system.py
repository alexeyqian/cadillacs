from game.systems.wave_system import *
from game.systems.enemy_system import *
from game.systems.projectile_system import *
from game.systems.combat_system import *
from game.systems.loot_system import *
from game.systems.life_reward_system import *
from game.systems.camera_system import *
from game.systems.cleanup_system import *
from game.systems.manager_system import *
from game.systems.effect_system import *
from game.systems.arena_system import *
from game.systems.explosive_system import *

# do not put arena lock logic inside player, enemy, camera
# arena system controls temporary battle boundaries
def update_gameplay(game_state, keys):
    update_wave_system(game_state) # may lock camera
    
    old_x = game_state.player.x
    old_y = game_state.player.y
    game_state.player.update()
    # moved from player.py
    game_state.player.apply_world_bounds(game_state.level.world_width,
        game_state.level.lane_top, game_state.level.lane_bottom)
    update_enemy_system(game_state)
    # TODO: check if this is dup with apply_world_bounds function in enemy
    apply_arena_bounds(game_state) # clamps player/enemies if camera locked
    collect_player_projectiles(game_state)
    update_projectiles(game_state)

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
