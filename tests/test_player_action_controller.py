import unittest

from game.controllers.player_action_controller import PlayerActionController
from game.controllers.player_combat_controller import PlayerCombatController
from game.data.player_config import DEFAULT_PLAYER_ATTACKS, DEFAULT_WEAPON_PLAYER_ATTACKS
from game.input.input_buffer import InputBuffer
from game.input.player_input_state import PlayerInputState


class FakeMovement:
    def __init__(self):
        self.is_running = True
        self.is_jumping = False
        self.run_attack_momentum_started = False
        self.can_run_attack = True
        self.last_run_attack_distance = 0

    def start_jump(self, owner, player_input):
        pass

    def can_start_run_attack(self):
        return self.can_run_attack

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
        self.input_buffer = InputBuffer(default_frames=6)
        self.air = None
        self.combat_controller = PlayerCombatController()
        self.grab_controller = FakeGrab()
        self.attacks = DEFAULT_PLAYER_ATTACKS
        self.weapon_attacks = DEFAULT_WEAPON_PLAYER_ATTACKS

    def get_attack_data(self, attack_name):
        weapon = getattr(self.weapon_slot, "weapon", None)
        weapon_type = getattr(weapon, "weapon_type", weapon)
        weapon_attack = self.weapon_attacks.get((weapon_type, attack_name))
        if weapon_attack:
            return weapon_attack
        return self.attacks.get(attack_name)


class PlayerActionControllerTests(unittest.TestCase):
    def test_held_run_attack_requires_attack_release_before_next_run_attack(self):
        owner = FakeOwner()
        actions = PlayerActionController()

        actions.update(owner, FakeInput(attack=True))

        self.assertEqual(owner.combat_controller.current_attack_name, owner.RUN_ATTACK)
        self.assertTrue(owner.input_state.run_attack_requires_attack_release)

        owner.combat_controller.cancel_attack()
        owner.input_state.attack_pressed = False
        owner.input_buffer.press("attack")
        actions.update(owner, FakeInput(attack=True))

        self.assertIsNone(owner.combat_controller.current_attack_name)
        self.assertFalse(owner.input_buffer.has("attack"))

        actions.update(owner, FakeInput(attack=False))
        actions.update(owner, FakeInput(attack=True))

        self.assertEqual(owner.combat_controller.current_attack_name, owner.RUN_ATTACK)

    def test_combat_controller_refuses_second_run_attack_until_attack_release(self):
        owner = FakeOwner()

        owner.combat_controller.start_attack(owner)
        self.assertEqual(owner.combat_controller.current_attack_name, owner.RUN_ATTACK)
        self.assertTrue(owner.input_state.run_attack_requires_attack_release)

        owner.combat_controller.cancel_attack()
        owner.combat_controller.start_attack(owner)

        self.assertNotEqual(owner.combat_controller.current_attack_name, owner.RUN_ATTACK)

    def test_attack_input_buffers_during_active_attack_and_starts_after_recovery(self):
        owner = FakeOwner()
        owner.movement.is_running = False
        owner.movement.can_run_attack = False
        actions = PlayerActionController()

        actions.update(owner, FakeInput(attack=True))
        self.assertEqual(owner.combat_controller.current_attack_name, owner.ATTACK_1)

        actions.update(owner, FakeInput(attack=False))
        actions.update(owner, FakeInput(attack=True))
        self.assertTrue(owner.input_buffer.has("attack"))

        owner.combat_controller.attack_manager.mark_connected()
        while owner.combat_controller.current_attack_name == owner.ATTACK_1:
            owner.combat_controller.update_timers(owner)
            actions.update(owner, FakeInput(attack=False))

        self.assertEqual(owner.combat_controller.current_attack_name, owner.ATTACK_2)
        self.assertFalse(owner.input_buffer.has("attack"))


if __name__ == "__main__":
    unittest.main()
