import unittest

from game.entities.attack_data import PLAYER_ATTACKS
from game.entities.enemy_config import ENEMY_CONFIGS


class AttackDataValidationTests(unittest.TestCase):
    def test_player_attack_phase_fits_duration(self):
        for attack_name, attack in PLAYER_ATTACKS.items():
            with self.subTest(attack_name=attack_name):
                self.assertGreater(attack.duration, 0)
                self.assertGreater(attack.active, 0)
                self.assertLessEqual(attack.phase.total_duration, attack.duration)

    def test_player_damaging_attacks_have_positive_hitboxes(self):
        for attack_name, attack in PLAYER_ATTACKS.items():
            with self.subTest(attack_name=attack_name):
                self.assertTrue(attack.hitboxes)
                for hitbox in attack.hitboxes:
                    self.assertGreater(hitbox.width, 0)
                    self.assertGreater(hitbox.height, 0)

    def test_melee_enemy_attacks_have_positive_hitboxes(self):
        for enemy_id, config in ENEMY_CONFIGS.items():
            if config.archetype == "ranged":
                continue

            with self.subTest(enemy_id=enemy_id):
                self.assertTrue(config.attack.hitboxes)
                for hitbox in config.attack.hitboxes:
                    self.assertGreater(hitbox.width, 0)
                    self.assertGreater(hitbox.height, 0)

    def test_enemy_attack_phase_fits_duration(self):
        for enemy_id, config in ENEMY_CONFIGS.items():
            with self.subTest(enemy_id=enemy_id):
                self.assertGreater(config.attack.duration, 0)
                self.assertGreater(config.attack.active, 0)
                self.assertEqual(config.attack.phase.total_duration, config.attack.duration)


if __name__ == "__main__":
    unittest.main()
