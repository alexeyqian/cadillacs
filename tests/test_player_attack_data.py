import unittest

from game.data.player_config import DEFAULT_PLAYER_ATTACKS, DEFAULT_WEAPON_PLAYER_ATTACKS
import game.settings as settings
from game.controllers.player_combat_controller import PlayerCombatController
from game.input.player_input_state import PlayerInputState
from game.managers.score_manager import ScoreManager
from game.settings import (
    PLAYER_GRAB_KNEE_ACTIVE_DURATION,
    PLAYER_GRAB_KNEE_DURATION,
    PLAYER_GRAB_KNEE_RECOVERY_DURATION,
    PLAYER_GRAB_KNEE_WINDUP_DURATION,
    RUN_ATTACK_FULL_POWER_DISTANCE,
    RUN_ATTACK_FULL_POWER_KNOCKBACK_BONUS,
    RUN_ATTACK_LANDING_RECOVERY,
)


class FakeMovement:
    def __init__(self):
        self.is_running = False
        self.is_jumping = False
        self.run_attack_momentum_started = False
        self.can_run_attack = False
        self.last_run_attack_distance = 0
        self.combo_finisher_nudge_started = False
        self.run_attack_cooldown_started = False

    def can_start_run_attack(self):
        return self.can_run_attack

    def start_run_attack_momentum(self, owner):
        self.run_attack_momentum_started = True

    def start_run_attack_cooldown(self):
        self.run_attack_cooldown_started = True

    def start_combo_finisher_nudge(self, owner):
        self.combo_finisher_nudge_started = True


class FakeStateMachine:
    def change_to(self, owner, state):
        owner.state = state


class FakeWeapon:
    def __init__(self, weapon_type, is_ranged=False):
        self.weapon_type = weapon_type
        self.is_ranged = is_ranged


class FakeWeaponSlot:
    def __init__(self):
        self.weapon = None


class FakeOwner:
    IDLE = "IDLE"
    JUMP_TAKEOFF = "JUMP_TAKEOFF"
    ATTACK = "ATTACK"
    ATTACK2 = "ATTACK2"
    ATTACK3 = "ATTACK3"
    RUN_ATTACK = "RUN_ATTACK"
    JUMP_ATTACK = "JUMP_ATTACK"
    RECOIL = "RECOIL"
    LANDING = "LANDING"
    DEAD = "DEAD"

    def __init__(self):
        self.state = self.IDLE
        self.movement = FakeMovement()
        self.state_machine = FakeStateMachine()
        self.weapon_slot = FakeWeaponSlot()
        self.attacks = DEFAULT_PLAYER_ATTACKS
        self.weapon_attacks = DEFAULT_WEAPON_PLAYER_ATTACKS
        self.input_state = PlayerInputState()
        self.air = None

    def get_attack_data(self, attack_name):
        weapon = getattr(self.weapon_slot, "weapon", None)
        weapon_type = getattr(weapon, "weapon_type", weapon)
        weapon_attack = self.weapon_attacks.get((weapon_type, attack_name))
        if weapon_attack and not getattr(weapon, "is_ranged", False):
            return weapon_attack
        return self.attacks.get(attack_name)


