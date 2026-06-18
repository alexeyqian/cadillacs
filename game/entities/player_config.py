from dataclasses import dataclass, replace
from game.settings import *
from game.entities.attack_data import *


DEFAULT_PLAYER_ATTACKS = {
    # shorter quick jab hitbox
    "ATTACK_1": replace(
        DEFAULT_PLAYER_ATTACK_DATA,
        damage=ATTACK_1_DAMAGE,
        windup=ATTACK_1_WINDUP_DURATION,
        active=ATTACK_1_ACTIVE_DURATION,
        recovery=ATTACK_1_RECOVERY_DURATION,

        # hardcode for now
        hitbox_offset_x=60,
        hitbox_offset_y=-320,
        hitbox_w=200,
        hitbox_h=60,
        
        #hitbox_offset_x=PLAYER_HIT_BOX_OFFSET_X,
        #hitbox_offset_y=PLAYER_HIT_BOX_OFFSET_Y,
        #hitbox_w=PLAYER_HITBOX_W,
        #hitbox_h=PLAYER_HITBOX_H,

        combo_window=PLAYER_FIRST_TO_SECOND_COMBO_WINDOW,
    ),
    # medium baseline hitbox
    "ATTACK_2": replace(
        DEFAULT_PLAYER_ATTACK_DATA,
        damage=ATTACK_2_DAMAGE,
        windup=ATTACK_2_WINDUP_DURATION,
        active=ATTACK_2_ACTIVE_DURATION,
        recovery=ATTACK_2_RECOVERY_DURATION,
        hitbox_offset_x=PLAYER_HIT_BOX_OFFSET_X,
        hitbox_offset_y=PLAYER_HIT_BOX_OFFSET_Y,
        hitbox_w=PLAYER_HITBOX_W,
        hitbox_h=PLAYER_HITBOX_H,
        combo_window=PLAYER_SECOND_TO_THIRD_COMBO_WINDOW,
    ),
    # wider/taller finisher hitbox. Keep it larger than ATTACK_2, but avoid
    # overextending it because ATTACK_3 also gets a small forward nudge.
    "ATTACK_3": replace(
        DEFAULT_PLAYER_ATTACK_DATA,
        damage=ATTACK_3_DAMAGE,
        windup=ATTACK_3_WINDUP_DURATION,
        active=ATTACK_3_ACTIVE_DURATION,
        recovery=ATTACK_3_RECOVERY_DURATION,
        hitbox_offset_x=PLAYER_HIT_BOX_OFFSET_X,
        hitbox_offset_y=PLAYER_HIT_BOX_OFFSET_Y,
        hitbox_w=PLAYER_HITBOX_W,
        hitbox_h=PLAYER_HITBOX_H,
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
        active=RUN_ATTACK_ACTIVE_DURATION,
        recovery=RUN_ATTACK_RECOVERY_DURATION,
        
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
}

# todo: should get from owner
def get_player_attack_data(attack_name, weapon=None):
    return DEFAULT_PLAYER_ATTACKS.get(attack_name)

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
    hurt_box_w: int = PLAYER_HURTBOX_H
    hurt_box_h: int = PLAYER_HURTBOX_H

    speed: float = PLAYER_SPEED
    run_speed: float = PLAYER_RUN_SPEED
    
    attack: AttackData = DEFAULT_PLAYER_ATTACKS["ATTACK_1"]
    run_attack_damage: int = RUN_ATTACK_DAMAGE

    # TODO: move to settings constant
    jump_attack_damage: int = JUMP_ATTACK_DAMAGE
    jump_power: float = 12
    jump_gravity: float = 0.7
    air_move_speed: float = 3.0
    jump_takeoff_frames: int = 6
    landing_recovery_frames: int = 6

    grab_range: int = PLAYER_GRAB_RANGE
    hit_stun_duration: int = ATTACK_1_HIT_STUN_DURATION
    sprite_scale: int = 2


PLAYER_CONFIGS = {
    "mustapha": PlayerConfig(
        player_id="mustapha",
        display_name="Mustapha",
    ),
}


def get_player_config(player_type):
    return PLAYER_CONFIGS.get(player_type, PLAYER_CONFIGS["mustapha"])
