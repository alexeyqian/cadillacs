from dataclasses import dataclass, field
from typing import Any

from game.animation.animation_config import *
from game.settings import *

@dataclass(frozen=True)
class EnemyConfig:
    enemy_id: str
    display_name: str
    archetype: str
    max_hp: int
    speed: float
    attack_damage: float
    width: float = ENEMY_W
    height: float = ENEMY_H
    detect_range: float = ENEMY_DETECT_RANGE
    attack_range_multiplier: float = 1.0
    attack_cooldown: int = 45
    attack_timing: dict = field(default_factory=lambda: {
        "windup": ENEMY_ATTACK_WINDUP,
        "active": ENEMY_ATTACK_ACTIVE,
        "recovery": ENEMY_ATTACK_RECOVERY,
    })
    score_points: int = 100
    idle_config: Any = field(default_factory=lambda: NORMAL_ENEMY_IDLE)
    walk_config: Any = field(default_factory=lambda: NORMAL_ENEMY_WALK)
    attack_config: Any = field(default_factory=lambda: NORMAL_ENEMY_ATTACK)


ENEMY_CONFIGS = {
    # Legacy aliases used by existing stage configs.
    "normal": EnemyConfig(
        enemy_id="normal",
        display_name="Ferris",
        archetype="basic_melee",
        max_hp=ENEMY_MAX_HP,
        speed=ENEMY_SPEED,
        attack_damage=ENEMY_ATTACK_DAMAGE,
        score_points=100,
    ),
    "fast": EnemyConfig(
        enemy_id="fast",
        display_name="Punk",
        archetype="fast_small",
        max_hp=FAST_ENEMY_MAX_HP,
        speed=FAST_ENEMY_SPEED,
        attack_damage=FAST_ENEMY_ATTACK_DAMAGE,
        width=FAST_ENEMY_W,
        height=FAST_ENEMY_H,
        attack_timing={
            "windup": 14,
            "active": 8,
            "recovery": ENEMY_ATTACK_RECOVERY,
        },
        score_points=200,
        idle_config=FAST_ENEMY_IDLE,
        walk_config=FAST_ENEMY_WALK,
        attack_config=FAST_ENEMY_ATTACK,
    ),
    "heavy": EnemyConfig(
        enemy_id="heavy",
        display_name="Hammer Terhune",
        archetype="heavy",
        max_hp=HEAVY_ENEMY_MAX_HP,
        speed=HEAVY_ENEMY_SPEED,
        attack_damage=HEAVY_ENEMY_ATTACK_DAMAGE,
        width=HEAVY_ENEMY_W,
        height=HEAVY_ENEMY_H,
        attack_range_multiplier=1.2,
        attack_timing={
            "windup": 26,
            "active": 10,
            "recovery": ENEMY_ATTACK_RECOVERY,
        },
        score_points=300,
        idle_config=HEAVY_ENEMY_IDLE,
        walk_config=HEAVY_ENEMY_WALK,
        attack_config=HEAVY_ENEMY_ATTACK,
    ),
    "ranged": EnemyConfig(
        enemy_id="ranged",
        display_name="Poacher Joe",
        archetype="ranged",
        max_hp=RANGED_ENEMY_MAX_HP,
        speed=ENEMY_SPEED * 0.85,
        attack_damage=RANGED_ENEMY_ATTACK_DAMAGE,
        attack_range_multiplier=4.0,
        attack_timing={
            "windup": ENEMY_ATTACK_WINDUP,
            "active": 3,
            "recovery": ENEMY_ATTACK_RECOVERY,
        },
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
        max_hp=50,
        speed=ENEMY_SPEED * 1.02,
        attack_damage=8,
        score_points=110,
    ),
    "punk": EnemyConfig(
        enemy_id="punk",
        display_name="Punk",
        archetype="fast_small",
        max_hp=35,
        speed=ENEMY_SPEED * 1.35,
        attack_damage=7,
        width=FAST_ENEMY_W,
        height=FAST_ENEMY_H,
        attack_timing={
            "windup": 14,
            "active": 8,
            "recovery": ENEMY_ATTACK_RECOVERY,
        },
        score_points=180,
        idle_config=FAST_ENEMY_IDLE,
        walk_config=FAST_ENEMY_WALK,
        attack_config=FAST_ENEMY_ATTACK,
    ),
    "thug": EnemyConfig(
        enemy_id="thug",
        display_name="Thug",
        archetype="fast_small",
        max_hp=40,
        speed=ENEMY_SPEED * 1.25,
        attack_damage=8,
        width=FAST_ENEMY_W,
        height=FAST_ENEMY_H,
        attack_timing={
            "windup": 14,
            "active": 8,
            "recovery": ENEMY_ATTACK_RECOVERY,
        },
        score_points=190,
        idle_config=FAST_ENEMY_IDLE,
        walk_config=FAST_ENEMY_WALK,
        attack_config=FAST_ENEMY_ATTACK,
    ),
    "blade": EnemyConfig(
        enemy_id="blade",
        display_name="Blade",
        archetype="weapon",
        max_hp=55,
        speed=ENEMY_SPEED * 1.05,
        attack_damage=12,
        attack_range_multiplier=1.6,
        attack_timing={
            "windup": 18,
            "active": 10,
            "recovery": 28,
        },
        score_points=225,
    ),
    "razor": EnemyConfig(
        enemy_id="razor",
        display_name="Razor",
        archetype="weapon",
        max_hp=60,
        speed=ENEMY_SPEED * 1.1,
        attack_damage=13,
        attack_range_multiplier=1.65,
        attack_timing={
            "windup": 18,
            "active": 10,
            "recovery": 28,
        },
        score_points=240,
    ),
    "poacher_joe": EnemyConfig(
        enemy_id="poacher_joe",
        display_name="Poacher Joe",
        archetype="ranged",
        max_hp=60,
        speed=ENEMY_SPEED * 0.85,
        attack_damage=18,
        attack_range_multiplier=4.0,
        attack_timing={
            "windup": ENEMY_ATTACK_WINDUP,
            "active": 3,
            "recovery": ENEMY_ATTACK_RECOVERY,
        },
        score_points=250,
    ),
    "gutter": EnemyConfig(
        enemy_id="gutter",
        display_name="Gutter",
        archetype="ranged",
        max_hp=65,
        speed=ENEMY_SPEED * 0.9,
        attack_damage=18,
        attack_range_multiplier=4.0,
        attack_timing={
            "windup": ENEMY_ATTACK_WINDUP,
            "active": 3,
            "recovery": ENEMY_ATTACK_RECOVERY,
        },
        score_points=275,
    ),
    "skinner": EnemyConfig(
        enemy_id="skinner",
        display_name="Skinner",
        archetype="ranged",
        max_hp=70,
        speed=ENEMY_SPEED * 0.92,
        attack_damage=20,
        attack_range_multiplier=4.0,
        attack_timing={
            "windup": ENEMY_ATTACK_WINDUP,
            "active": 3,
            "recovery": ENEMY_ATTACK_RECOVERY,
        },
        score_points=300,
    ),
    "black_elmer": EnemyConfig(
        enemy_id="black_elmer",
        display_name="Black Elmer",
        archetype="heavy",
        max_hp=95,
        speed=ENEMY_SPEED * 0.75,
        attack_damage=16,
        width=HEAVY_ENEMY_W,
        height=HEAVY_ENEMY_H,
        attack_range_multiplier=1.2,
        attack_timing={
            "windup": 26,
            "active": 10,
            "recovery": ENEMY_ATTACK_RECOVERY,
        },
        score_points=300,
        idle_config=HEAVY_ENEMY_IDLE,
        walk_config=HEAVY_ENEMY_WALK,
        attack_config=HEAVY_ENEMY_ATTACK,
    ),
    "hammer": EnemyConfig(
        enemy_id="hammer",
        display_name="Hammer Terhune",
        archetype="heavy",
        max_hp=115,
        speed=ENEMY_SPEED * 0.8,
        attack_damage=18,
        width=HEAVY_ENEMY_W,
        height=HEAVY_ENEMY_H,
        attack_range_multiplier=1.25,
        attack_timing={
            "windup": 26,
            "active": 10,
            "recovery": ENEMY_ATTACK_RECOVERY,
        },
        score_points=350,
        idle_config=HEAVY_ENEMY_IDLE,
        walk_config=HEAVY_ENEMY_WALK,
        attack_config=HEAVY_ENEMY_ATTACK,
    ),
    "wrench": EnemyConfig(
        enemy_id="wrench",
        display_name="Wrench Terhune",
        archetype="heavy",
        max_hp=105,
        speed=ENEMY_SPEED * 0.85,
        attack_damage=17,
        width=HEAVY_ENEMY_W,
        height=HEAVY_ENEMY_H,
        attack_range_multiplier=1.2,
        attack_timing={
            "windup": 26,
            "active": 10,
            "recovery": ENEMY_ATTACK_RECOVERY,
        },
        score_points=325,
        idle_config=HEAVY_ENEMY_IDLE,
        walk_config=HEAVY_ENEMY_WALK,
        attack_config=HEAVY_ENEMY_ATTACK,
    ),
}


def get_enemy_config(enemy_type):
    return ENEMY_CONFIGS.get(enemy_type, ENEMY_CONFIGS["normal"])
