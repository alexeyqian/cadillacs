from dataclasses import dataclass

from game.settings import *

@dataclass(frozen=True)
class EnemyConfig:
    enemy_id: str
    display_name: str = "Enemy"
    archetype: str = "basic_melee"
    collision_box_w: int = ENEMY_COLLISION_W
    collision_box_h: int = ENEMY_COLLISION_H
    max_hp: int = ENEMY_MAX_HP
    speed: float = ENEMY_SPEED
    patrol_distance:int = ENEMY_DETECT_RANGE
    detect_range: float = ENEMY_DETECT_RANGE
    attack_range:int = 90 
    attack_lane_range:int = 45
    attack_damage: float = ENEMY_ATTACK_DAMAGE
    attack_cooldown_duration: int = ENEMY_ATTACK_COOLDOWN
    hit_stun_duration: int = 15
    thrown_damage:int = THROWN_DAMAGE
    score_points: int = ENEMY_SCORE_POINTS
    sprite_scale: int  = 4


ENEMY_CONFIGS = {
    "ferris": EnemyConfig(
        enemy_id="ferris",
        display_name="Ferris"
    ),
    "gneiss": EnemyConfig(
        enemy_id="gneiss",
        display_name="Gneiss",
        max_hp=int(ENEMY_MAX_HP*1.2),
        speed=int(ENEMY_SPEED * 1.2),
        attack_damage=int(ENEMY_ATTACK_DAMAGE*1.2),
        score_points=int(ENEMY_SCORE_POINTS*1.2),
    ),
    "black_elmer": EnemyConfig(
        enemy_id="black_elmer",
        display_name="Black Elmer",
        archetype="heavy",
        max_hp=ENEMY_MAX_HP*2,
        speed=int(ENEMY_SPEED * 0.75),
        attack_damage=ENEMY_ATTACK_DAMAGE * 2,
        collision_box_w=int(ENEMY_COLLISION_W * 2),
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
        attack_damage=RAPTOR_ENEMY_ATTACK_DAMAGE,
        attack_cooldown_duration=50,
        score_points=int(ENEMY_SCORE_POINTS * 2),
    ),
    "ranged": EnemyConfig(
        enemy_id="ranged",
        display_name="Ranged Enemy",
        archetype="ranged",
        max_hp=RANGED_ENEMY_MAX_HP,
        attack_range=260,
        attack_lane_range=60,
        attack_damage=RANGED_ENEMY_ATTACK_DAMAGE,
        attack_cooldown_duration=90,
        score_points=int(ENEMY_SCORE_POINTS * 1.5),
    ),
    "boss": EnemyConfig(
        enemy_id="boss",
        display_name="Boss",
        archetype="boss",
        max_hp=ENEMY_MAX_HP*10,
        speed=int(ENEMY_SPEED * 0.5),
        attack_damage=ENEMY_ATTACK_DAMAGE*3,
        attack_cooldown_duration=60,
        collision_box_w=int(ENEMY_COLLISION_W * 2),
        score_points=int(ENEMY_SCORE_POINTS*10),
    ),
}

def get_enemy_config(enemy_type):
    return ENEMY_CONFIGS.get(enemy_type, ENEMY_CONFIGS["ferris"])
