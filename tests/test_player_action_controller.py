import unittest

from game.controllers.player_action_controller import PlayerActionController
from game.controllers.player_combat_controller import PlayerCombatController
from game.components.player_intent import PlayerIntent
from game.data.player_config import DEFAULT_PLAYER_ATTACKS, DEFAULT_WEAPON_PLAYER_ATTACKS
from game.entities.player import Player
from game.input.input_buffer import InputBuffer
from game.input.player_input_state import PlayerInputState


class FakeRunMovement:
    def __init__(self, can_run_attack):
        self._can_run_attack = can_run_attack

    def can_start_run_attack(self):
        return self._can_run_attack


class FakeJumpMovement:
    def start_jump(self, owner, player_input):
        pass


class FakeMovement:
    def __init__(self):
        self.is_running = True
        self.is_jumping = False
        self.run_attack_momentum_started = False
        self.can_run_attack = True
        self.last_run_attack_distance = 0
        self.run_movement = FakeRunMovement(can_run_attack=True)
        self.jump_movement = FakeJumpMovement()

    def start_run_attack_momentum(self, owner):
        self.run_attack_momentum_started = True


class FakeStateMachine:
    def change_to(self, owner, state):
        owner.state = state


class FakeWeaponSlot:
    def __init__(self):
        self.weapon = None

    def fire(self, owner):
        pass


class FakeGrab:
    grabbed_enemy = None


class FakeInput:
    def __init__(self, attack=False):
        self.attack = attack
        self.jump = False
        self.drop = False


class FakeOwner:
    IDLE = "IDLE"
    ATTACK = "ATTACK"
    ATTACK2 = "ATTACK2"
    ATTACK3 = "ATTACK3"
    RUN_ATTACK = "RUN_ATTACK"
    JUMP_ATTACK = "JUMP_ATTACK"
    GRAB_KNEE = "GRAB_KNEE"
    RECOIL = "RECOIL"
    DEAD = "DEAD"

    def __init__(self):
        self.state = self.IDLE
        self.movement = FakeMovement()
        self.state_machine = FakeStateMachine()
        self.weapon_slot = FakeWeaponSlot()
        self.intent = PlayerIntent()
        self.input_state = PlayerInputState()
        self.input_buffer = InputBuffer()
        from game.components.player_combat_state import PlayerCombatState
        from game.components.player_grab_state import PlayerGrabState
        self.combat_controller = PlayerCombatController()
        self.combat_state = PlayerCombatState()
        self.combat_state.attacks = DEFAULT_PLAYER_ATTACKS
        self.combat_state.weapon_attacks = DEFAULT_WEAPON_PLAYER_ATTACKS
        self.grab_state = PlayerGrabState()
        self.grab_state.grabbed_enemy = None

    def get_attack_data(self, attack_name):
        weapon = getattr(self.weapon_slot, "weapon", None)
        weapon_type = getattr(weapon, "weapon_type", weapon)
        weapon_attack = self.combat_state.weapon_attacks.get((weapon_type, attack_name))
        if weapon_attack:
            return weapon_attack
        return self.combat_state.attacks.get(attack_name)


class PlayerActionControllerTests(unittest.TestCase):
    def test_held_run_attack_requires_attack_release_before_next_run_attack(self):
        owner = FakeOwner()
        actions = PlayerActionController()

        actions.request_actions(owner, FakeInput(attack=True))
        Player._try_start_attack(owner)

        self.assertEqual(owner.combat_state.current_attack_name, owner.RUN_ATTACK)
        self.assertTrue(owner.input_state.run_attack_requires_attack_release)

        owner.combat_controller.cancel_attack(owner)
        owner.input_state.attack_pressed = False
        owner.input_buffer.press_attack(12)
        actions.request_actions(owner, FakeInput(attack=True))
        Player._try_start_attack(owner)

        self.assertIsNone(owner.combat_state.current_attack_name)
        self.assertFalse(owner.input_buffer.has_attack())

        actions.request_actions(owner, FakeInput(attack=False))
        actions.request_actions(owner, FakeInput(attack=True))
        Player._try_start_attack(owner)

        self.assertEqual(owner.combat_state.current_attack_name, owner.RUN_ATTACK)

    def test_combat_controller_refuses_second_run_attack_until_attack_release(self):
        owner = FakeOwner()

        owner.combat_controller.start_attack(owner)
        self.assertEqual(owner.combat_state.current_attack_name, owner.RUN_ATTACK)
        self.assertTrue(owner.input_state.run_attack_requires_attack_release)

        owner.combat_controller.cancel_attack(owner)
        owner.combat_controller.start_attack(owner)

        self.assertNotEqual(owner.combat_state.current_attack_name, owner.RUN_ATTACK)

    def test_attack_input_buffers_during_active_attack_and_starts_after_recovery(self):
        owner = FakeOwner()
        owner.movement.is_running = False
        owner.movement.run_movement._can_run_attack = False
        actions = PlayerActionController()

        actions.request_actions(owner, FakeInput(attack=True))
        Player._try_start_attack(owner)
        self.assertEqual(owner.combat_state.current_attack_name, owner.ATTACK)

        actions.request_actions(owner, FakeInput(attack=False))
        actions.request_actions(owner, FakeInput(attack=True))
        Player._try_start_attack(owner)
        self.assertTrue(owner.input_buffer.has_attack())

        owner.combat_state.attack_manager.has_connected = True
        while owner.combat_state.current_attack_name == owner.ATTACK:
            owner.combat_controller.advance_timers(owner)
            owner.combat_controller.update_attack(owner)
            actions.request_actions(owner, FakeInput(attack=False))
            Player._try_start_attack(owner)

        self.assertEqual(owner.combat_state.current_attack_name, owner.ATTACK2)
        self.assertFalse(owner.input_buffer.has_attack())


if __name__ == "__main__":
    unittest.main()
