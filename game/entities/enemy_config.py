from dataclasses import dataclass

from game.settings import *

@dataclass(frozen=True)
class EnemyConfig:
    enemy_id: str
    display_name: str
    archetype: str
    max_hp: int
    speed: float
    detect_range: float = ENEMY_DETECT_RANGE
    attack_range:int = 90 
    attack_lane_range:int = 45
    attack_damage: float
    attack_cooldown_duration: int = ENEMY_ATTACK_COOLDOWN
    collision_box_w: int = ENEMY_COLLISION_W
    hit_stun_duration: int = 15
    score_points: int = 100


ENEMY_CONFIGS = {

    "ranged": EnemyConfig(
        enemy_id="ranged",
        display_name="Poacher Joe",
        archetype="ranged",
        max_hp=RANGED_ENEMY_MAX_HP,
        speed=ENEMY_SPEED * 0.85,
        attack_damage=RANGED_ENEMY_ATTACK_DAMAGE,
        score_points=250,
    ),

    # Named Cadillacs & Dinosaurs-inspired roster entries.
    "ferris": EnemyConfig(
        enemy_id="ferris",
        display_name="Ferris",
        archetype="basic_melee",
        max_hp=ENEMY_MAX_HP,
        speed=ENEMY_SPEED,
        attack_damage=ENEMY_ATTACK_DAMAGE,
        hit_stun_duration=28,
        score_points=100,
    ),
    "driver": EnemyConfig(
        enemy_id="driver",
        display_name="Driver",
        archetype="basic_melee",
        max_hp=ENEMY_MAX_HP,
        speed=ENEMY_SPEED * 1.08,
        attack_damage=ENEMY_ATTACK_DAMAGE,
        score_points=125,
    ),
    "gneiss": EnemyConfig(
        enemy_id="gneiss",
        display_name="Gneiss",
        archetype="basic_melee",
        max_hp=int(ENEMY_MAX_HP*1.2),
        speed=ENEMY_SPEED * 1.10,
        attack_damage=8,
        hit_stun_duration=28,
        score_points=110,
    ),
    "punk": EnemyConfig(
        enemy_id="punk",
        display_name="Punk",
        archetype="fast_small",
        max_hp=35,
        speed=ENEMY_SPEED * 1.35,
        attack_damage=7,
        collision_box_w=int(FAST_ENEMY_W * 0.5),
        score_points=180,
    ),
    "thug": EnemyConfig(
        enemy_id="thug",
        display_name="Thug",
        archetype="fast_small",
        max_hp=40,
        speed=ENEMY_SPEED * 1.25,
        attack_damage=8,
        collision_box_w=int(FAST_ENEMY_W * 0.5),
        score_points=190,
    ),
    "blade": EnemyConfig(
        enemy_id="blade",
        display_name="Blade",
        archetype="weapon",
        max_hp=55,
        speed=ENEMY_SPEED * 1.05,
        attack_damage=12,
        score_points=225,
    ),
    "razor": EnemyConfig(
        enemy_id="razor",
        display_name="Razor",
        archetype="weapon",
        max_hp=60,
        speed=ENEMY_SPEED * 1.1,
        attack_damage=13,
        
        score_points=240,
    ),
    "poacher_joe": EnemyConfig(
        enemy_id="poacher_joe",
        display_name="Poacher Joe",
        archetype="ranged",
        max_hp=60,
        speed=ENEMY_SPEED * 0.85,
        attack_damage=18,
        score_points=250,
    ),
    "gutter": EnemyConfig(
        enemy_id="gutter",
        display_name="Gutter",
        archetype="ranged",
        max_hp=65,
        speed=ENEMY_SPEED * 0.9,
        attack_damage=18,
        score_points=275,
    ),
    "skinner": EnemyConfig(
        enemy_id="skinner",
        display_name="Skinner",
        archetype="ranged",
        max_hp=70,
        speed=ENEMY_SPEED * 0.92,
        attack_damage=20,
        score_points=300,
    ),
    "black_elmer": EnemyConfig(
        enemy_id="black_elmer",
        display_name="Black Elmer",
        archetype="heavy",
        max_hp=95,
        speed=ENEMY_SPEED * 0.75,
        attack_damage=16,
        collision_box_w=int(HEAVY_ENEMY_W * 0.5),
        
        score_points=300,
    ),
    "hammer": EnemyConfig(
        enemy_id="hammer",
        display_name="Hammer Terhune",
        archetype="heavy",
        max_hp=115,
        speed=ENEMY_SPEED * 0.8,
        attack_damage=18,
        collision_box_w=int(HEAVY_ENEMY_W * 0.5),
        
        score_points=350,
    ),
    "wrench": EnemyConfig(
        enemy_id="wrench",
        display_name="Wrench Terhune",
        archetype="heavy",
        max_hp=105,
        speed=ENEMY_SPEED * 0.85,
        attack_damage=17,
        collision_box_w=int(HEAVY_ENEMY_W * 0.5),
        
        score_points=325,
    ),
    "boss": EnemyConfig(
        enemy_id="boss",
        display_name="Boss",
        archetype="boss",
        max_hp=BOSS_ENEMY_MAX_HP,
        speed=BOSS_ENEMY_SPEED,
        attack_damage=BOSS_ENEMY_ATTACK_DAMAGE,
        attack_cooldown_duration=60,
        collision_box_w=int(BOSS_ENEMY_W * 0.5),


        hit_stun_duration=8,
        score_points=1000,
    ),
}


def get_enemy_config(enemy_type):
    return ENEMY_CONFIGS.get(enemy_type, ENEMY_CONFIGS["ferris"])
