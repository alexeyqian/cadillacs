from game.systems.combat_system import handle_player_grab_or_throw
from game.systems.inventory_system import update_player_weapon_interaction

def update_player_input_system(game_state, keys):
    update_player_weapon_interaction(game_state, keys)
    handle_player_grab_or_throw(game_state, keys)
