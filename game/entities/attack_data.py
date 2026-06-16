from dataclasses import dataclass, replace

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
class AttackHitboxData:
    x: int
    y: int
    width: int
    height: int


@dataclass(frozen=True)
class PlayerAttackData:
    damage: int
    duration: int
    phase: AttackPhaseData
    hitboxes: tuple = ()
    counter_hurtboxes: tuple = ()
    max_targets: int = 1
    combo_window: int = 30
    action_lock: int = 0
    lane_reach: int = 0
    counter_hit_stun_bonus: int = 0

    @property
    def windup(self):
        return self.phase.windup

    @property
    def active(self):
        return self.phase.active

    @property
    def recovery(self):
        return self.phase.recovery


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
    hitboxes: tuple = (
        AttackHitboxData(x=72, y=-272, width=120, height=40),
    )
    max_targets: int = 1
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

    @property
    def duration(self):
        return self.total_duration


PLAYER_COUNTER_HIT_STUN_BONUS = 10
PLAYER_COMBO_WINDOW = 26
PLAYER_FIRST_TO_SECOND_COMBO_WINDOW = 26
PLAYER_SECOND_TO_THIRD_COMBO_WINDOW = 19
PLAYER_THIRD_HIT_RECOVERY = 24
PLAYER_CLASH_RECOVERY = 8

PLAYER_ATTACKS = {
    "ATTACK_1": PlayerAttackData(
        damage=FIST_DAMAGE - 2,
        duration=12,
        phase=AttackPhaseData(windup=8, active=4, recovery=0),
        hitboxes=(AttackHitboxData(x=94, y=-300, width=160, height=40),),
        counter_hurtboxes=(AttackHitboxData(x=54, y=-300, width=40, height=40),),
        combo_window=PLAYER_FIRST_TO_SECOND_COMBO_WINDOW,
    ),
    "ATTACK_2": PlayerAttackData(
        damage=FIST_DAMAGE,
        duration=12,
        phase=AttackPhaseData(windup=8, active=4, recovery=0),
        hitboxes=(AttackHitboxData(x=94, y=-300, width=160, height=40),),
        counter_hurtboxes=(AttackHitboxData(x=54, y=-300, width=40, height=40),),
        combo_window=PLAYER_SECOND_TO_THIRD_COMBO_WINDOW,
    ),
    "ATTACK_3": PlayerAttackData(
        damage=FIST_DAMAGE + 4,
        duration=12,
        phase=AttackPhaseData(windup=8, active=4, recovery=0),
        hitboxes=(AttackHitboxData(x=94, y=-300, width=160, height=40),),
        counter_hurtboxes=(AttackHitboxData(x=54, y=-300, width=40, height=40),),
        combo_window=0,
        action_lock=PLAYER_THIRD_HIT_RECOVERY,
    ),
    "RUN_ATTACK": PlayerAttackData(
        damage=FIST_DAMAGE,
        duration=18,
        phase=AttackPhaseData(windup=8, active=6, recovery=4),
        hitboxes=(AttackHitboxData(x=40, y=-220, width=160, height=80),),
    ),
    "JUMP_ATTACK": PlayerAttackData(
        damage=FIST_DAMAGE,
        duration=18,
        phase=AttackPhaseData(windup=8, active=6, recovery=4),
        hitboxes=(AttackHitboxData(x=40, y=-220, width=160, height=80),),
    ),
    # Grab knee is safe once a grab succeeds, so keep it below combo finisher damage.
    "GRAB_KNEE": PlayerAttackData(
        damage=FIST_DAMAGE,
        duration=PLAYER_GRAB_KNEE_DURATION,
        phase=AttackPhaseData(windup=6, active=4, recovery=4),
        hitboxes=(AttackHitboxData(x=50, y=-190, width=60, height=60),),
    ),
}

WEAPON_PLAYER_ATTACKS = {
    ("knife", "ATTACK_1"): replace(
        PLAYER_ATTACKS["ATTACK_1"],
        damage=PLAYER_ATTACKS["ATTACK_1"].damage + KNIFE_DAMAGE,
        hitboxes=(AttackHitboxData(x=90, y=-304, width=200, height=44),),
        lane_reach=1,
    ),
    ("knife", "ATTACK_2"): replace(
        PLAYER_ATTACKS["ATTACK_2"],
        damage=PLAYER_ATTACKS["ATTACK_2"].damage + KNIFE_DAMAGE,
        hitboxes=(AttackHitboxData(x=90, y=-304, width=200, height=44),),
        lane_reach=1,
    ),
    ("knife", "ATTACK_3"): replace(
        PLAYER_ATTACKS["ATTACK_3"],
        damage=PLAYER_ATTACKS["ATTACK_3"].damage + KNIFE_DAMAGE,
        hitboxes=(AttackHitboxData(x=90, y=-304, width=210, height=48),),
        lane_reach=1,
    ),
    ("bat", "ATTACK_1"): replace(
        PLAYER_ATTACKS["ATTACK_1"],
        damage=PLAYER_ATTACKS["ATTACK_1"].damage + BAT_DAMAGE,
        hitboxes=(AttackHitboxData(x=80, y=-316, width=250, height=64),),
        lane_reach=1,
        max_targets=2,
    ),
    ("bat", "ATTACK_2"): replace(
        PLAYER_ATTACKS["ATTACK_2"],
        damage=PLAYER_ATTACKS["ATTACK_2"].damage + BAT_DAMAGE,
        hitboxes=(AttackHitboxData(x=80, y=-316, width=250, height=64),),
        lane_reach=1,
        max_targets=2,
    ),
    ("bat", "ATTACK_3"): replace(
        PLAYER_ATTACKS["ATTACK_3"],
        damage=PLAYER_ATTACKS["ATTACK_3"].damage + BAT_DAMAGE,
        hitboxes=(AttackHitboxData(x=72, y=-320, width=280, height=72),),
        lane_reach=1,
        max_targets=2,
    ),
}


def get_player_attack_data(attack_name, weapon=None):
    if weapon and not getattr(weapon, "is_ranged", False):
        weapon_type = getattr(weapon, "weapon_type", None)
        weapon_attack = WEAPON_PLAYER_ATTACKS.get((weapon_type, attack_name))
        if weapon_attack:
            return weapon_attack

    return PLAYER_ATTACKS.get(attack_name)
