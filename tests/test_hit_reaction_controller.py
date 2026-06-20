from game.combat.hit_reaction import HitReaction
from game.controllers.hit_reaction_controller import HitReactionController


def test_hit_reaction_controller_uses_custom_stun_frames():
    controller = HitReactionController(default_stun_frames=8)

    controller.start_hit_stun(HitReaction(stun_frames=14))

    assert controller.hit_stun_remaining == 14
    assert controller.is_in_hit_stun() is True


def test_hit_reaction_controller_uses_default_stun_frames():
    controller = HitReactionController(default_stun_frames=8)

    controller.start_hit_stun()

    assert controller.hit_stun_remaining == 8


def test_hit_reaction_controller_advance_timers_updates_hit_stun():
    controller = HitReactionController(default_stun_frames=8)
    controller.hit_stun_remaining = 2

    controller.advance_timers()

    assert controller.hit_stun_remaining == 1
    assert controller.is_in_hit_stun() is True

    controller.advance_timers()

    assert controller.hit_stun_remaining == 0
    assert controller.is_in_hit_stun() is False


def test_hit_reaction_controller_can_reset():
    controller = HitReactionController(default_stun_frames=8)
    controller.hit_stun_remaining = 2

    controller.reset()

    assert controller.hit_stun_remaining == 0
