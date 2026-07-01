import pygame

from game.input.player_input import PlayerInput
from game.input.player_input_state import PlayerInputState


class FakeKeys:
    def __init__(self, pressed=None):
        self.pressed = set(pressed or [])

    def __getitem__(self, key):
        return key in self.pressed


def make_input(*pressed):
    return PlayerInput(FakeKeys(pressed))


def test_player_input_maps_arrow_keys():
    player_input = make_input(
        pygame.K_LEFT,
        pygame.K_RIGHT,
        pygame.K_UP,
        pygame.K_DOWN,
    )

    assert player_input.left is True
    assert player_input.right is True
    assert player_input.up is True
    assert player_input.down is True


def test_player_input_maps_wasd_aliases():
    player_input = make_input(
        pygame.K_a,
        pygame.K_d,
        pygame.K_w,
        pygame.K_s,
    )

    assert player_input.left is True
    assert player_input.right is True
    assert player_input.up is True
    assert player_input.down is True


def test_player_input_maps_action_keys():
    player_input = make_input(
        pygame.K_SPACE,
        pygame.K_j,
        pygame.K_q,
    )

    assert player_input.jump is True
    assert player_input.attack is True
    assert player_input.drop is True


def test_player_input_maps_secondary_action_aliases():
    player_input = make_input(pygame.K_k)

    assert player_input.jump is True


def test_player_input_state_defaults_edge_flags_to_false():
    input_state = PlayerInputState()

    assert input_state.attack_pressed is False
    assert input_state.jump_pressed is False
    assert input_state.jump_attack_pressed is False
    assert input_state.run_attack_requires_attack_release is False
