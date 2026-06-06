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