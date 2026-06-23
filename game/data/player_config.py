from dataclasses import dataclass, replace
from game.combat.attack_data import AttackData, DEFAULT_PLAYER_ATTACK_DATA
from game.settings import (
    ATTACK_1_ACTIVE_DURATION,
    ATTACK_1_DAMAGE,
    ATTACK_1_HIT_STUN_DURATION,
    ATTACK_1_WINDUP_DURATION,
    ATTACK_2_ACTIVE_DURATION,
    ATTACK_2_DAMAGE,
    ATTACK_2_WINDUP_DURATION,
    ATTACK_3_ACTIVE_DURATION,
    ATTACK_3_DAMAGE,
    ATTACK_3_WINDUP_DURATION,
    BAT_DAMAGE,
    FIST_DAMAGE,
    KNIFE_DAMAGE,
    PLAYER_COLLISION_H,
    PLAYER_COLLISION_W,
    PLAYER_GRAB_RANGE,
    PLAYER_H,
    PLAYER_HITBOX_H,
    PLAYER_HITBOX_W,
    PLAYER_HIT_BOX_OFFSET_X,
    PLAYER_HIT_BOX_OFFSET_Y,
    PLAYER_HURTBOX_H,
    PLAYER_HURTBOX_OFFSET_X,
    PLAYER_HURTBOX_OFFSET_Y,
    PLAYER_HURTBOX_W,
    PLAYER_LIVES,
    PLAYER_MAX_HP,
    PLAYER_SPEED,
    PLAYER_RUN_SPEED,
    PLAYER_AIR_MOVE_SPEED,
    PLAYER_THIRD_HIT_RECOVERY,
    PLAYER_W,
    RUN_ATTACK_BASE_ENEMY_HIT_STUN,
    RUN_ATTACK_BASE_KNOCKBACK,
    RUN_ATTACK_DAMAGE,
    RUN_ATTACK_LANDING_RECOVERY,
    RUN_ATTACK_REQUIRED_DISTANCE,
    RUN_ATTACK_WINDUP_DURATION,
    THROWN_DAMAGE,
)


DEFAULT_PLAYER_ATTACKS = {
    # shorter quick jab hitbox
    "ATTACK": replace(
        DEFAULT_PLAYER_ATTACK_DATA,
        damage=ATTACK_1_DAMAGE,
        windup=ATTACK_1_WINDUP_DURATION,
        active=ATTACK_1_ACTIVE_DURATION,
        recovery=3,

        # hardcode for now
        hitbox_offset_x=60,
        hitbox_offset_y=-320,
        hitbox_w=150,
        hitbox_h=60,
        
        #hitbox_offset_x=PLAYER_HIT_BOX_OFFSET_X,
        #hitbox_offset_y=PLAYER_HIT_BOX_OFFSET_Y,
        #hitbox_w=PLAYER_HITBOX_W,
        #hitbox_h=PLAYER_HITBOX_H,

        combo_window=13, # difficult: 22 -> 13
    ),
    # medium baseline hitbox
    "ATTACK2": replace(
        DEFAULT_PLAYER_ATTACK_DATA,
        damage=ATTACK_2_DAMAGE,
        windup=ATTACK_2_WINDUP_DURATION,
        active=ATTACK_2_ACTIVE_DURATION,
        recovery=5,
        hitbox_offset_x=PLAYER_HIT_BOX_OFFSET_X,
        hitbox_offset_y=PLAYER_HIT_BOX_OFFSET_Y,
        hitbox_w=PLAYER_HITBOX_W,
        hitbox_h=PLAYER_HITBOX_H,
        combo_window=15, # difficult: 30 -> 15
    ),
    # wider/taller finisher hitbox. Keep it larger than ATTACK2, but avoid
    # overextending it because ATTACK3 also gets a small forward nudge.
    "ATTACK3": replace(
        DEFAULT_PLAYER_ATTACK_DATA,
        damage=ATTACK_3_DAMAGE,
        windup=ATTACK_3_WINDUP_DURATION,
        active=ATTACK_3_ACTIVE_DURATION,
        recovery=6,
        hitbox_offset_x=PLAYER_HIT_BOX_OFFSET_X,
        hitbox_offset_y=PLAYER_HIT_BOX_OFFSET_Y,
        hitbox_w=PLAYER_HITBOX_W + 20,
        hitbox_h=PLAYER_HITBOX_H + 20,
        combo_window=0,
        cooldown=PLAYER_THIRD_HIT_RECOVERY,
    ),
    "RUN_ATTACK": replace(
        DEFAULT_PLAYER_ATTACK_DATA,
        hitbox_offset_x=40,
        hitbox_offset_y=-250,
        hitbox_w=200,
        hitbox_h=100,

        damage=RUN_ATTACK_DAMAGE,
        windup=RUN_ATTACK_WINDUP_DURATION,
        active=10,
        recovery=4,
        
        max_targets=3,
        cooldown=RUN_ATTACK_LANDING_RECOVERY,
        knockback_velocity=RUN_ATTACK_BASE_KNOCKBACK,
        hit_stun_duration=RUN_ATTACK_BASE_ENEMY_HIT_STUN,
    ),
    "JUMP_ATTACK": replace(
        DEFAULT_PLAYER_ATTACK_DATA,
        damage=FIST_DAMAGE,
        windup=4,
        active=8,
        recovery=6,
        hitbox_offset_x=86,
        hitbox_offset_y=-224,
        hitbox_w=118,
        hitbox_h=58,
    ),
    # Grab knee is safe once a grab succeeds, so keep it below combo finisher damage.
    "GRAB_KNEE": replace(
        DEFAULT_PLAYER_ATTACK_DATA,
        damage=FIST_DAMAGE,
        windup=6,
        active=4,
        recovery=4,
        hitbox_offset_x=50,
        hitbox_offset_y=-190,
        hitbox_w=60,
        hitbox_h=60,
    ),
    "THROW": replace(
        DEFAULT_PLAYER_ATTACK_DATA,
        damage=THROWN_DAMAGE,
        windup=0,
        active=1,
        recovery=0,
        cooldown=0,
        hitbox_w=0,
        hitbox_h=0,
        hit_stun_duration=0,
        knockback_velocity=0,
        lane_reach=0,
        combo_window=0,
    ),
}

