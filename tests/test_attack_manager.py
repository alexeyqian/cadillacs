import unittest
from dataclasses import replace

from game.entities.attack_manager import AttackManager
from game.entities.attack_data import DEFAULT_ENEMY_ATTACK_DATA, DEFAULT_PLAYER_ATTACK_DATA


class AttackManagerTests(unittest.TestCase):
    def test_player_attack_uses_elapsed_timer_and_duration(self):
        attack = replace(
            DEFAULT_PLAYER_ATTACK_DATA,
            damage=10,
            windup=0,
            active=1,
            recovery=2,
        )
        controller = AttackManager()

        controller.start("ATTACK_1", attack)

        self.assertTrue(controller.is_attacking)
        self.assertEqual(controller.elapsed_frames, 0)
        self.assertEqual(controller.remaining_frames, 3)

        self.assertFalse(controller.advance())
        self.assertEqual(controller.elapsed_frames, 1)
        self.assertEqual(controller.remaining_frames, 2)

        controller.advance()
        self.assertTrue(controller.advance())

    def test_enemy_attack_phase_controls_active_window(self):
        attack = replace(
            DEFAULT_ENEMY_ATTACK_DATA,
            damage=10,
            windup=2,
            active=2,
            recovery=2,
        )
        controller = AttackManager()

        controller.start("enemy_punch", attack)

        self.assertFalse(controller.is_active())
        controller.advance()
        self.assertFalse(controller.is_active())
        controller.advance()
        self.assertTrue(controller.is_active())
        controller.advance()
        self.assertTrue(controller.is_active())
        controller.advance()
        self.assertFalse(controller.is_active())

    def test_phase_name_tracks_attack_timing(self):
        attack = replace(
            DEFAULT_ENEMY_ATTACK_DATA,
            damage=10,
            windup=2,
            active=2,
            recovery=2,
        )
        controller = AttackManager()

        controller.start("enemy_punch", attack)

        self.assertEqual(controller.get_phase_name(), "WINDUP")
        controller.advance()
        self.assertEqual(controller.get_phase_name(), "WINDUP")
        controller.advance()
        self.assertEqual(controller.get_phase_name(), "ACTIVE")
        controller.advance()
        self.assertEqual(controller.get_phase_name(), "ACTIVE")
        controller.advance()
        self.assertEqual(controller.get_phase_name(), "RECOVERY")
        self.assertEqual(
            controller.get_timing_label(),
            "enemy_punch RECOVERY 4/6"
        )

    def test_hit_targets_are_tracked_per_attack(self):
        attack = replace(
            DEFAULT_PLAYER_ATTACK_DATA,
            damage=10,
            windup=0,
            active=1,
            recovery=2,
        )
        target = object()
        controller = AttackManager()

        controller.start("ATTACK_1", attack)
        controller.mark_target_hit(target)

        self.assertTrue(controller.has_connected)
        self.assertTrue(controller.has_hit_target(target))

        controller.start("ATTACK_2", attack)

        self.assertFalse(controller.has_connected)
        self.assertFalse(controller.has_hit_target(target))

    def test_target_limit_blocks_extra_targets(self):
        attack = replace(
            DEFAULT_PLAYER_ATTACK_DATA,
            damage=10,
            windup=0,
            active=1,
            recovery=2,
            max_targets=2,
        )
        first_target = object()
        second_target = object()
        third_target = object()
        controller = AttackManager()

        controller.start("wide_swing", attack)

        self.assertTrue(controller.can_hit_target(first_target))
        controller.mark_target_hit(first_target)
        self.assertFalse(controller.can_hit_target(first_target))
        self.assertTrue(controller.can_hit_target(second_target))
        controller.mark_target_hit(second_target)
        self.assertFalse(controller.can_hit_more_targets())
        self.assertFalse(controller.can_hit_target(third_target))


if __name__ == "__main__":
    unittest.main()
