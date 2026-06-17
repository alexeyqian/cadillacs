from dataclasses import dataclass

from game.settings import *


@dataclass(frozen=True)
class PlayerConfig:
    player_id: str
    display_name: str
    max_hp: int = PLAYER_MAX_HP
    lives: int = PLAYER_LIVES
    speed: float = PLAYER_SPEED
    run_speed: float = PLAYER_RUN_SPEED
    run_attack_damage: int = int(FIST_DAMAGE*1.5)
    jump_attack_damage: int = FIST_DAMAGE + 5
    jump_power: float = 12
    jump_gravity: float = 0.7
    air_move_speed: float = 3.0
    jump_takeoff_frames: int = 6
    landing_recovery_frames: int = 6
    grab_range: int = PLAYER_GRAB_RANGE
    width: int = PLAYER_W
    height: int = PLAYER_H
    collision_box_w: int = PLAYER_COLLISION_W
    collision_box_h: int = PLAYER_COLLISION_H
    hit_stun_duration: int = 20
    sprite_scale: int = 2


PLAYER_CONFIGS = {
    "mustapha": PlayerConfig(
        player_id="mustapha",
        display_name="Mustapha",
    ),
}


def get_player_config(player_type):
    return PLAYER_CONFIGS.get(player_type, PLAYER_CONFIGS["mustapha"])