DEFAULT_WEAPON_PLAYER_ATTACKS = {
    ("knife", "ATTACK"): replace(
        DEFAULT_PLAYER_ATTACKS["ATTACK"],
        damage=DEFAULT_PLAYER_ATTACKS["ATTACK"].damage + KNIFE_DAMAGE,
        lane_reach=1,
    ),
    ("knife", "ATTACK2"): replace(
        DEFAULT_PLAYER_ATTACKS["ATTACK2"],
        damage=DEFAULT_PLAYER_ATTACKS["ATTACK2"].damage + KNIFE_DAMAGE,
        lane_reach=1,
    ),
    ("knife", "ATTACK3"): replace(
        DEFAULT_PLAYER_ATTACKS["ATTACK3"],
        damage=DEFAULT_PLAYER_ATTACKS["ATTACK3"].damage + KNIFE_DAMAGE,
        lane_reach=1,
    ),
    ("bat", "ATTACK"): replace(
        DEFAULT_PLAYER_ATTACKS["ATTACK"],
        damage=DEFAULT_PLAYER_ATTACKS["ATTACK"].damage + BAT_DAMAGE,
        max_targets=2,
        lane_reach=1,
    ),
    ("bat", "ATTACK2"): replace(
        DEFAULT_PLAYER_ATTACKS["ATTACK2"],
        damage=DEFAULT_PLAYER_ATTACKS["ATTACK2"].damage + BAT_DAMAGE,
        max_targets=2,
        lane_reach=1,
    ),
    ("bat", "ATTACK3"): replace(
        DEFAULT_PLAYER_ATTACKS["ATTACK3"],
        damage=DEFAULT_PLAYER_ATTACKS["ATTACK3"].damage + BAT_DAMAGE,
        max_targets=2,
        lane_reach=1,
    ),
}

DEFAULT_PLAYER_TYPE = "mustapha"

@dataclass(frozen=True)
class PlayerConfig:
    player_id: str
    display_name: str
    lives: int = PLAYER_LIVES
    max_hp: int = PLAYER_MAX_HP

    width: int = PLAYER_W
    height: int = PLAYER_H
    collision_box_w: int = PLAYER_COLLISION_W
    collision_box_h: int = PLAYER_COLLISION_H
    hurt_box_w: int = PLAYER_HURTBOX_W
    hurt_box_h: int = PLAYER_HURTBOX_H
    hurt_box_offset_x: int = PLAYER_HURTBOX_OFFSET_X
    hurt_box_offset_y: int = PLAYER_HURTBOX_OFFSET_Y

    speed: float = PLAYER_SPEED
    run_speed: float = PLAYER_RUN_SPEED
    run_attack_min_distance: float = RUN_ATTACK_REQUIRED_DISTANCE

    attacks: dict = None
    weapon_attacks: dict = None
    attack: AttackData = DEFAULT_PLAYER_ATTACKS["ATTACK"]
    jump_power: float = 12
    jump_gravity: float = 0.7
    air_move_speed: float = PLAYER_AIR_MOVE_SPEED
    jump_takeoff_frames: int = 6
    landing_recovery_frames: int = 6
    grab_range: int = PLAYER_GRAB_RANGE
    hit_stun_duration: int = ATTACK_1_HIT_STUN_DURATION
    sprite_scale: int = 2


PLAYER_CONFIGS = {
    "mustapha": PlayerConfig(
        player_id="mustapha",
        display_name="Mustapha",
        attacks=DEFAULT_PLAYER_ATTACKS,
        weapon_attacks=DEFAULT_WEAPON_PLAYER_ATTACKS,
    ),
}


def get_player_config(player_type):
    return PLAYER_CONFIGS.get(player_type, PLAYER_CONFIGS[DEFAULT_PLAYER_TYPE])
