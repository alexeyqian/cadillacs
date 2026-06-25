from game.entities.character import Character
from game.entities.player import Player
from game.controllers.player_lifecycle_controller import PlayerLifecycleController


class FakeMovement:
    def __init__(self):
        self.is_jumping = True
        self.cancelled_run_attack_momentum = False
        self.cancelled_combo_finisher_nudge = False

    def cancel_run_attack_momentum(self):
        self.cancelled_run_attack_momentum = True

    def cancel_combo_finisher_nudge(self):
        self.cancelled_combo_finisher_nudge = True


class FakeAir:
    def __init__(self):
        self.reset_called = False

    def reset(self):
        self.reset_called = True


class FakeStateMachine:
    def change_to(self, owner, state):
        owner.state = state


class FakePlayerHitStunController:
    def __init__(self):
        self.reset_called = False

    def reset(self):
        self.reset_called = True


def test_player_inherits_from_character():
    assert issubclass(Player, Character)


def test_player_uses_character_shared_api_methods():
    assert Player.draw is Character.draw
    assert Player.apply_world_bounds is Character.apply_world_bounds
    assert Player.get_frame_rect is Character.get_frame_rect
    assert Player.get_collision_rect is Character.get_collision_rect
    assert Player.get_hurt_rect is Character.get_hurt_rect
    assert Player.get_attack_rect is Character.get_attack_rect


def test_player_reset_for_stage_start_resets_runtime_position_state():
    player = Player.__new__(Player)
    player.IDLE = "IDLE"
    player.state = "JUMP"
    player.facing_right = False
    player.lifecycle_controller = PlayerLifecycleController(0, 0, lives=2)
    player.movement = FakeMovement()
    player.air = FakeAir()
    player.state_machine = FakeStateMachine()
    player.hit_stun_controller = FakePlayerHitStunController()

    player.reset_for_stage_start(120, 340)

    assert player.x == 120
    assert player.y == 340
    assert player.lifecycle_controller.respawn_x == 120
    assert player.lifecycle_controller.respawn_y == 340
    assert player.movement.is_jumping is False
    assert player.movement.cancelled_run_attack_momentum is True
    assert player.movement.cancelled_combo_finisher_nudge is True
    assert player.air.reset_called is True
    assert player.hit_stun_controller.reset_called is True
    assert player.state == player.IDLE
    assert player.facing_right is True


def test_player_lifecycle_tracks_lives_and_respawn_timer():
    lifecycle = PlayerLifecycleController(0, 0, lives=2)

    lifecycle.lose_life()

    assert lifecycle.lives == 1
    assert lifecycle.respawn_remaining == 90

    lifecycle.respawn_remaining = 2
    lifecycle.advance_timers()

    assert lifecycle.respawn_remaining == 1
    assert lifecycle.is_respawn_ready() is False

    lifecycle.advance_timers()

    assert lifecycle.respawn_remaining == 0
    assert lifecycle.is_respawn_ready() is True


def test_player_lifecycle_can_gain_life():
    lifecycle = PlayerLifecycleController(0, 0, lives=2)

    lifecycle.gain_life()

    assert lifecycle.lives == 3
