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
