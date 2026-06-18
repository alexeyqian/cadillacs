from dataclasses import dataclass
from typing import Optional

from game.settings import *
from game.entities.attack_data import AttackHitboxData, AttackPhaseData, EnemyAttackData

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

    hit_box_w: int = ENEMY_HITBOX_W
    hit_box_h: int = ENEMY_HITBOX_H
    hit_box_offset_x: int = ENEMY_HITBOX_OFFSET_X
    hit_box_offset_y: int = ENEMY_HITBOX_OFFSET_Y

    max_hp: int = ENEMY_MAX_HP
    speed: float = ENEMY_SPEED

    patrol_distance:int = ENEMY_DETECT_RANGE
    detect_range: float = ENEMY_DETECT_RANGE
    attack_range:int = ENEMY_ATTACK_RANGE
    attack_lane_range:int = ENEMY_ATTACK_LANE_RANGE
    # Normal melee enemies must be in the same lane to start attack
    # Boss/ranged can keep wider behavior for now
    # 0 = same lane only
    # 1 = same or adjacent lane
    attack_lane_reach: int = 0
    attack: EnemyAttackData = EnemyAttackData(
            damage=ENEMY_ATTACK_DAMAGE,
            delay=ENEMY_ATTACK_DELAY,
            cooldown=ENEMY_ATTACK_COOLDOWN,
            phase=AttackPhaseData(windup=ENEMY_ATTACK_WINDUP,
                                active=ENEMY_ATTACK_ACTIVE,
                                recovery=ENEMY_ATTACK_RECOVERY),
            hitboxes=(AttackHitboxData(
                x=ENEMY_HITBOX_OFFSET_X,
                y=ENEMY_HITBOX_OFFSET_Y, 
                width=ENEMY_HITBOX_W,
                height=ENEMY_HITBOX_H),),
        )

    max_melee_attackers:int = 2 # move to stage config?
    melee_attack_slot_limit: Optional[int] = None

    hit_stun_duration: int = 15 # for self or for player
    # give heavy enemies poise, so weak punches still deal damage 
    # but do not always interrupt them.
    flinch_damage_threshold: int = 0
    attack_flinch_damage_threshold: Optional[int] = None
    # TODO: too complicated, need to remove
    # Anti-stunlock tuning:
    # If the player lands this many quick hits inside the window, the enemy gets
    # a short stun-resistance window. Hits still deal damage, but light punches
    # stop resetting HIT forever, giving the enemy a chance to move or attack.
    anti_stunlock_hit_limit: int = 3
    anti_stunlock_hit_window: int = 90
    stun_resistance_duration: int = 45
    resisted_hit_stun_duration: int = 4
    breakout_recoil_duration: int = 10
    breakout_velocity: float = 6
    recovery_punish_delay_multiplier: float = 0.5

    thrown_damage:int = THROWN_DAMAGE
    score_points: int = ENEMY_SCORE_POINTS
    sprite_scale: int  = 4

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

        attack=EnemyAttackData(
            damage=int(ENEMY_ATTACK_DAMAGE * GNEISS_SCALER),
            delay=int(ENEMY_ATTACK_DELAY * 0.8),
            cooldown=int(ENEMY_ATTACK_COOLDOWN * 0.8),
            phase=AttackPhaseData(windup=ENEMY_ATTACK_WINDUP,
                                active=ENEMY_ATTACK_ACTIVE,
                                recovery=ENEMY_ATTACK_RECOVERY),
            hitboxes=(AttackHitboxData(
                        x=ENEMY_HITBOX_OFFSET_X,
                        y=ENEMY_HITBOX_OFFSET_Y,
                        width=ENEMY_HITBOX_W,
                        height=ENEMY_HITBOX_H),),
        ),
        score_points=int(ENEMY_SCORE_POINTS*GNEISS_SCALER),
    ),
    # 60, 85
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

        hit_box_w=200,
        hit_box_h=60,
        hit_box_offset_x=100,
        hit_box_offset_y=-250,

        max_hp=ENEMY_MAX_HP * 2,
        speed=int(ENEMY_SPEED * 0.7),

        attack_range=int(ENEMY_ATTACK_RANGE * BLACK_ELMER_SCALER),
        attack_lane_range=int(ENEMY_ATTACK_LANE_RANGE * BLACK_ELMER_SCALER),
        attack_lane_reach=1,
        attack=EnemyAttackData(
            damage=ENEMY_ATTACK_DAMAGE * BLACK_ELMER_SCALER,
            delay=int(ENEMY_ATTACK_DELAY * BLACK_ELMER_SCALER),
            cooldown=int(ENEMY_ATTACK_COOLDOWN * BLACK_ELMER_SCALER),
            phase=AttackPhaseData(windup=int(ENEMY_ATTACK_WINDUP*BLACK_ELMER_SCALER),
                                active=int(ENEMY_ATTACK_ACTIVE*BLACK_ELMER_SCALER),
                                recovery=int(ENEMY_ATTACK_RECOVERY*BLACK_ELMER_SCALER)),
            hitboxes=(
                AttackHitboxData(
                    x=int(ENEMY_HITBOX_OFFSET_X*BLACK_ELMER_SCALER),
                    y=int(ENEMY_HITBOX_OFFSET_Y*BLACK_ELMER_SCALER),
                    width=int(ENEMY_HITBOX_W*BLACK_ELMER_SCALER),
                    height=int(ENEMY_HITBOX_H*BLACK_ELMER_SCALER),
                ),
            ),
        ),
        # todo: simplify it
        # So Black Elmer only flinches from the heavy punch
        # light punch hits still reduce HP, but he can keep acting.
        flinch_damage_threshold=FIST_DAMAGE + 4,
        attack_flinch_damage_threshold=BAT_DAMAGE,
        anti_stunlock_hit_limit=2,

        score_points=int(ENEMY_SCORE_POINTS * BLACK_ELMER_SCALER),
    ),

    "walther": EnemyConfig(
        enemy_id="walther",
        display_name="Walther",
        archetype="heavy",

        collision_box_w=int(ENEMY_COLLISION_W * 2),
        collision_box_h=ENEMY_COLLISION_H,

        hurt_box_w=320,
        hurt_box_h=360,
        hurt_box_offset_x=-160,
        hurt_box_offset_y=-400,

        hit_box_w=200,
        hit_box_h=80,
        hit_box_offset_x=160,
        hit_box_offset_y=-300,

        max_hp=ENEMY_MAX_HP * 4,
        speed=int(ENEMY_SPEED * 0.7),
        attack_range=int(ENEMY_ATTACK_RANGE * WALTHER_SCALER),
        attack_lane_range=int(ENEMY_ATTACK_LANE_RANGE * WALTHER_SCALER),
        attack_lane_reach=1,
        attack=EnemyAttackData(
            damage=ENEMY_ATTACK_DAMAGE * WALTHER_SCALER,
            delay=int(ENEMY_ATTACK_DELAY * 1),
            cooldown=int(ENEMY_ATTACK_COOLDOWN * WALTHER_SCALER),
            phase=AttackPhaseData(windup=int(ENEMY_ATTACK_WINDUP*WALTHER_SCALER),
                                active=int(ENEMY_ATTACK_ACTIVE*WALTHER_SCALER),
                                recovery=int(ENEMY_ATTACK_RECOVERY*WALTHER_SCALER)),
            hitboxes=(
                AttackHitboxData(
                    x=400,
                    y=200,
                    width=200,
                    height=200,
                ),
            ),
        ),
        # So Black Elmer only flinches from the heavy punch
        # light punch hits still reduce HP, but he can keep acting.
        flinch_damage_threshold=FIST_DAMAGE + 100, # means no flinch
        attack_flinch_damage_threshold=BAT_DAMAGE,
        anti_stunlock_hit_limit=2,

        score_points=int(ENEMY_SCORE_POINTS * WALTHER_SCALER),
    ),
    "boss": EnemyConfig(
        enemy_id="boss",
        display_name="Boss",
        archetype="boss",

        max_hp=ENEMY_MAX_HP * 10,
        speed=BOSS_ENEMY_SPEED,

        attack_range=int(ENEMY_ATTACK_RANGE * WALTHER_SCALER),
        attack_lane_range=int(ENEMY_ATTACK_LANE_RANGE * WALTHER_SCALER),
        attack_lane_reach=1,
        attack=EnemyAttackData(
            damage=ENEMY_ATTACK_DAMAGE * WALTHER_SCALER,
            delay=ENEMY_ATTACK_DELAY,
            cooldown=int(ENEMY_ATTACK_COOLDOWN * WALTHER_SCALER),
            phase=AttackPhaseData(windup=int(ENEMY_ATTACK_WINDUP * WALTHER_SCALER),
                                active=int(ENEMY_ATTACK_ACTIVE * WALTHER_SCALER),
                                recovery=int(ENEMY_ATTACK_RECOVERY * WALTHER_SCALER)),
            hitboxes=(
                AttackHitboxData(
                    x=400,
                    y=200,
                    width=200,
                    height=200,
                ),
            ),
        ),
        flinch_damage_threshold=FIST_DAMAGE + 100,
        attack_flinch_damage_threshold=BAT_DAMAGE,
        anti_stunlock_hit_limit=2,

        score_points=int(ENEMY_SCORE_POINTS * WALTHER_SCALER),
    ),
}

def get_enemy_config(enemy_type):
    return ENEMY_CONFIGS.get(enemy_type, ENEMY_CONFIGS["ferris"])
