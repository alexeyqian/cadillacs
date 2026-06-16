import unittest

from game.animation.mustapha_data import MUSTAPHA_ANIMATIONS, MUSTAPHA_ANIM_FPS


class PlayerAnimationDataTests(unittest.TestCase):
    def test_mustapha_combo_punches_have_separate_animation_keys(self):
        for animation_key in ["attack_1", "attack_2", "attack_3"]:
            with self.subTest(animation_key=animation_key):
                self.assertIn(animation_key, MUSTAPHA_ANIMATIONS)
                self.assertIn(animation_key, MUSTAPHA_ANIM_FPS)

    def test_mustapha_combo_punches_alias_current_three_phase_punch(self):
        base_attack = MUSTAPHA_ANIMATIONS["attack"]

        for animation_key in ["attack_1", "attack_2", "attack_3"]:
            with self.subTest(animation_key=animation_key):
                self.assertIs(MUSTAPHA_ANIMATIONS[animation_key], base_attack)
                self.assertEqual(MUSTAPHA_ANIMATIONS[animation_key]["frames_count"], 3)
                self.assertEqual(MUSTAPHA_ANIM_FPS[animation_key], 12)


if __name__ == "__main__":
    unittest.main()
