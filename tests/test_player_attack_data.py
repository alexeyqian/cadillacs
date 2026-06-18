import unittest

from game.entities.attack_data import PLAYER_ATTACKS, WEAPON_PLAYER_ATTACKS
from game.entities.player_combat_controller import PlayerCombatController
from game.ui.score_manager import ScoreManager
from game.settings import (
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
        self.attack_3_nudge_started = False

    def can_start_run_attack(self):
        return self.can_run_attack

    def start_run_attack_momentum(self, owner):
        self.run_attack_momentum_started = True

    def start_attack_3_nudge(self, owner):
        self.attack_3_nudge_started = True


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
    ATTACK_1 = "ATTACK_1"
    ATTACK_2 = "ATTACK_2"
    ATTACK_3 = "ATTACK_3"
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
        self.air = None


class PlayerAttackDataTests(unittest.TestCase):
    def finish_connected_attack(self, combat, owner):
        combat.mark_attack_connected()
        for _ in range(combat.attack_remaining):
            combat.update_timers(owner)

    def test_standing_attack_duration_comes_from_attack_data(self):
        owner = FakeOwner()
        combat = PlayerCombatController()

        combat.start_attack(owner)

        self.assertEqual(owner.state, owner.ATTACK_1)
        self.assertEqual(combat.current_attack_name, owner.ATTACK_1)
        self.assertEqual(combat.attack_timer, 0)
        self.assertEqual(combat.attack_remaining, PLAYER_ATTACKS["ATTACK_1"].duration)

    def test_running_attack_duration_comes_from_attack_data(self):
        owner = FakeOwner()
        owner.movement.is_running = True
        owner.movement.can_run_attack = True
        combat = PlayerCombatController()

        combat.start_attack(owner)

        self.assertEqual(owner.state, owner.RUN_ATTACK)
        self.assertEqual(combat.current_attack_name, owner.RUN_ATTACK)
        self.assertEqual(combat.attack_remaining, PLAYER_ATTACKS["RUN_ATTACK"].duration)
        self.assertTrue(owner.movement.run_attack_momentum_started)

    def test_running_attack_has_arcade_style_timing_and_landing_recovery(self):
        attack = PLAYER_ATTACKS["RUN_ATTACK"]

        self.assertEqual(attack.windup, 4)
        self.assertEqual(attack.active, 10)
        self.assertEqual(attack.recovery, 4)
        self.assertEqual(attack.duration, attack.phase.total_duration)
        self.assertEqual(attack.action_lock, RUN_ATTACK_LANDING_RECOVERY)

    def test_running_attack_has_counter_hurtbox_for_committed_flying_kick(self):
        self.assertTrue(PLAYER_ATTACKS["RUN_ATTACK"].counter_hurtbox)

    def test_running_attack_requires_enough_run_distance(self):
        owner = FakeOwner()
        owner.movement.is_running = True
        owner.movement.can_run_attack = False
        combat = PlayerCombatController()

        combat.start_attack(owner)

        self.assertEqual(owner.state, owner.ATTACK_1)
        self.assertEqual(combat.current_attack_name, owner.ATTACK_1)
        self.assertFalse(owner.movement.run_attack_momentum_started)

    def test_running_attack_knockback_scales_with_run_distance(self):
        owner = FakeOwner()
        owner.movement.can_run_attack = True
        owner.movement.last_run_attack_distance = RUN_ATTACK_FULL_POWER_DISTANCE
        combat = PlayerCombatController()

        combat.start_attack(owner)

        self.assertEqual(
            combat.get_attack_knockback_velocity(owner),
            PLAYER_ATTACKS["RUN_ATTACK"].knockback_velocity
            + RUN_ATTACK_FULL_POWER_KNOCKBACK_BONUS,
        )

    def test_running_attack_has_stronger_knockback_than_normal_punch(self):
        self.assertGreater(
            PLAYER_ATTACKS["RUN_ATTACK"].knockback_velocity,
            PLAYER_ATTACKS["ATTACK_1"].knockback_velocity,
        )

    def test_running_attack_has_longer_enemy_hit_stun_than_normal_punch(self):
        self.assertGreater(
            PLAYER_ATTACKS["RUN_ATTACK"].enemy_hit_stun_duration,
            PLAYER_ATTACKS["ATTACK_1"].enemy_hit_stun_duration,
        )

    def test_running_attack_can_hit_multiple_targets(self):
        self.assertGreater(
            PLAYER_ATTACKS["RUN_ATTACK"].max_targets,
            PLAYER_ATTACKS["ATTACK_1"].max_targets,
        )

    def test_jump_attack_duration_comes_from_attack_data(self):
        owner = FakeOwner()
        owner.movement.is_jumping = True
        combat = PlayerCombatController()

        combat.start_jump_attack(owner)

        self.assertEqual(owner.state, owner.JUMP_ATTACK)
        self.assertEqual(combat.current_attack_name, owner.JUMP_ATTACK)
        self.assertEqual(combat.attack_remaining, PLAYER_ATTACKS["JUMP_ATTACK"].duration)

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
        attack = PLAYER_ATTACKS["JUMP_ATTACK"]

        self.assertEqual(attack.windup, 4)
        self.assertEqual(attack.active, 8)
        self.assertEqual(attack.recovery, 6)
        self.assertTrue(attack.counter_hurtbox)

    def test_attack_timer_counts_up_until_attack_finishes(self):
        owner = FakeOwner()
        combat = PlayerCombatController()

        combat.start_attack(owner)
        combat.update_timers(owner)

        self.assertEqual(combat.attack_timer, 1)
        self.assertEqual(combat.attack_remaining, PLAYER_ATTACKS["ATTACK_1"].duration - 1)

        for _ in range(PLAYER_ATTACKS["ATTACK_1"].duration - 1):
            combat.update_timers(owner)

        self.assertFalse(combat.is_attacking)
        self.assertEqual(combat.attack_timer, 0)
        self.assertEqual(owner.state, owner.IDLE)

    def test_standing_combo_attacks_have_recovery_frames(self):
        self.assertEqual(PLAYER_ATTACKS["ATTACK_1"].recovery, 3)
        self.assertEqual(PLAYER_ATTACKS["ATTACK_2"].recovery, 5)
        self.assertEqual(PLAYER_ATTACKS["ATTACK_3"].recovery, 6)

        for attack_name in ["ATTACK_1", "ATTACK_2", "ATTACK_3"]:
            attack = PLAYER_ATTACKS[attack_name]
            self.assertEqual(attack.duration, attack.phase.total_duration)

    def test_standing_combo_hitboxes_progress_from_jab_to_finisher(self):
        attack_1_hitbox = PLAYER_ATTACKS["ATTACK_1"].hitbox
        attack_2_hitbox = PLAYER_ATTACKS["ATTACK_2"].hitbox
        attack_3_hitbox = PLAYER_ATTACKS["ATTACK_3"].hitbox

        self.assertLess(attack_1_hitbox.width, attack_2_hitbox.width)
        self.assertGreater(attack_3_hitbox.width, attack_2_hitbox.width)
        self.assertGreater(attack_3_hitbox.height, attack_2_hitbox.height)
        self.assertLessEqual(attack_3_hitbox.width, attack_2_hitbox.width + 20)

    def test_player_attack_is_inactive_during_recovery(self):
        owner = FakeOwner()
        combat = PlayerCombatController()
        attack = PLAYER_ATTACKS["ATTACK_1"]

        combat.start_attack(owner)
        for _ in range(attack.windup + attack.active):
            combat.update_timers(owner)

        self.assertTrue(combat.is_attacking)
        self.assertFalse(combat.is_attack_active())
        self.assertEqual(combat.get_attack_phase_name(), "RECOVERY")

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
            combat.attack_controller.current_attack,
            WEAPON_PLAYER_ATTACKS[("knife", owner.ATTACK_1)],
        )
        self.assertEqual(
            combat.get_attack_damage(owner),
            WEAPON_PLAYER_ATTACKS[("knife", owner.ATTACK_1)].damage,
        )
        self.assertEqual(combat.get_attack_lane_reach(owner), 1)

    def test_bat_attack_can_hit_two_targets_from_weapon_attack_data(self):
        owner = FakeOwner()
        owner.weapon_slot.weapon = FakeWeapon("bat")
        combat = PlayerCombatController()

        combat.start_attack(owner)

        self.assertEqual(
            combat.attack_controller.current_attack,
            WEAPON_PLAYER_ATTACKS[("bat", owner.ATTACK_1)],
        )
        self.assertEqual(combat.attack_controller.current_attack.max_targets, 2)

    def test_ranged_weapon_does_not_change_melee_attack_data(self):
        owner = FakeOwner()
        owner.weapon_slot.weapon = FakeWeapon("pistol", is_ranged=True)
        combat = PlayerCombatController()

        combat.start_attack(owner)

        self.assertEqual(combat.attack_controller.current_attack, PLAYER_ATTACKS["ATTACK_1"])

    def test_second_combo_hit_allows_moderate_followup_delay(self):
        owner = FakeOwner()
        combat = PlayerCombatController()

        combat.start_attack(owner)
        self.finish_connected_attack(combat, owner)
        for _ in range(13):
            combat.update_timers(owner)
        combat.start_attack(owner)

        self.assertEqual(owner.state, owner.ATTACK_2)

    def test_second_combo_hit_resets_when_followup_is_too_late(self):
        owner = FakeOwner()
        combat = PlayerCombatController()

        combat.start_attack(owner)
        self.finish_connected_attack(combat, owner)
        for _ in range(14):
            combat.update_timers(owner)
        combat.start_attack(owner)

        self.assertEqual(owner.state, owner.ATTACK_1)

    def test_third_combo_hit_requires_tighter_followup_delay(self):
        owner = FakeOwner()
        combat = PlayerCombatController()

        combat.start_attack(owner)
        self.finish_connected_attack(combat, owner)
        combat.start_attack(owner)
        self.finish_connected_attack(combat, owner)
        for _ in range(6):
            combat.update_timers(owner)
        combat.start_attack(owner)

        self.assertEqual(owner.state, owner.ATTACK_3)
        self.assertTrue(owner.movement.attack_3_nudge_started)

    def test_third_combo_hit_resets_when_followup_is_too_late(self):
        owner = FakeOwner()
        combat = PlayerCombatController()

        combat.start_attack(owner)
        self.finish_connected_attack(combat, owner)
        combat.start_attack(owner)
        self.finish_connected_attack(combat, owner)
        for _ in range(7):
            combat.update_timers(owner)
        combat.start_attack(owner)

        self.assertEqual(owner.state, owner.ATTACK_1)

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
            combat.update_timers(owner)
        combat.start_attack(owner)

        self.assertEqual(owner.state, owner.ATTACK_1)

    def test_score_combo_caps_at_three_multiplier(self):
        score_manager = ScoreManager()

        for _ in range(6):
            score_manager.register_hit()

        self.assertEqual(score_manager.combo_count, 3)
        self.assertEqual(score_manager.get_multiplier(), 3)


if __name__ == "__main__":
    unittest.main()
