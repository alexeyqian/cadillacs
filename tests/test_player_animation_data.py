import unittest

from PIL import Image

from game.animation.mustapha_data import MUSTAPHA_ANIMATIONS, MUSTAPHA_ANIM_FPS


class PlayerAnimationDataTests(unittest.TestCase):
    def test_mustapha_combo_punches_have_separate_animation_keys(self):
        for animation_key in ["attack_1", "attack_2", "attack_3"]:
            with self.subTest(animation_key=animation_key):
                self.assertIn(animation_key, MUSTAPHA_ANIMATIONS)
                self.assertIn(animation_key, MUSTAPHA_ANIM_FPS)

    def test_mustapha_combo_punches_use_distinct_three_phase_sheets(self):
        expected_files = {
            "attack_1": "assets/player/mustapha_attack_1.png",
            "attack_2": "assets/player/mustapha_attack_2.png",
            "attack_3": "assets/player/mustapha_attack_3.png",
        }
        for animation_key in ["attack_1", "attack_2", "attack_3"]:
            with self.subTest(animation_key=animation_key):
                self.assertEqual(MUSTAPHA_ANIMATIONS[animation_key]["file"], expected_files[animation_key])
                self.assertEqual(MUSTAPHA_ANIMATIONS[animation_key]["frames_count"], 3)
                self.assertEqual(MUSTAPHA_ANIM_FPS[animation_key], 12)

    def test_mustapha_combo_punch_frame_rects_fit_their_sheets(self):
        for animation_key in ["attack_1", "attack_2", "attack_3"]:
            config = MUSTAPHA_ANIMATIONS[animation_key]
            image = Image.open(config["file"])
            sheet_width, sheet_height = image.size

            for frame in config["frames"]:
                with self.subTest(animation_key=animation_key, frame_rect=frame["frame_rect"]):
                    x, y, width, height = frame["frame_rect"]
                    self.assertLessEqual(x + width, sheet_width)
                    self.assertLessEqual(y + height, sheet_height)


if __name__ == "__main__":
    unittest.main()
