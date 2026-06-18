from dataclasses import dataclass

from game.settings import *

@dataclass(frozen=True)
class PlayerAttackData:
    hitbox_offset_x: int = PLAYER_HIT_BOX_OFFSET_X
    hitbox_offset_y: int = PLAYER_HIT_BOX_OFFSET_Y
    hitbox_w: int = PLAYER_HITBOX_W
    hitbox_h: int = PLAYER_HITBOX_H

    damage: int = ATTACK_1_DAMAGE
    duration: int = ATTACK_1_WINDUP_DURATION + ATTACK_1_ACTIVE_DURATION + ATTACK_1_RECOVERY_DURATION
    windup: int = ATTACK_1_WINDUP_DURATION
    active: int = ATTACK_1_ACTIVE_DURATION
    recovery: int = ATTACK_1_RECOVERY_DURATION
    cooldown: int = ATTACK_1_COOLDOWN
    
    # todo: replace with cooldown
    action_lock: int = 0 # cooldown

    max_targets: int = 1
    combo_window: int = ATTACK_COMBO_WINDOW

    lane_reach: int = 0
    counter_hit_stun_bonus: int = 0
    knockback_velocity: int = 10
    enemy_hit_stun_duration: int = 15
    
    # deprecated fields
    counter_hurtbox_offset_x: int = 0
    counter_hurtbox_offset_y: int = 0
    counter_hurtbox_w: int = 0
    counter_hurtbox_h: int = 0

    @property
    def total_duration(self):
        return self.windup + self.active + self.recovery

@dataclass(frozen=True)
class EnemyAttackData:
    hitbox_offset_x: int = ENEMY_HITBOX_OFFSET_X
    hitbox_offset_y: int = ENEMY_HITBOX_OFFSET_Y
    hitbox_w: int = ENEMY_HITBOX_W
    hitbox_h: int = ENEMY_HITBOX_H

    delay: int = ENEMY_ATTACK_DELAY

    damage: float = ENEMY_ATTACK_DAMAGE
    windup: int = ENEMY_ATTACK_WINDUP
    active: int = ENEMY_ATTACK_ACTIVE
    recovery: int = ENEMY_ATTACK_RECOVERY
    cooldown: int = ENEMY_ATTACK_COOLDOWN

    @property
    def total_duration(self):
        return self.windup + self.active + self.recovery
