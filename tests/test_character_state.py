from game.components.character_state import CharacterState
from game.entities.enemy_state import EnemyState
from game.entities.player import Player
from game.entities.player_state import PlayerState
from game.entities.player_state_machine import PlayerStateMachine


def test_player_and_enemy_share_common_character_states():
    shared_state_names = [
        "IDLE",
        "WALK",
        "ATTACK",
        "HIT",
        "RECOIL",
        "DEAD",
        "GRABBED",
        "KNOCKDOWN",
        "GETUP",
    ]

    for state_name in shared_state_names:
        assert getattr(Player, state_name) == getattr(CharacterState, state_name)
        assert getattr(EnemyState, state_name) == getattr(CharacterState, state_name)


def test_player_exposes_shared_recovery_states():
    assert Player.GRABBED == "GRABBED"
    assert Player.KNOCKDOWN == "KNOCKDOWN"
    assert Player.GETUP == "GETUP"


def test_player_state_machine_registers_shared_recovery_states():
    owner = Player.__new__(Player)
    owner.state = Player.IDLE

    state_machine = PlayerStateMachine(owner)

    assert Player.GRABBED in state_machine.states
    assert Player.KNOCKDOWN in state_machine.states
    assert Player.GETUP in state_machine.states


def test_player_specific_states_are_grouped_under_player_state():
    assert Player.ATTACK_1 == PlayerState.ATTACK_1
    assert Player.RUN_ATTACK == PlayerState.RUN_ATTACK
    assert Player.JUMP_ATTACK == PlayerState.JUMP_ATTACK
    assert Player.GRAB_KNEE == PlayerState.GRAB_KNEE
    assert Player.THROW == PlayerState.THROW
