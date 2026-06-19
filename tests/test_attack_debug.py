import unittest
from dataclasses import replace

from game.combat.attack_manager import AttackManager
from game.combat.attack_data import DEFAULT_PLAYER_ATTACK_DATA
from game.entities.attack_debug import format_attack_debug_lines


class AttackDebugTests(unittest.TestCase):
    def test_inactive_attack_has_no_debug_lines(self):
        controller = AttackManager()

        self.assertEqual(format_attack_debug_lines("Player", controller), [])

    def test_attack_debug_lines_include_timing_damage_targets_and_boxes(self):
        attack = replace(
            DEFAULT_PLAYER_ATTACK_DATA,
            damage=10,
            windup=4,
            active=4,
            recovery=4,
            hitbox_offset_x=10,
            hitbox_offset_y=-20,
            hitbox_w=30,
            hitbox_h=40,
            max_targets=2,
        )
        controller = AttackManager()
        controller.start("test_punch", attack)
        for _ in range(4):
            controller.advance()
        controller.mark_target_hit(object())

        lines = format_attack_debug_lines(
            "Player",
            controller,
            damage=13,
            lane_reach=1,
        )

        self.assertEqual(lines[0], "Player: test_punch ACTIVE 4/12")
        self.assertEqual(lines[1], "hits 1/2 | damage 13 | lane 1")
        self.assertEqual(lines[2], "hitbox x:10 y:-20 w:30 h:40")


if __name__ == "__main__":
    unittest.main()
