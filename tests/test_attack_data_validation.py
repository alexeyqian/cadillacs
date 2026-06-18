import unittest

from game.entities.attack_data import EnemyAttackData
from game.entities.enemy_config import ENEMY_CONFIGS
from game.entities.player_config import PLAYER_ATTACKS, WEAPON_PLAYER_ATTACKS


class AttackDataValidationTests(unittest.TestCase):
    def test_enemy_configs_use_enemy_attack_data(self):
        for enemy_id, config in ENEMY_CONFIGS.items():
            with self.subTest(enemy_id=enemy_id):
                self.assertIsInstance(config.attack, EnemyAttackData)

    def test_player_attack_phase_fits_duration(self):
        for attack_name, attack in PLAYER_ATTACKS.items():
            with self.subTest(attack_name=attack_name):
                self.assertGreater(attack.duration, 0)
                self.assertGreater(attack.active, 0)
                self.assertGreater(attack.max_targets, 0)
                self.assertLessEqual(attack.total_duration, attack.duration)

    def test_player_damaging_attacks_have_positive_hitboxes(self):
        for attack_name, attack in PLAYER_ATTACKS.items():
            with self.subTest(attack_name=attack_name):
                self.assertGreater(attack.hitbox_w, 0)
                self.assertGreater(attack.hitbox_h, 0)

    def test_weapon_player_attack_phase_fits_duration(self):
        for attack_key, attack in WEAPON_PLAYER_ATTACKS.items():
            with self.subTest(attack_key=attack_key):
                self.assertGreater(attack.duration, 0)
                self.assertGreater(attack.active, 0)
                self.assertGreater(attack.max_targets, 0)
                self.assertLessEqual(attack.total_duration, attack.duration)

    def test_weapon_player_attacks_have_positive_hitboxes(self):
        for attack_key, attack in WEAPON_PLAYER_ATTACKS.items():
            with self.subTest(attack_key=attack_key):
                self.assertGreater(attack.hitbox_w, 0)
                self.assertGreater(attack.hitbox_h, 0)

    def test_melee_enemy_attacks_have_positive_hitboxes(self):
        for enemy_id, config in ENEMY_CONFIGS.items():
            if config.archetype == "ranged":
                continue

            with self.subTest(enemy_id=enemy_id):
                self.assertGreater(config.attack.hitbox_w, 0)
                self.assertGreater(config.attack.hitbox_h, 0)

    def test_enemy_attack_phase_fits_duration(self):
        for enemy_id, config in ENEMY_CONFIGS.items():
            with self.subTest(enemy_id=enemy_id):
                self.assertGreater(config.attack.duration, 0)
                self.assertGreater(config.attack.active, 0)
                self.assertGreater(config.attack.max_targets, 0)
                self.assertEqual(config.attack.total_duration, config.attack.duration)


if __name__ == "__main__":
    unittest.main()
