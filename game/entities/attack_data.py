from dataclasses import dataclass

from game.settings import *


@dataclass(frozen=True)
class AttackPhaseData:
    windup: int = 0
    active: int = 0
    recovery: int = 0

    @property
    def total_duration(self):
        return self.windup + self.active + self.recovery


@dataclass(frozen=True)
class PlayerAttackData:
    damage: int
    duration: int
    combo_window: int = 30
    action_lock: int = 0
    lane_reach: int = 0
    counter_hit_stun_bonus: int = 0


@dataclass(frozen=True)
class EnemyAttackData:
    damage: float = ENEMY_ATTACK_DAMAGE
    delay: int = ENEMY_ATTACK_DELAY
    cooldown: int = ENEMY_ATTACK_COOLDOWN
    phase: AttackPhaseData = AttackPhaseData(
        windup=ENEMY_ATTACK_WINDUP,
        active=ENEMY_ATTACK_ACTIVE,
        recovery=ENEMY_ATTACK_RECOVERY,
    )
    clash_recovery_duration: int = ENEMY_ATTACK_CLASH_RECOVERY_DURATION
    clash_cooldown_duration: int = ENEMY_ATTACK_CLASH_COOLDOWN_DURATION

    @property
    def windup(self):
        return self.phase.windup

    @property
    def active(self):
        return self.phase.active

    @property
    def recovery(self):
        return self.phase.recovery

    @property
    def total_duration(self):
        return self.phase.total_duration


PLAYER_COUNTER_HIT_STUN_BONUS = 10
PLAYER_COMBO_WINDOW = 30
PLAYER_THIRD_HIT_RECOVERY = 10
PLAYER_CLASH_RECOVERY = 8

PLAYER_ATTACKS = {
    "ATTACK_1": PlayerAttackData(
        damage=FIST_DAMAGE - 2,
        duration=12,
    ),
    "ATTACK_2": PlayerAttackData(
        damage=FIST_DAMAGE,
        duration=12,
    ),
    "ATTACK_3": PlayerAttackData(
        damage=FIST_DAMAGE + 4,
        duration=12,
        combo_window=0,
        action_lock=PLAYER_THIRD_HIT_RECOVERY,
    ),
    "RUN_ATTACK": PlayerAttackData(
        damage=FIST_DAMAGE,
        duration=18,
    ),
    "JUMP_ATTACK": PlayerAttackData(
        damage=FIST_DAMAGE,
        duration=18,
    ),
    # Grab knee is safe once a grab succeeds, so keep it below combo finisher damage.
    "GRAB_KNEE": PlayerAttackData(
        damage=FIST_DAMAGE,
        duration=PLAYER_GRAB_KNEE_DURATION,
    ),
}
