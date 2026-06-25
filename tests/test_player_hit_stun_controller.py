from game.combat.hit_reaction import HitReaction
from game.controllers.player_reaction_controller import PlayerReactionController


class FakeOwner:
    HIT = "HIT"
    IDLE = "IDLE"

    def __init__(self):
        self.state = self.IDLE
        self.state_machine = self

    def change_to(self, owner, state):
        owner.state = state


def test_hit_stun_uses_custom_stun_frames():
    controller = PlayerReactionController(default_stun_frames=8)

    controller._start_hit_stun(HitReaction(stun_frames=14))

    assert controller._hit_stun_remaining == 14
    assert controller.is_in_hit_stun() is True


def test_hit_stun_uses_default_stun_frames():
    controller = PlayerReactionController(default_stun_frames=8)

    controller._start_hit_stun()

    assert controller._hit_stun_remaining == 8


def test_hit_stun_ticks_down():
    controller = PlayerReactionController(default_stun_frames=8)
    controller._hit_stun_remaining = 2

    controller._tick()

    assert controller._hit_stun_remaining == 1
    assert controller.is_in_hit_stun() is True

    controller._tick()

    assert controller._hit_stun_remaining == 0
    assert controller.is_in_hit_stun() is False


def test_update_hit_state_transitions_owner():
    controller = PlayerReactionController(default_stun_frames=8)
    owner = FakeOwner()
    controller._hit_stun_remaining = 2

    controller.update_hit_state(owner)
    assert controller._hit_stun_remaining == 1
    assert owner.state == owner.HIT

    controller.update_hit_state(owner)
    assert controller._hit_stun_remaining == 0
    assert owner.state == owner.IDLE

    controller.update_hit_state(owner)  # no-op when not in stun


def test_reset_clears_hit_stun():
    controller = PlayerReactionController(default_stun_frames=8)
    controller._hit_stun_remaining = 2

    controller.reset()

    assert controller._hit_stun_remaining == 0
