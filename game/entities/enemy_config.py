from dataclasses import dataclass, replace
from typing import Optional
from game.settings import *
from game.entities.attack_data import AttackData, DEFAULT_ENEMY_ATTACK_DATA

GNEISS_SCALER=1.2
BLACK_ELMER_SCALER=1.5
WALTHER_SCALER=3

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
    # todo:move inside attack data
    attack_range:int = ENEMY_ATTACK_RANGE
    attack_lane_range:int = ENEMY_ATTACK_LANE_RANGE

    # Normal melee enemies must be in the same lane to start attack
    # Boss/ranged can keep wider behavior for now
    # 0 = same lane only
    # 1 = same or adjacent lane
    # todo: remove, already in attack data
    attack_lane_reach: int = 0
    hit_stun_duration: int = 15 # for self or for player
    attack: AttackData = DEFAULT_ENEMY_ATTACK_DATA
    score_points: int = ENEMY_SCORE_POINTS
    sprite_scale: int  = 4

    # enemy specific
    patrol_distance:int = ENEMY_DETECT_RANGE
    detect_range: float = ENEMY_DETECT_RANGE
    # todo: move to enemy reactions
    # give heavy enemies poise, so weak punches still deal damage 
    # but do not always interrupt them.
    flinch_damage_threshold: int = 0
    # todo: should be single int
    attack_flinch_damage_threshold: Optional[int] = None
    # it should be field of EnemyCombatController
    max_melee_attackers:int = 2 # move to stage config?
    melee_attack_slot_limit: Optional[int] = None
    # todo:should not be here
    thrown_damage:int = THROWN_DAMAGE

# Each enemy archetype has a readable combat rhythm:
# Ferris   = basic pressure, fair but less passive.
# Gneiss   = fast striker, quicker startup and shorter cooldown.
# Elmer    = heavy bruiser, bigger reach and attack poise.
# Ranged   = long pressure, shorter pauses between shots.
ENEMY_CONFIGS = {
    "ferris": EnemyConfig(
        enemy_id="ferris",
        display_name="Ferris",
    ),

    "gneiss": EnemyConfig(
        enemy_id="gneiss",
        display_name="Gneiss",
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
            hitbox_offset_x=ENEMY_HITBOX_OFFSET_X,
            hitbox_offset_y=ENEMY_HITBOX_OFFSET_Y,
            hitbox_w=ENEMY_HITBOX_W,
            hitbox_h=ENEMY_HITBOX_H,
        ),
        score_points=int(ENEMY_SCORE_POINTS*GNEISS_SCALER),
    ),

    "black_elmer": EnemyConfig(
        enemy_id="black_elmer",
        display_name="Black Elmer",
        archetype="heavy",

        collision_box_w=int(ENEMY_COLLISION_W * BLACK_ELMER_SCALER),
        collision_box_h=ENEMY_COLLISION_H,

        hurt_box_w=200,
        hurt_box_h=300,
        hurt_box_offset_x=-100,
        hurt_box_offset_y=-300,

        max_hp=ENEMY_MAX_HP * 2,
        speed=int(ENEMY_SPEED * 0.7),

        attack_range=int(ENEMY_ATTACK_RANGE * BLACK_ELMER_SCALER),
        attack_lane_range=int(ENEMY_ATTACK_LANE_RANGE * BLACK_ELMER_SCALER),
        attack_lane_reach=1,
        attack=replace(
            DEFAULT_ENEMY_ATTACK_DATA,
            damage=ENEMY_ATTACK_DAMAGE * BLACK_ELMER_SCALER,
            delay=int(ENEMY_ATTACK_DELAY * BLACK_ELMER_SCALER),
            cooldown=int(ENEMY_ATTACK_COOLDOWN * BLACK_ELMER_SCALER),
            windup=int(ENEMY_ATTACK_WINDUP*BLACK_ELMER_SCALER),
            active=int(ENEMY_ATTACK_ACTIVE*BLACK_ELMER_SCALER),
            recovery=int(ENEMY_ATTACK_RECOVERY*BLACK_ELMER_SCALER),
            hitbox_offset_x=200,
            hitbox_offset_y=60,
            hitbox_w=100,
            hitbox_h=-250,
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

        collision_box_w=250,
        collision_box_h=ENEMY_COLLISION_H,

        hurt_box_w=250,
        hurt_box_h=400,
        hurt_box_offset_x=-125,
        hurt_box_offset_y=-400,

        max_hp=ENEMY_MAX_HP * 4,
        speed=int(ENEMY_SPEED * 0.7),
        attack_range=int(ENEMY_ATTACK_RANGE * WALTHER_SCALER),
        attack_lane_range=int(ENEMY_ATTACK_LANE_RANGE * WALTHER_SCALER),
        attack_lane_reach=1,
        attack=replace(
            DEFAULT_ENEMY_ATTACK_DATA,
            damage=ENEMY_ATTACK_DAMAGE * WALTHER_SCALER,
            delay=int(ENEMY_ATTACK_DELAY * 1),
            cooldown=int(ENEMY_ATTACK_COOLDOWN * WALTHER_SCALER),
            windup=int(ENEMY_ATTACK_WINDUP*WALTHER_SCALER),
            active=int(ENEMY_ATTACK_ACTIVE*WALTHER_SCALER),
            recovery=int(ENEMY_ATTACK_RECOVERY*WALTHER_SCALER),
            hitbox_offset_x=125,
            hitbox_offset_y=-350,
            hitbox_w=180,
            hitbox_h=200,
        ),
        # So Black Elmer only flinches from the heavy punch
        # light punch hits still reduce HP, but he can keep acting.
        flinch_damage_threshold=FIST_DAMAGE + 100, # means no flinch
        attack_flinch_damage_threshold=BAT_DAMAGE,

        score_points=int(ENEMY_SCORE_POINTS * WALTHER_SCALER),
    ),
}

def get_enemy_config(enemy_type):
    return ENEMY_CONFIGS.get(enemy_type, ENEMY_CONFIGS["ferris"])