class AttackDataTests(unittest.TestCase):
    def finish_connected_attack(self, combat, owner):
        combat.attack_manager.has_connected = True
        for _ in range(combat.attack_manager.remaining_frames):
            combat.advance_timers(owner)
            combat.update_attack(owner)

    def finish_missed_attack(self, combat, owner):
        for _ in range(combat.attack_manager.remaining_frames):
            combat.advance_timers(owner)
            combat.update_attack(owner)

    def remaining_followup_window_after_attack(self, attack):
        return max(0, attack.combo_window - attack.total_duration)

    def test_standing_attack_duration_comes_from_attack_data(self):
        owner = FakeOwner()
        combat = PlayerCombatController()

        combat.start_attack(owner)

        self.assertEqual(owner.state, owner.ATTACK)
        self.assertEqual(combat.current_attack_name, owner.ATTACK)
        self.assertEqual(combat.attack_manager.elapsed_frames, 0)
        self.assertEqual(
            combat.attack_manager.remaining_frames,
            DEFAULT_PLAYER_ATTACKS["ATTACK"].total_duration,
        )

    def test_attack_debug_accessors_use_active_attack_data(self):
        owner = FakeOwner()
        combat = PlayerCombatController()

        combat.start_attack(owner)

        attack = DEFAULT_PLAYER_ATTACKS["ATTACK"]
        self.assertEqual(combat.get_attack_data(owner), attack)
        self.assertEqual(combat.get_attack_damage(owner), attack.damage)
        self.assertEqual(combat.get_attack_lane_reach(owner), attack.lane_reach)

    def test_attack_debug_accessors_are_safe_when_idle(self):
        owner = FakeOwner()
        combat = PlayerCombatController()

        self.assertIsNone(combat.get_attack_data(owner))
        self.assertEqual(combat.get_attack_damage(owner), 0)
        self.assertEqual(combat.get_attack_lane_reach(owner), 0)

    def test_running_attack_duration_comes_from_attack_data(self):
        owner = FakeOwner()
        owner.movement.is_running = True
        owner.movement.can_run_attack = True
        combat = PlayerCombatController()

        combat.start_attack(owner)

        self.assertEqual(owner.state, owner.RUN_ATTACK)
        self.assertEqual(combat.current_attack_name, owner.RUN_ATTACK)
        self.assertEqual(
            combat.attack_manager.remaining_frames,
            DEFAULT_PLAYER_ATTACKS["RUN_ATTACK"].total_duration,
        )
        self.assertTrue(owner.movement.run_attack_momentum_started)

        self.finish_connected_attack(combat, owner)

        self.assertTrue(owner.movement.run_attack_cooldown_started)

    def test_running_attack_has_arcade_style_timing_and_landing_recovery(self):
        attack = DEFAULT_PLAYER_ATTACKS["RUN_ATTACK"]

        self.assertEqual(attack.windup, 4)
        self.assertEqual(attack.active, 10)
        self.assertEqual(attack.recovery, 4)
        self.assertEqual(attack.cooldown, RUN_ATTACK_LANDING_RECOVERY)

    def test_running_attack_requires_enough_run_distance(self):
        owner = FakeOwner()
        owner.movement.is_running = True
        owner.movement.can_run_attack = False
        combat = PlayerCombatController()

        combat.start_attack(owner)

        self.assertEqual(owner.state, owner.ATTACK)
        self.assertEqual(combat.current_attack_name, owner.ATTACK)
        self.assertFalse(owner.movement.run_attack_momentum_started)

    def test_running_attack_knockback_scales_with_run_distance(self):
        owner = FakeOwner()
        owner.movement.can_run_attack = True
        owner.movement.last_run_attack_distance = RUN_ATTACK_FULL_POWER_DISTANCE
        combat = PlayerCombatController()

        combat.start_attack(owner)

        self.assertEqual(
            combat.attack_result.get_hit_reaction(owner).knockback_velocity,
            DEFAULT_PLAYER_ATTACKS["RUN_ATTACK"].knockback_velocity
            + RUN_ATTACK_FULL_POWER_KNOCKBACK_BONUS,
        )

    def test_running_attack_has_stronger_knockback_than_normal_punch(self):
        self.assertGreater(
            DEFAULT_PLAYER_ATTACKS["RUN_ATTACK"].knockback_velocity,
            DEFAULT_PLAYER_ATTACKS["ATTACK"].knockback_velocity,
        )

    def test_running_attack_has_longer_enemy_hit_stun_than_normal_punch(self):
        self.assertGreater(
            DEFAULT_PLAYER_ATTACKS["RUN_ATTACK"].hit_stun_duration,
            DEFAULT_PLAYER_ATTACKS["ATTACK"].hit_stun_duration,
        )

    def test_running_attack_can_hit_multiple_targets(self):
        self.assertGreater(
            DEFAULT_PLAYER_ATTACKS["RUN_ATTACK"].max_targets,
            DEFAULT_PLAYER_ATTACKS["ATTACK"].max_targets,
        )

    def test_jump_attack_duration_comes_from_attack_data(self):
        owner = FakeOwner()
        owner.movement.is_jumping = True
        combat = PlayerCombatController()

        combat.start_jump_attack(owner)

        self.assertEqual(owner.state, owner.JUMP_ATTACK)
        self.assertEqual(combat.current_attack_name, owner.JUMP_ATTACK)
        self.assertEqual(
            combat.attack_manager.remaining_frames,
            DEFAULT_PLAYER_ATTACKS["JUMP_ATTACK"].total_duration,
        )

    def test_jump_attack_cannot_start_during_takeoff(self):
        class FakeAir:
            def can_start_jump_attack(self):
                return False

        owner = FakeOwner()
        owner.state = owner.JUMP_TAKEOFF
        owner.movement.is_jumping = True
        owner.air = FakeAir()
        combat = PlayerCombatController()

        combat.start_jump_attack(owner)

        self.assertEqual(owner.state, owner.JUMP_TAKEOFF)
        self.assertIsNone(combat.current_attack_name)

    def test_jump_attack_can_only_start_once_per_jump(self):
        class FakeAir:
            def __init__(self):
                self.has_used_jump_attack = False

            def can_start_jump_attack(self):
                return not self.has_used_jump_attack

            def mark_jump_attack_used(self):
                self.has_used_jump_attack = True

        owner = FakeOwner()
        owner.movement.is_jumping = True
        owner.air = FakeAir()
        combat = PlayerCombatController()

        combat.start_jump_attack(owner)
        combat.cancel_attack()
        combat.start_jump_attack(owner)

        self.assertEqual(owner.state, owner.JUMP_ATTACK)
        self.assertIsNone(combat.current_attack_name)
        self.assertTrue(owner.air.has_used_jump_attack)

    def test_jump_attack_uses_flying_kick_timing(self):
        attack = DEFAULT_PLAYER_ATTACKS["JUMP_ATTACK"]

        self.assertEqual(attack.windup, 4)
        self.assertEqual(attack.active, 8)
        self.assertEqual(attack.recovery, 6)

    def test_grab_knee_timing_comes_from_settings(self):
        attack = DEFAULT_PLAYER_ATTACKS["GRAB_KNEE"]

        self.assertEqual(attack.windup, PLAYER_GRAB_KNEE_WINDUP_DURATION)
        self.assertEqual(attack.active, PLAYER_GRAB_KNEE_ACTIVE_DURATION)
        self.assertEqual(attack.recovery, PLAYER_GRAB_KNEE_RECOVERY_DURATION)
        self.assertEqual(attack.total_duration, PLAYER_GRAB_KNEE_DURATION)

    def test_attack_timer_counts_up_until_attack_finishes(self):
        owner = FakeOwner()
        combat = PlayerCombatController()

        combat.start_attack(owner)
        combat.update_attack(owner)

        self.assertEqual(combat.attack_manager.elapsed_frames, 1)
        self.assertEqual(
            combat.attack_manager.remaining_frames,
            DEFAULT_PLAYER_ATTACKS["ATTACK"].total_duration - 1,
        )

        for _ in range(DEFAULT_PLAYER_ATTACKS["ATTACK"].total_duration - 1):
            combat.update_attack(owner)

        self.assertFalse(combat.is_attacking)
        self.assertEqual(combat.attack_manager.elapsed_frames, 0)
        self.assertEqual(owner.state, owner.IDLE)

    def test_standing_combo_attacks_have_recovery_frames(self):
        self.assertEqual(DEFAULT_PLAYER_ATTACKS["ATTACK"].recovery, 3)
        self.assertEqual(DEFAULT_PLAYER_ATTACKS["ATTACK2"].recovery, 5)
        self.assertEqual(DEFAULT_PLAYER_ATTACKS["ATTACK3"].recovery, 6)

    def test_standing_combo_windows_are_defined_on_attack_data(self):
        self.assertEqual(DEFAULT_PLAYER_ATTACKS["ATTACK"].combo_window, 13)
        self.assertEqual(DEFAULT_PLAYER_ATTACKS["ATTACK2"].combo_window, 15)
        self.assertEqual(DEFAULT_PLAYER_ATTACKS["ATTACK3"].combo_window, 0)

    def test_standing_combo_hitboxes_progress_from_jab_to_finisher(self):
        attack = DEFAULT_PLAYER_ATTACKS["ATTACK"]
        attack2 = DEFAULT_PLAYER_ATTACKS["ATTACK2"]
        attack3 = DEFAULT_PLAYER_ATTACKS["ATTACK3"]

        self.assertLess(attack.hitbox_w, attack2.hitbox_w)
        self.assertGreater(attack3.hitbox_w, attack2.hitbox_w)
        self.assertGreater(attack3.hitbox_h, attack2.hitbox_h)
        self.assertLessEqual(attack3.hitbox_w, attack2.hitbox_w + 20)

    def test_player_attack_is_inactive_during_recovery(self):
        owner = FakeOwner()
        combat = PlayerCombatController()
        attack = DEFAULT_PLAYER_ATTACKS["ATTACK"]

        combat.start_attack(owner)
        for _ in range(attack.windup + attack.active):
            combat.update_attack(owner)

        self.assertTrue(combat.is_attacking)
        self.assertFalse(combat.attack_manager.is_active())
        self.assertEqual(combat.attack_manager.get_phase_name(), "RECOVERY")

    def test_player_combat_controller_uses_per_target_hit_tracking(self):
        first_target = object()
        second_target = object()
        owner = FakeOwner()
        combat = PlayerCombatController()

        combat.start_attack(owner)

        self.assertTrue(combat.can_hit_target(first_target))
        combat.mark_attack_hit(first_target)

        self.assertFalse(combat.can_hit_target(first_target))
        self.assertFalse(combat.can_hit_target(second_target))

    def test_knife_attack_uses_weapon_attack_data(self):
        owner = FakeOwner()
        owner.weapon_slot.weapon = FakeWeapon("knife")
        combat = PlayerCombatController()

        combat.start_attack(owner)

        self.assertEqual(
            combat.attack_manager.current_attack,
            DEFAULT_WEAPON_PLAYER_ATTACKS[("knife", owner.ATTACK)],
        )
        self.assertEqual(
            combat.attack_result.get_damage(owner),
            DEFAULT_WEAPON_PLAYER_ATTACKS[("knife", owner.ATTACK)].damage,
        )
        self.assertEqual(combat.attack_result.get_lane_reach(owner), 1)

    def test_bat_attack_can_hit_two_targets_from_weapon_attack_data(self):
        owner = FakeOwner()
        owner.weapon_slot.weapon = FakeWeapon("bat")
        combat = PlayerCombatController()

        combat.start_attack(owner)

        self.assertEqual(
            combat.attack_manager.current_attack,
            DEFAULT_WEAPON_PLAYER_ATTACKS[("bat", owner.ATTACK)],
        )
        self.assertEqual(combat.attack_manager.current_attack.max_targets, 2)

    def test_ranged_weapon_does_not_change_melee_attack_data(self):
        owner = FakeOwner()
        owner.weapon_slot.weapon = FakeWeapon("pistol", is_ranged=True)
        combat = PlayerCombatController()

        combat.start_attack(owner)

        self.assertEqual(combat.attack_manager.current_attack, DEFAULT_PLAYER_ATTACKS["ATTACK"])

    def test_second_combo_hit_allows_moderate_followup_delay(self):
        owner = FakeOwner()
        combat = PlayerCombatController()

        combat.start_attack(owner)
        self.finish_connected_attack(combat, owner)
        for _ in range(self.remaining_followup_window_after_attack(DEFAULT_PLAYER_ATTACKS["ATTACK"]) - 1):
            combat.advance_timers(owner)
        combat.start_attack(owner)

        self.assertEqual(owner.state, owner.ATTACK2)

    def test_missed_combo_can_continue_when_debug_flag_enabled(self):
        owner = FakeOwner()
        combat = PlayerCombatController()

        combat.start_attack(owner)
        self.finish_missed_attack(combat, owner)
        combat.start_attack(owner)

        self.assertEqual(owner.state, owner.ATTACK2)

    def test_missed_combo_resets_when_debug_flag_disabled(self):
        previous_value = settings.ALLOW_COMBO_NOT_HIT
        settings.ALLOW_COMBO_NOT_HIT = False
        owner = FakeOwner()
        combat = PlayerCombatController()

        try:
            combat.start_attack(owner)
            self.finish_missed_attack(combat, owner)
            combat.start_attack(owner)
        finally:
            settings.ALLOW_COMBO_NOT_HIT = previous_value

        self.assertEqual(owner.state, owner.ATTACK)

    def test_second_combo_hit_resets_when_followup_is_too_late(self):
        owner = FakeOwner()
        combat = PlayerCombatController()

        combat.start_attack(owner)
        self.finish_connected_attack(combat, owner)
        for _ in range(self.remaining_followup_window_after_attack(DEFAULT_PLAYER_ATTACKS["ATTACK"]) + 1):
            combat.advance_timers(owner)
        combat.start_attack(owner)

        self.assertEqual(owner.state, owner.ATTACK)

    def test_third_combo_hit_requires_tighter_followup_delay(self):
        owner = FakeOwner()
        combat = PlayerCombatController()

        combat.start_attack(owner)
        self.finish_connected_attack(combat, owner)
        combat.start_attack(owner)
        self.finish_connected_attack(combat, owner)
        for _ in range(self.remaining_followup_window_after_attack(DEFAULT_PLAYER_ATTACKS["ATTACK2"]) - 1):
            combat.advance_timers(owner)
        combat.start_attack(owner)

        self.assertEqual(owner.state, owner.ATTACK3)
        self.assertTrue(owner.movement.combo_finisher_nudge_started)

    def test_third_combo_hit_resets_when_followup_is_too_late(self):
        owner = FakeOwner()
        combat = PlayerCombatController()

        combat.start_attack(owner)
        self.finish_connected_attack(combat, owner)
        combat.start_attack(owner)
        self.finish_connected_attack(combat, owner)
        for _ in range(self.remaining_followup_window_after_attack(DEFAULT_PLAYER_ATTACKS["ATTACK2"]) + 1):
            combat.advance_timers(owner)
        combat.start_attack(owner)

        self.assertEqual(owner.state, owner.ATTACK)

    def test_combo_chain_restarts_after_third_hit_recovery(self):
        owner = FakeOwner()
        combat = PlayerCombatController()

        combat.start_attack(owner)
        self.finish_connected_attack(combat, owner)
        combat.start_attack(owner)
        self.finish_connected_attack(combat, owner)
        combat.start_attack(owner)
        self.finish_connected_attack(combat, owner)
        combat.start_attack(owner)

        self.assertEqual(owner.state, owner.IDLE)

        for _ in range(24):
            combat.advance_timers(owner)
        combat.start_attack(owner)

        self.assertEqual(owner.state, owner.ATTACK)

    def test_score_combo_caps_at_three_multiplier(self):
        score_manager = ScoreManager()

        for _ in range(6):
            score_manager.register_hit()

        self.assertEqual(score_manager._combo_count, 3)
        self.assertEqual(score_manager.get_multiplier(), 3)


if __name__ == "__main__":
    unittest.main()
