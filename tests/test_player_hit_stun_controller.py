from game.combat.hit_reaction import HitReaction
from game.controllers.player_reaction_controller import PlayerReactionController
from game.components.player_reaction_state import PlayerReactionState


class FakeOwner:
    HIT = "HIT"
    IDLE = "IDLE"

    def __init__(self, default_stun_frames=8):
        self.state = self.IDLE
        self.state_machine = self
        self.reaction_state = PlayerReactionState(default_stun_frames)

    def change_to(self, owner, state):
        owner.state = state


def test_hit_stun_uses_custom_stun_frames():
    owner = FakeOwner(default_stun_frames=8)
    controller = PlayerReactionController()

    controller._start_hit_stun(owner, HitReaction(stun_frames=14))

    assert owner.reaction_state._hit_stun_remaining == 14
    assert controller.is_in_hit_stun(owner) is True


def test_hit_stun_uses_default_stun_frames():
    owner = FakeOwner(default_stun_frames=8)
    controller = PlayerReactionController()

    controller._start_hit_stun(owner)

    assert owner.reaction_state._hit_stun_remaining == 8


def test_hit_stun_ticks_down():
    owner = FakeOwner(default_stun_frames=8)
    controller = PlayerReactionController()
    owner.reaction_state._hit_stun_remaining = 2

    controller._tick(owner)

    assert owner.reaction_state._hit_stun_remaining == 1
    assert controller.is_in_hit_stun(owner) is True

    controller._tick(owner)

    assert owner.reaction_state._hit_stun_remaining == 0
    assert controller.is_in_hit_stun(owner) is False


def test_update_hit_state_transitions_owner():
    owner = FakeOwner(default_stun_frames=8)
    controller = PlayerReactionController()
    owner.reaction_state._hit_stun_remaining = 2

    controller.update_hit_state(owner)
    assert owner.reaction_state._hit_stun_remaining == 1
    assert owner.state == owner.HIT

    controller.update_hit_state(owner)
    assert owner.reaction_state._hit_stun_remaining == 0
    assert owner.state == owner.IDLE

    controller.update_hit_state(owner)  # no-op when not in stun


def test_reset_clears_hit_stun():
    owner = FakeOwner(default_stun_frames=8)
    controller = PlayerReactionController()
    owner.reaction_state._hit_stun_remaining = 2

    controller.reset(owner)

    assert owner.reaction_state._hit_stun_remaining == 0
