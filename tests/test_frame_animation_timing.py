import pygame
import pytest

from game.animation.frame_animation import (
    FrameAnimation,
    FrameData,
    build_default_frame_configs,
    get_frame_configs,
    load_frame_animation,
)
from game.controllers.frame_animation_controller import FrameAnimationController
from game.tuning import scale_animation_fps_map


def make_frames(count):
    return [
        FrameData(pygame.Surface((1, 1), pygame.SRCALPHA), (0, 0))
        for _ in range(count)
    ]


def test_frame_animation_uses_scalar_frame_duration():
    animation = FrameAnimation(make_frames(2), frame_duration=2)

    animation.update()
    assert animation.get_frame_index() == 0

    animation.update()
    assert animation.get_frame_index() == 1
    assert animation.get_total_duration() == 4


def test_frame_animation_uses_per_frame_durations():
    animation = FrameAnimation(make_frames(3), frame_duration=[1, 3, 2])

    animation.update()
    assert animation.get_frame_index() == 1

    animation.update()
    animation.update()
    assert animation.get_frame_index() == 1

    animation.update()
    assert animation.get_frame_index() == 2
    assert animation.get_total_duration() == 6


def test_frame_animation_controller_accepts_fps_or_frame_duration_list():
    controller = FrameAnimationController({}, {"idle": 12, "attack": [4, 6, 8]})

    assert controller.frame_duration("idle") == 5
    assert controller.frame_duration("attack", frame_count=3) == [4, 6, 8]
    assert controller.animation_total_duration(3, [4, 6, 8]) == 18


def test_frame_animation_controller_rejects_wrong_duration_count():
    controller = FrameAnimationController({}, {"attack": [4, 6]})

    with pytest.raises(ValueError):
        controller.frame_duration("attack", frame_count=3)


def test_build_default_frame_configs_uses_horizontal_256_frames():
    frame_configs = build_default_frame_configs(3, (256, 256), (-128, -256))

    assert frame_configs == [
        {"frame_rect": (0, 0, 256, 256), "offset": (-128, -256)},
        {"frame_rect": (256, 0, 256, 256), "offset": (-128, -256)},
        {"frame_rect": (512, 0, 256, 256), "offset": (-128, -256)},
    ]


def test_load_frame_animation_uses_default_configs_when_frames_missing(monkeypatch):
    class LoadedImage:
        def convert_alpha(self):
            return pygame.Surface((512, 256), pygame.SRCALPHA)

    monkeypatch.setattr(pygame.image, "load", lambda _filename: LoadedImage())

    frames = load_frame_animation(
        {
            "walk": {
                "file": "unused.png",
                "frames_count": 2,
                "default_frame_size": (256, 256),
                "default_offset": (-128, -256),
            }
        },
        "walk",
    )

    assert len(frames) == 2
    assert frames[0].image.get_size() == (256, 256)
    assert frames[0].offset == (-128, -256)
    assert frames[1].image.get_size() == (256, 256)
    assert frames[1].offset == (-128, -256)


def test_frame_width_and_height_override_explicit_frames():
    frame_configs = get_frame_configs(
        {
            "frames_count": 2,
            "frame_width": 80,
            "frame_height": 120,
            "default_frame_size": (256, 256),
            "frames": [
                {"frame_rect": (0, 0, 10, 10), "offset": (99, 99)},
            ],
        }
    )

    assert frame_configs == [
        {"frame_rect": (0, 0, 80, 120), "offset": (-40, -120)},
        {"frame_rect": (80, 0, 80, 120), "offset": (-40, -120)},
    ]


def test_load_frame_animation_offsets_from_frame_bottom_center(monkeypatch):
    class LoadedImage:
        def convert_alpha(self):
            return pygame.Surface((100, 64), pygame.SRCALPHA)

    monkeypatch.setattr(pygame.image, "load", lambda _filename: LoadedImage())

    frames = load_frame_animation(
        {
            "hit": {
                "file": "unused.png",
                "frames_count": 1,
                "frames": [
                    {"frame_rect": (0, 0, 77, 64), "offset": (0, 0)},
                ],
            }
        },
        "hit",
    )

    assert frames[0].offset == (-38.5, -64)


def test_load_frame_animation_copies_animation_scale_to_frames(monkeypatch):
    class LoadedImage:
        def convert_alpha(self):
            return pygame.Surface((64, 32), pygame.SRCALPHA)

    monkeypatch.setattr(pygame.image, "load", lambda _filename: LoadedImage())

    frames = load_frame_animation(
        {
            "walk": {
                "file": "unused.png",
                "frames_count": 1,
                "scale": 1,
                "frames": [
                    {"frame_rect": (0, 0, 64, 32), "offset": (-32, -32)},
                ],
            }
        },
        "walk",
    )

    assert frames[0].scale == 1
    assert frames[0].get_scale(default_scale=2) == 1


def test_animation_tuning_scales_fps_and_duration_lists():
    scaled = scale_animation_fps_map(
        {
            "idle": 10,
            "attack": [4, 6, 8],
        },
        scale=2.0,
    )

    assert scaled["idle"] == 20
    assert scaled["attack"] == [2, 3, 4]
