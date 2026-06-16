import unittest

from game.entities.attack_data import AttackHitboxData
from game.entities.combat_geometry import combat_box_to_world_rect


class CombatGeometryTests(unittest.TestCase):
    def test_combat_box_faces_right_from_anchor(self):
        box = AttackHitboxData(x=40, y=-20, width=30, height=10)

        rect = combat_box_to_world_rect(100, 200, True, box)

        self.assertEqual((rect.x, rect.y, rect.width, rect.height), (140, 180, 30, 10))

    def test_combat_box_faces_left_from_anchor(self):
        box = AttackHitboxData(x=40, y=-20, width=30, height=10)

        rect = combat_box_to_world_rect(100, 200, False, box)

        self.assertEqual((rect.x, rect.y, rect.width, rect.height), (30, 180, 30, 10))


if __name__ == "__main__":
    unittest.main()
