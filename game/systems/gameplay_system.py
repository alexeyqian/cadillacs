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

def update_gameplay(game_state, keys):
    update_wave_system(game_state)
    game_state.player.update()
    update_enemy_system()
    collect_player_projectiles(game_state)
    update_projectiles(game_state)

    handle_player_attack_collision(game_state)
    handle_player_projectile_collision(game_state)
    handle_enemy_projectile_collision(game_state)

    create_enemy_loot(game_state)
    create_object_loot(game_state)
    update_loot_pickup(game_state)

    update_wave_completion(game_state)
    update_life_reward_system(game_state)
    update_camera_system(game_state)
    
    update_effect_system(game_state)
    update_manager_system(game_state)

    cleanup_game_state(game_state)
