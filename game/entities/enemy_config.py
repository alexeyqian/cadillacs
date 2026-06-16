from dataclasses import dataclass
from typing import Optional

from game.settings import *
from game.entities.attack_data import AttackHitboxData, AttackPhaseData, EnemyAttackData

@dataclass(frozen=True)
class EnemyConfig:
    enemy_id: str
    display_name: str = "Enemy"
    archetype: str = "basic_melee"
    max_melee_attackers:int = 2 # move to stage config?
    collision_box_w: int = ENEMY_COLLISION_W
    collision_box_h: int = ENEMY_COLLISION_H
    max_hp: int = ENEMY_MAX_HP
    speed: float = ENEMY_SPEED
    patrol_distance:int = ENEMY_DETECT_RANGE
    detect_range: float = ENEMY_DETECT_RANGE
    attack_range:int = 90 
    attack_lane_range:int = 45
    # Normal melee enemies must be in the same lane to start attack
    # Boss/ranged can keep wider behavior for now
    # 0 = same lane only
    # 1 = same or adjacent lane
    attack_lane_reach: int = 0
    attack: EnemyAttackData = EnemyAttackData()
    melee_attack_slot_limit: Optional[int] = None

    hit_stun_duration: int = 15
    # give heavy enemies poise, so weak punches still deal damage 
    # but do not always interrupt them.
    flinch_damage_threshold: int = 0
    attack_flinch_damage_threshold: Optional[int] = None
    # Anti-stunlock tuning:
    # If the player lands this many quick hits inside the window, the enemy gets
    # a short stun-resistance window. Hits still deal damage, but light punches
    # stop resetting HIT forever, giving the enemy a chance to move or attack.
    anti_stunlock_hit_limit: int = 3
    anti_stunlock_hit_window: int = 90
    stun_resistance_duration: int = 45
    resisted_hit_stun_duration: int = 4
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
        attack_range=105,
        attack_lane_range=48,
        attack=EnemyAttackData(
            damage=ENEMY_ATTACK_DAMAGE,
            delay=16,
            cooldown=35,
            phase=AttackPhaseData(windup=18, active=8, recovery=22),
            hitboxes=(AttackHitboxData(x=72, y=-272, width=132, height=44),),
        ),
    ),
    "gneiss": EnemyConfig(
        enemy_id="gneiss",
        display_name="Gneiss",
        max_hp=int(ENEMY_MAX_HP*1.2),
        speed=int(ENEMY_SPEED * 1.2),
        attack_range=115,
        attack_lane_range=50,
        attack=EnemyAttackData(
            damage=int(ENEMY_ATTACK_DAMAGE * 0.9),
            delay=10,
            cooldown=28,
            phase=AttackPhaseData(windup=13, active=7, recovery=18),
            hitboxes=(AttackHitboxData(x=144, y=-264, width=120, height=40),),
        ),
        score_points=int(ENEMY_SCORE_POINTS*1.2),
    ),
    "black_elmer": EnemyConfig(
        enemy_id="black_elmer",
        display_name="Black Elmer",
        archetype="heavy",
        max_hp=ENEMY_MAX_HP*2,
        speed=int(ENEMY_SPEED * 0.75),
        attack_range=125,
        attack_lane_range=58,
        attack_lane_reach=1,
        attack=EnemyAttackData(
            damage=ENEMY_ATTACK_DAMAGE * 2,
            delay=24,
            cooldown=50,
            phase=AttackPhaseData(windup=24, active=11, recovery=28),
            hitboxes=(AttackHitboxData(x=128, y=-284, width=150, height=84),),
        ),
        collision_box_w=int(ENEMY_COLLISION_W * 2),
        # So Black Elmer only flinches from the heavy punch
        # light punch hits still reduce HP, but he can keep acting.
        flinch_damage_threshold=FIST_DAMAGE + 4,
        attack_flinch_damage_threshold=BAT_DAMAGE,
        score_points=int(ENEMY_SCORE_POINTS*2),
    ),
    "raptor": EnemyConfig(
        enemy_id="raptor",
        display_name="Raptor",
        archetype="raptor",
        max_hp=RAPTOR_ENEMY_MAX_HP,
        speed=RAPTOR_ENEMY_SPEED,
        attack_range=110,
        attack_lane_range=55,
        attack=EnemyAttackData(
            damage=RAPTOR_ENEMY_ATTACK_DAMAGE,
            delay=14,
            cooldown=60,
            phase=AttackPhaseData(windup=18, active=8, recovery=22),
            hitboxes=(AttackHitboxData(x=20, y=-448, width=132, height=96),),
        ),
        score_points=int(ENEMY_SCORE_POINTS * 2),
    ),
    "ranged": EnemyConfig(
        enemy_id="ranged",
        display_name="Ranged Enemy",
        archetype="ranged",
        max_hp=RANGED_ENEMY_MAX_HP,
        attack_range=260,
        attack_lane_range=60,
        attack=EnemyAttackData(
            damage=RANGED_ENEMY_ATTACK_DAMAGE,
            delay=24,
            cooldown=70,
            phase=AttackPhaseData(windup=28, active=4, recovery=34),
            hitboxes=(),
        ),
        score_points=int(ENEMY_SCORE_POINTS * 1.5),
    ),
    "boss": EnemyConfig(
        enemy_id="boss",
        display_name="Boss",
        archetype="boss",
        max_hp=ENEMY_MAX_HP*10,
        speed=int(ENEMY_SPEED * 0.5),
        attack_lane_reach=1,
        attack=EnemyAttackData(
            damage=ENEMY_ATTACK_DAMAGE * 3,
            delay=30,
            cooldown=60,
            phase=AttackPhaseData(windup=30, active=12, recovery=35),
            hitboxes=(AttackHitboxData(x=128, y=-284, width=120, height=80),),
        ),
        flinch_damage_threshold=FIST_DAMAGE + 4,
        collision_box_w=int(ENEMY_COLLISION_W * 2),
        score_points=int(ENEMY_SCORE_POINTS*10),
    ),
}

def get_enemy_config(enemy_type):
    return ENEMY_CONFIGS.get(enemy_type, ENEMY_CONFIGS["ferris"])
