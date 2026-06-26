from game.entities.character import Character
from game.entities.player import Player
from game.controllers.player_lifecycle_controller import PlayerLifecycleController
from game.components.player_lifecycle_state import PlayerLifecycleState
from game.components.player_reaction_state import PlayerReactionState


class FakeAttackMovement:
    def __init__(self):
        self.cancelled_run_attack_momentum = False
        self.cancelled_combo_finisher_nudge = False

    def cancel_run_attack_momentum(self):
        self.cancelled_run_attack_momentum = True

    def cancel_combo_finisher_nudge(self):
        self.cancelled_combo_finisher_nudge = True


class FakeMovement:
    def __init__(self):
        self.is_jumping = True
        self.attack_movement = FakeAttackMovement()


class FakeAir:
    def __init__(self):
        self.reset_called = False

    def reset(self):
        self.reset_called = True


class FakeStateMachine:
    def change_to(self, owner, state):
        owner.state = state


class FakeReactionController:
    def __init__(self):
        self.reset_called = False

    def reset(self, owner):
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
    player.lifecycle_controller = PlayerLifecycleController()
    player.lifecycle_state = PlayerLifecycleState(0, 0, lives=2)
    player.movement = FakeMovement()
    player.air = FakeAir()
    player.state_machine = FakeStateMachine()
    player.reaction_controller = FakeReactionController()
    player.reaction_state = PlayerReactionState(8)

    player.reset_for_stage_start(120, 340)

    assert player.x == 120
    assert player.y == 340
    assert player.lifecycle_state.respawn_x == 120
    assert player.lifecycle_state.respawn_y == 340
    assert player.movement.is_jumping is False
    assert player.movement.attack_movement.cancelled_run_attack_momentum is True
    assert player.movement.attack_movement.cancelled_combo_finisher_nudge is True
    assert player.air.reset_called is True
    assert player.reaction_controller.reset_called is True
    assert player.state == player.IDLE
    assert player.facing_right is True


def test_player_lifecycle_tracks_lives_and_respawn_timer():
    controller = PlayerLifecycleController()

    class FakeOwner:
        lifecycle_state = PlayerLifecycleState(0, 0, lives=2)

    owner = FakeOwner()
    controller.lose_life(owner)

    assert owner.lifecycle_state.lives == 1
    assert owner.lifecycle_state.respawn_remaining == 90

    owner.lifecycle_state.respawn_remaining = 2
    controller.advance_timers(owner)

    assert owner.lifecycle_state.respawn_remaining == 1
    assert controller.is_respawn_ready(owner) is False

    controller.advance_timers(owner)

    assert owner.lifecycle_state.respawn_remaining == 0
    assert controller.is_respawn_ready(owner) is True


def test_player_lifecycle_can_gain_life():
    controller = PlayerLifecycleController()

    class FakeOwner:
        lifecycle_state = PlayerLifecycleState(0, 0, lives=2)

    owner = FakeOwner()
    controller.gain_life(owner)

    assert owner.lifecycle_state.lives == 3
