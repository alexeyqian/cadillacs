from dataclasses import dataclass, replace
from typing import Optional
from game.combat.attack_data import AttackData, DEFAULT_ENEMY_ATTACK_DATA
from game.settings import *

GNEISS_SCALER=1.2
BLACK_ELMER_SCALER=1.5
WALTHER_SCALER=3
DEFAULT_ENEMY_TYPE = "ferris"

@dataclass(frozen=True)
class EnemyConfig:
    enemy_id: str
    display_name: str = "Enemy"
    archetype: str = "basic_melee"

    collision_box_w: int = ENEMY_COLLISION_W
    collision_box_h: int = ENEMY_COLLISION_H

    hurt_box_w: int = ENEMY_HURTBOX_W
    hurt_box_h: int = ENEMY_HURTBOX_H
    hurt_box_offset_x: int = ENEMY_HURTBOX_OFFSET_X
    hurt_box_offset_y: int = ENEMY_HURTBOX_OFFSET_Y

    max_hp: int = ENEMY_MAX_HP
    speed: float = ENEMY_SPEED
    can_run: bool = False
    run_speed: float = ENEMY_RUN_SPEED
    can_run_attack: bool = False
    run_attack: Optional[AttackData] = None
    can_jump: bool = False
    can_jump_attack: bool = False
    jump_attack: Optional[AttackData] = None

    attack: AttackData = DEFAULT_ENEMY_ATTACK_DATA
    score_points: int = ENEMY_SCORE_POINTS
    sprite_scale: int  = 1

    # enemy specific
    patrol_distance:int = ENEMY_DETECT_RANGE
    detect_range: float = ENEMY_DETECT_RANGE
    attack_range:int = ENEMY_ATTACK_RANGE
    attack_lane_range:int = ENEMY_ATTACK_LANE_RANGE

    # give heavy enemies poise, so weak punches still deal damage
    # but do not always interrupt them.
    flinch_damage_threshold: int = 0
    attack_flinch_damage_threshold: Optional[int] = None
    knockdown_damage_threshold: int = 40

    max_melee_attackers:int = 2 # move to stage config?
    melee_attack_slot_limit: Optional[int] = None
# Each enemy archetype has a readable combat rhythm:
# Ferris   = basic pressure, fair but less passive.
# Gneiss   = fast striker, quicker startup and shorter cooldown.
# Elmer    = heavy bruiser, bigger reach and attack poise.
ENEMY_CONFIGS = {
    "ferris": EnemyConfig(
        enemy_id="ferris",
        display_name="Ferris",
    ),

    "gneiss": EnemyConfig(
        enemy_id="gneiss",
        display_name="Gneiss",
        sprite_scale=1,
        max_hp=int(ENEMY_MAX_HP * GNEISS_SCALER),
        speed=int(ENEMY_SPEED),

        attack=replace(
            DEFAULT_ENEMY_ATTACK_DATA,
            damage=int(ENEMY_ATTACK_DAMAGE * GNEISS_SCALER),
            delay=int(ENEMY_ATTACK_DELAY * 0.8),
            cooldown=int(ENEMY_ATTACK_COOLDOWN * 0.8),
            windup=ENEMY_ATTACK_WINDUP,
            active=ENEMY_ATTACK_ACTIVE,
            recovery=ENEMY_ATTACK_RECOVERY,
        ),
        score_points=int(ENEMY_SCORE_POINTS*GNEISS_SCALER),
    ),
    
    "blade": EnemyConfig(
        enemy_id="blade",
        display_name="Blade",
        max_hp=int(ENEMY_MAX_HP * 1.5),
        speed=int(ENEMY_SPEED),

        attack=replace(
            DEFAULT_ENEMY_ATTACK_DATA,
            damage=int(ENEMY_ATTACK_DAMAGE * 1.5),
            delay=int(ENEMY_ATTACK_DELAY * 0.8),
            cooldown=int(ENEMY_ATTACK_COOLDOWN * 0.8),
            windup=ENEMY_ATTACK_WINDUP,
            active=ENEMY_ATTACK_ACTIVE,
            recovery=ENEMY_ATTACK_RECOVERY,
        ),
        score_points=int(ENEMY_SCORE_POINTS*1.5),
    ),

    "black_elmer": EnemyConfig(
        enemy_id="black_elmer",
        display_name="Black Elmer",
        archetype="heavy",

        max_hp=ENEMY_MAX_HP * 2,
        speed=int(ENEMY_SPEED * 0.7),
        can_run=False,
        run_speed=int(ENEMY_RUN_SPEED * 0.9),
        can_run_attack=False,
        can_jump=False,
        can_jump_attack=False,

        attack_range=int(ENEMY_ATTACK_RANGE * BLACK_ELMER_SCALER),
        attack_lane_range=int(ENEMY_ATTACK_LANE_RANGE * BLACK_ELMER_SCALER),
        attack=replace(
            DEFAULT_ENEMY_ATTACK_DATA,
            damage=ENEMY_ATTACK_DAMAGE * BLACK_ELMER_SCALER,
            delay=int(ENEMY_ATTACK_DELAY * BLACK_ELMER_SCALER),
            cooldown=int(ENEMY_ATTACK_COOLDOWN * BLACK_ELMER_SCALER),
            windup=int(ENEMY_ATTACK_WINDUP*BLACK_ELMER_SCALER),
            active=int(ENEMY_ATTACK_ACTIVE*BLACK_ELMER_SCALER),
            recovery=int(ENEMY_ATTACK_RECOVERY*BLACK_ELMER_SCALER),
            lane_reach=1,
        ),
        # todo: simplify it
        # So Black Elmer only flinches from the heavy punch
        # light punch hits still reduce HP, but he can keep acting.
        flinch_damage_threshold=FIST_DAMAGE + 4,
        attack_flinch_damage_threshold=BAT_DAMAGE,

        score_points=int(ENEMY_SCORE_POINTS * BLACK_ELMER_SCALER),
    ),

    "walther": EnemyConfig(
        enemy_id="walther",
        display_name="Walther",
        archetype="heavy",

        max_hp=ENEMY_MAX_HP * 4,
        speed=int(ENEMY_SPEED * 0.7),
        attack_range=int(ENEMY_ATTACK_RANGE * WALTHER_SCALER),
        attack_lane_range=int(ENEMY_ATTACK_LANE_RANGE * WALTHER_SCALER),
        attack=replace(
            DEFAULT_ENEMY_ATTACK_DATA,
            damage=ENEMY_ATTACK_DAMAGE * WALTHER_SCALER,
            delay=int(ENEMY_ATTACK_DELAY * 1),
            cooldown=int(ENEMY_ATTACK_COOLDOWN * WALTHER_SCALER),
            windup=int(ENEMY_ATTACK_WINDUP*WALTHER_SCALER),
            active=int(ENEMY_ATTACK_ACTIVE*WALTHER_SCALER),
            recovery=int(ENEMY_ATTACK_RECOVERY*WALTHER_SCALER),
            lane_reach=1,
        ),
        # So Black Elmer only flinches from the heavy punch
        # light punch hits still reduce HP, but he can keep acting.
        flinch_damage_threshold=FIST_DAMAGE + 100, # means no flinch
        attack_flinch_damage_threshold=BAT_DAMAGE,

        score_points=int(ENEMY_SCORE_POINTS * WALTHER_SCALER),
    ),

}

def get_enemy_config(enemy_type):
    return ENEMY_CONFIGS.get(enemy_type, ENEMY_CONFIGS[DEFAULT_ENEMY_TYPE])
