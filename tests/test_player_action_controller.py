import unittest

from game.entities.player_action_controller import PlayerActionController
from game.entities.player_combat_controller import PlayerCombatController
from game.entities.player_input_state import PlayerInputState


class FakeMovement:
    def __init__(self):
        self.is_running = True
        self.is_jumping = False
        self.jump_pressed = False
        self.run_attack_momentum_started = False

    def start_jump(self, player_input):
        pass

    def start_run_attack_momentum(self, owner):
        self.run_attack_momentum_started = True


class FakeStateMachine:
    def change_to(self, owner, state):
        owner.state = state


class FakeWeaponSlot:
    def __init__(self):
        self.weapon = None
        self.fire_pressed = False

    def fire(self, owner):
        pass


class FakeGrab:
    grabbed_enemy = None


class FakeInput:
    def __init__(self, attack=False):
        self.attack = attack
        self.jump = False
        self.fire = False


class FakeOwner:
    IDLE = "IDLE"
    ATTACK_1 = "ATTACK_1"
    ATTACK_2 = "ATTACK_2"
    ATTACK_3 = "ATTACK_3"
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
        self.input_state = PlayerInputState()
        self.combat = PlayerCombatController()
        self.grab = FakeGrab()


class PlayerActionControllerTests(unittest.TestCase):
    def test_held_run_attack_requires_attack_release_before_next_run_attack(self):
        owner = FakeOwner()
        actions = PlayerActionController()

        actions.update(owner, FakeInput(attack=True))

        self.assertEqual(owner.combat.current_attack_name, owner.RUN_ATTACK)
        self.assertTrue(owner.input_state.run_attack_requires_attack_release)

        owner.combat.cancel_attack()
        owner.input_state.attack_pressed = False
        actions.update(owner, FakeInput(attack=True))

        self.assertIsNone(owner.combat.current_attack_name)

        actions.update(owner, FakeInput(attack=False))
        actions.update(owner, FakeInput(attack=True))

        self.assertEqual(owner.combat.current_attack_name, owner.RUN_ATTACK)


if __name__ == "__main__":
    unittest.main()
