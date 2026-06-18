from dataclasses import dataclass, replace

from game.settings import *


# todo: move to settings
PLAYER_COUNTER_HIT_STUN_BONUS = 10
# Combo windows are measured from attack start, not from attack finish.
# Because standing punches now have recovery frames, these values include
# attack duration plus the desired follow-up grace period.
PLAYER_COMBO_WINDOW = 29
PLAYER_FIRST_TO_SECOND_COMBO_WINDOW = 29
PLAYER_SECOND_TO_THIRD_COMBO_WINDOW = 24
PLAYER_THIRD_HIT_RECOVERY = 24
PLAYER_CLASH_RECOVERY = 8

@dataclass(frozen=True)
class AttackPhaseData:
    windup: int = 0
    active: int = 0
    recovery: int = 0

    @property
    def total_duration(self):
        return self.windup + self.active + self.recovery


@dataclass(frozen=True)
# x, y is offset relative to base middle of collision box
class AttackHitboxData:
    x: int
    y: int
    width: int
    height: int


PLAYER_ATTACK_HITBOXES = (
    AttackHitboxData(
        x=PLAYER_HIT_BOX_OFFSET_X,
        y=PLAYER_HIT_BOX_OFFSET_Y,
        width=PLAYER_HITBOX_W,
        height=PLAYER_HITBOX_H,
    ),
)
PLAYER_RUN_ATTACK_HITBOXES = (
    AttackHitboxData(
        x=0,
        y=-1 * PLAYER_W,
        width=int(PLAYER_HITBOX_W * 1.2),
        height=int(PLAYER_HITBOX_H * 2),
    ),
)

# deprecated
PLAYER_ATTACK_COUNTER_HURTBOXES = (
    AttackHitboxData(
        x=54,
        y=-300,
        width=34,
        height=38,
    ),
)
PLAYER_RUN_ATTACK_COUNTER_HURTBOXES = (
    AttackHitboxData(x=54, y=-300, width=34, height=38),
)


@dataclass(frozen=True)
class PlayerAttackData:
    damage: int
    duration: int
    phase: AttackPhaseData
    hitboxes: tuple = ()
    counter_hurtboxes: tuple = ()
    max_targets: int = 1
    combo_window: int = ATTACK_COMBO_WINDOW
    action_lock: int = 0
    lane_reach: int = 0
    counter_hit_stun_bonus: int = 0
    knockback_velocity: int = 10
    enemy_hit_stun_duration: int = 15

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
    # should use per enemy design
    hitboxes: tuple = (
        AttackHitboxData(
            x=ENEMY_HITBOX_OFFSET_X,
            y=ENEMY_HITBOX_OFFSET_Y, 
            width=ENEMY_HITBOX_W,
            height=ENEMY_HITBOX_H),
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

PLAYER_ATTACKS = {
    # shorter quick jab hitbox
    "ATTACK_1": PlayerAttackData(
        damage=ATTACK_1_DAMAGE,
        duration=ATTACK_1_WINDUP_DURATION + ATTACK_1_ACTIVE_DURATION + ATTACK_1_RECOVERY_DURATION,
        phase=AttackPhaseData(
            windup=ATTACK_1_WINDUP_DURATION,
            active=ATTACK_1_ACTIVE_DURATION,
            recovery=ATTACK_1_RECOVERY_DURATION),
        hitboxes=PLAYER_ATTACK_HITBOXES,
        counter_hurtboxes=PLAYER_ATTACK_COUNTER_HURTBOXES,
        combo_window=PLAYER_FIRST_TO_SECOND_COMBO_WINDOW,
    ),
    # medium baseline hitbox
    "ATTACK_2": PlayerAttackData(
        damage=ATTACK_2_DAMAGE,
        duration=ATTACK_2_WINDUP_DURATION + ATTACK_2_ACTIVE_DURATION + ATTACK_2_RECOVERY_DURATION,
        phase=AttackPhaseData(
            windup=ATTACK_2_WINDUP_DURATION,
            active=ATTACK_2_ACTIVE_DURATION,
            recovery=ATTACK_2_RECOVERY_DURATION),
        hitboxes=PLAYER_ATTACK_HITBOXES,
        counter_hurtboxes=PLAYER_ATTACK_COUNTER_HURTBOXES,
        combo_window=PLAYER_SECOND_TO_THIRD_COMBO_WINDOW,
    ),
    # wider/taller finisher hitbox. Keep it larger than ATTACK_2, but avoid
    # overextending it because ATTACK_3 also gets a small forward nudge.
    "ATTACK_3": PlayerAttackData(
        damage=ATTACK_3_DAMAGE,
        duration=ATTACK_3_WINDUP_DURATION + ATTACK_3_ACTIVE_DURATION + ATTACK_3_RECOVERY_DURATION,
        phase=AttackPhaseData(
            windup=ATTACK_3_WINDUP_DURATION,
            active=ATTACK_3_ACTIVE_DURATION,
            recovery=ATTACK_3_RECOVERY_DURATION),
        hitboxes=PLAYER_ATTACK_HITBOXES,
        counter_hurtboxes=PLAYER_ATTACK_COUNTER_HURTBOXES,
        combo_window=0,
        action_lock=PLAYER_THIRD_HIT_RECOVERY,
    ),
    "RUN_ATTACK": PlayerAttackData(
        damage=RUN_ATTACK_DAMAGE,
        duration=RUN_ATTACK_TOTAL_DURATION,
        phase=AttackPhaseData(
            windup=RUN_ATTACK_WINDUP_DURATION, 
            active=RUN_ATTACK_ACTIVE_DURATION,
            recovery=RUN_ATTACK_RECOVERY_DURATION),
        hitboxes=PLAYER_RUN_ATTACK_HITBOXES,
        counter_hurtboxes=PLAYER_RUN_ATTACK_COUNTER_HURTBOXES,
        max_targets=3,
        action_lock=RUN_ATTACK_LANDING_RECOVERY,
        knockback_velocity=RUN_ATTACK_BASE_KNOCKBACK,
        enemy_hit_stun_duration=RUN_ATTACK_BASE_ENEMY_HIT_STUN,
    ),
    "JUMP_ATTACK": PlayerAttackData(
        damage=FIST_DAMAGE,
        duration=18,
        phase=AttackPhaseData(windup=4, active=8, recovery=6),
        hitboxes=(AttackHitboxData(x=86, y=-224, width=118, height=58),),
        counter_hurtboxes=(AttackHitboxData(x=-16, y=-268, width=104, height=116),),
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
