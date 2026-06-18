from dataclasses import dataclass

from game.settings import *


@dataclass(frozen=True)
class AttackData:
    hitbox_offset_x: int
    hitbox_offset_y: int
    hitbox_w: int
    hitbox_h: int

    delay: int
    damage: float
    windup: int
    active: int
    recovery: int
    cooldown: int

    hit_stun_duration: int
    knockback_velocity: int
    lane_reach: int
    max_targets: int
    combo_window: int

    @property
    def total_duration(self):
        return self.windup + self.active + self.recovery


DEFAULT_PLAYER_ATTACK_DATA = AttackData(
    hitbox_offset_x=PLAYER_HIT_BOX_OFFSET_X,
    hitbox_offset_y=PLAYER_HIT_BOX_OFFSET_Y,
    hitbox_w=PLAYER_HITBOX_W,
    hitbox_h=PLAYER_HITBOX_H,
    delay=0,
    damage=ATTACK_1_DAMAGE,
    windup=ATTACK_1_WINDUP_DURATION,
    active=ATTACK_1_ACTIVE_DURATION,
    recovery=ATTACK_1_RECOVERY_DURATION,
    cooldown=0,
    hit_stun_duration=15,
    knockback_velocity=10,
    lane_reach=1,
    max_targets=1,
    combo_window=ATTACK_COMBO_WINDOW,
)


DEFAULT_ENEMY_ATTACK_DATA = AttackData(
    hitbox_offset_x=ENEMY_HITBOX_OFFSET_X,
    hitbox_offset_y=ENEMY_HITBOX_OFFSET_Y,
    hitbox_w=ENEMY_HITBOX_W,
    hitbox_h=ENEMY_HITBOX_H,
    delay=ENEMY_ATTACK_DELAY,
    damage=ENEMY_ATTACK_DAMAGE,
    windup=ENEMY_ATTACK_WINDUP,
    active=ENEMY_ATTACK_ACTIVE,
    recovery=ENEMY_ATTACK_RECOVERY,
    cooldown=ENEMY_ATTACK_COOLDOWN,
    hit_stun_duration=0,
    knockback_velocity=0,
    lane_reach=0,
    max_targets=1,
    combo_window=ATTACK_COMBO_WINDOW,
)
