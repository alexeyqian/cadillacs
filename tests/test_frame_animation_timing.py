import pygame
import pytest

from game.animation.frame_animation import FrameAnimation, FrameData
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
