import unittest

from game.entities.attack_controller import AttackController
from game.entities.attack_data import AttackPhaseData, EnemyAttackData, PlayerAttackData


class AttackControllerTests(unittest.TestCase):
    def test_player_attack_uses_elapsed_timer_and_duration(self):
        attack = PlayerAttackData(
            damage=10,
            duration=3,
            phase=AttackPhaseData(windup=0, active=1, recovery=2),
        )
        controller = AttackController()

        controller.start_attack("ATTACK_1", attack)

        self.assertTrue(controller.is_attacking)
        self.assertEqual(controller.attack_timer, 0)
        self.assertEqual(controller.attack_remaining, 3)

        self.assertFalse(controller.update_attack_timer())
        self.assertEqual(controller.attack_timer, 1)
        self.assertEqual(controller.attack_remaining, 2)

        controller.update_attack_timer()
        self.assertTrue(controller.update_attack_timer())

    def test_enemy_attack_phase_controls_active_window(self):
        attack = EnemyAttackData(
            damage=10,
            phase=AttackPhaseData(windup=2, active=2, recovery=2),
        )
        controller = AttackController()

        controller.start_attack("enemy_punch", attack)

        self.assertFalse(controller.is_active())
        controller.update_attack_timer()
        self.assertFalse(controller.is_active())
        controller.update_attack_timer()
        self.assertTrue(controller.is_active())
        controller.update_attack_timer()
        self.assertTrue(controller.is_active())
        controller.update_attack_timer()
        self.assertFalse(controller.is_active())

    def test_phase_name_tracks_attack_timing(self):
        attack = EnemyAttackData(
            damage=10,
            phase=AttackPhaseData(windup=2, active=2, recovery=2),
        )
        controller = AttackController()

        controller.start_attack("enemy_punch", attack)

        self.assertEqual(controller.get_phase_name(), "WINDUP")
        controller.update_attack_timer()
        self.assertEqual(controller.get_phase_name(), "WINDUP")
        controller.update_attack_timer()
        self.assertEqual(controller.get_phase_name(), "ACTIVE")
        controller.update_attack_timer()
        self.assertEqual(controller.get_phase_name(), "ACTIVE")
        controller.update_attack_timer()
        self.assertEqual(controller.get_phase_name(), "RECOVERY")
        self.assertEqual(
            controller.get_timing_label(),
            "enemy_punch RECOVERY 4/6"
        )

    def test_hit_targets_are_tracked_per_attack(self):
        attack = PlayerAttackData(
            damage=10,
            duration=3,
            phase=AttackPhaseData(windup=0, active=1, recovery=2),
        )
        target = object()
        controller = AttackController()

        controller.start_attack("ATTACK_1", attack)
        controller.mark_target_hit(target)

        self.assertTrue(controller.attack_connected)
        self.assertTrue(controller.has_hit_target(target))

        controller.start_attack("ATTACK_2", attack)

        self.assertFalse(controller.attack_connected)
        self.assertFalse(controller.has_hit_target(target))

    def test_target_limit_blocks_extra_targets(self):
        attack = PlayerAttackData(
            damage=10,
            duration=3,
            phase=AttackPhaseData(windup=0, active=1, recovery=2),
            max_targets=2,
        )
        first_target = object()
        second_target = object()
        third_target = object()
        controller = AttackController()

        controller.start_attack("wide_swing", attack)

        self.assertTrue(controller.can_hit_target(first_target))
        controller.mark_target_hit(first_target)
        self.assertFalse(controller.can_hit_target(first_target))
        self.assertTrue(controller.can_hit_target(second_target))
        controller.mark_target_hit(second_target)
        self.assertFalse(controller.can_hit_more_targets())
        self.assertFalse(controller.can_hit_target(third_target))


if __name__ == "__main__":
    unittest.main()
