import unittest

from PIL import Image

from game.animation.frame_animation import get_frame_configs
from game.animation.mustapha_data import MUSTAPHA_ANIMATIONS


class PlayerAnimationDataTests(unittest.TestCase):
    def test_mustapha_combo_punches_have_separate_animation_keys(self):
        for animation_key in ["attack", "attack2", "attack3"]:
            with self.subTest(animation_key=animation_key):
                self.assertIn(animation_key, MUSTAPHA_ANIMATIONS)

    def test_mustapha_combo_punches_use_distinct_three_phase_sheets(self):
        expected_files = {
            "attack": "assets/player/mustapha_attack_3x.png",
            "attack2": "assets/player/mustapha_attack2_3x.png",
            "attack3": "assets/player/mustapha_attack3_3x.png",
        }
        for animation_key in ["attack", "attack2", "attack3"]:
            with self.subTest(animation_key=animation_key):
                self.assertEqual(MUSTAPHA_ANIMATIONS[animation_key]["file"], expected_files[animation_key])
                self.assertEqual(MUSTAPHA_ANIMATIONS[animation_key]["frames_count"], 3)
                self.assertEqual(len(MUSTAPHA_ANIMATIONS[animation_key]["frame_durations"]), 3)

    def test_mustapha_attack_can_define_animation_hitbox(self):
        self.assertEqual(MUSTAPHA_ANIMATIONS["attack"]["hitbox"], (64, -256, 128, 100))
        self.assertEqual(MUSTAPHA_ANIMATIONS["attack2"]["hitbox"], (64, -192, 128, 100))
        self.assertEqual(MUSTAPHA_ANIMATIONS["attack3"]["hitbox"], (64, -192, 128, 100))

    def test_mustapha_combo_punch_frame_rects_fit_their_sheets(self):
        for animation_key in ["attack", "attack2", "attack3"]:
            config = MUSTAPHA_ANIMATIONS[animation_key]
            image = Image.open(config["file"])
            sheet_width, sheet_height = image.size

            for frame in get_frame_configs(config):
                with self.subTest(animation_key=animation_key, frame_rect=frame["frame_rect"]):
                    x, y, width, height = frame["frame_rect"]
                    self.assertLessEqual(x + width, sheet_width)
                    self.assertLessEqual(y + height, sheet_height)

    def test_mustapha_walk_3x_uses_unscaled_256_frames(self):
        config = MUSTAPHA_ANIMATIONS["walk"]

        self.assertEqual(config["file"], "assets/player/mustapha_walk_3x.png")
        self.assertEqual(config["frame_width"], 256)
        self.assertEqual(config["frame_height"], 256)
        self.assertEqual(config["scale"], 1)

        for frame in get_frame_configs(config):
            with self.subTest(frame_rect=frame["frame_rect"]):
                self.assertEqual(frame["frame_rect"][2:], (256, 256))

    def test_mustapha_animations_without_frames_use_256_defaults(self):
        for animation_key, config in MUSTAPHA_ANIMATIONS.items():
            if "frames" in config or "frame_width" in config or "frame_height" in config:
                continue

            with self.subTest(animation_key=animation_key):
                self.assertEqual(config["default_frame_size"], (256, 256))
                self.assertEqual(config["default_offset"], (-128, -256))

    def test_mustapha_animations_without_explicit_scale_render_at_source_size(self):
        for animation_key in ["hit", "dead", "jump", "jump_attack", "grab", "throw", "grab_knee"]:
            with self.subTest(animation_key=animation_key):
                self.assertEqual(MUSTAPHA_ANIMATIONS[animation_key]["scale"], 1)

    def test_mustapha_animations_without_frames_fit_their_sheets(self):
        for animation_key, config in MUSTAPHA_ANIMATIONS.items():
            if "frames" in config:
                continue

            image = Image.open(config["file"])
            sheet_width, sheet_height = image.size
            frame_width, frame_height = config["default_frame_size"]

            with self.subTest(animation_key=animation_key):
                self.assertLessEqual(config["frames_count"] * frame_width, sheet_width)
                self.assertLessEqual(frame_height, sheet_height)


if __name__ == "__main__":
    unittest.main()
