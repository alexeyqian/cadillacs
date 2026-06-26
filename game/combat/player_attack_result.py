from game.combat.hit_reaction import HitReaction
from game.settings import (
    FIST_DAMAGE,
    RUN_ATTACK_FULL_POWER_DISTANCE,
    RUN_ATTACK_FULL_POWER_ENEMY_HIT_STUN_BONUS,
    RUN_ATTACK_FULL_POWER_KNOCKBACK_BONUS,
    RUN_ATTACK_REQUIRED_DISTANCE,
)


class PlayerAttackResult:
    def __init__(self):
        pass

    def get_damage(self, owner):
        attack_data = self._get_current_or_state_attack_data(owner)
        if not attack_data:
            return int(FIST_DAMAGE)

        return int(attack_data.damage)

    def get_lane_reach(self, owner):
        attack_data = self._get_current_or_state_attack_data(owner)
        return attack_data.lane_reach if attack_data else 0

    def get_hit_reaction(self, owner):
        return HitReaction(
            stun_frames=self._get_enemy_hit_stun_duration(owner),
            knockback_velocity=self._get_knockback_velocity(owner),
        )

    def _get_knockback_velocity(self, owner):
        attack_data = self._get_current_or_state_attack_data(owner)
        if not attack_data:
            return 10
        return int(
            attack_data.knockback_velocity
            + self._get_run_attack_power_bonus(
                owner,
                RUN_ATTACK_FULL_POWER_KNOCKBACK_BONUS,
            )
        )

    def _get_enemy_hit_stun_duration(self, owner):
        attack_data = self._get_current_or_state_attack_data(owner)
        if not attack_data:
            return 15
        return int(
            attack_data.hit_stun_duration
            + self._get_run_attack_power_bonus(
                owner,
                RUN_ATTACK_FULL_POWER_ENEMY_HIT_STUN_BONUS,
            )
        )

    def _get_run_attack_power_bonus(self, owner, full_power_bonus):
        if owner.combat_state.current_attack_name != owner.RUN_ATTACK:
            return 0

        run_distance = owner.movement.last_run_attack_distance
        bonus_distance = max(
            1,
            RUN_ATTACK_FULL_POWER_DISTANCE - RUN_ATTACK_REQUIRED_DISTANCE,
        )
        bonus_ratio = (run_distance - RUN_ATTACK_REQUIRED_DISTANCE) / bonus_distance
        bonus_ratio = max(0, min(1, bonus_ratio))
        return full_power_bonus * bonus_ratio

    def _get_current_or_state_attack_data(self, owner):
        if owner.combat_state.attack_manager.current_attack:
            return owner.combat_state.attack_manager.current_attack
        return owner.get_attack_data(owner.state)
