import unittest

from game.entities.attack_data import PLAYER_ATTACKS
from game.entities.player_combat import PlayerCombat


class FakeMovement:
    def __init__(self):
        self.is_running = False
        self.is_jumping = False


class FakeStateMachine:
    def change_to(self, owner, state):
        owner.state = state


class FakeOwner:
    IDLE = "IDLE"
    ATTACK_1 = "ATTACK_1"
    ATTACK_2 = "ATTACK_2"
    ATTACK_3 = "ATTACK_3"
    RUN_ATTACK = "RUN_ATTACK"
    JUMP_ATTACK = "JUMP_ATTACK"
    DEAD = "DEAD"

    def __init__(self):
        self.state = self.IDLE
        self.movement = FakeMovement()
        self.state_machine = FakeStateMachine()


class PlayerAttackDataTests(unittest.TestCase):
    def test_standing_attack_duration_comes_from_attack_data(self):
        owner = FakeOwner()
        combat = PlayerCombat()

        combat.start_attack(owner)

        self.assertEqual(owner.state, owner.ATTACK_1)
        self.assertEqual(combat.current_attack_name, owner.ATTACK_1)
        self.assertEqual(combat.attack_timer, 0)
        self.assertEqual(combat.attack_remaining, PLAYER_ATTACKS["ATTACK_1"].duration)

    def test_running_attack_duration_comes_from_attack_data(self):
        owner = FakeOwner()
        owner.movement.is_running = True
        combat = PlayerCombat()

        combat.start_attack(owner)

        self.assertEqual(owner.state, owner.RUN_ATTACK)
        self.assertEqual(combat.current_attack_name, owner.RUN_ATTACK)
        self.assertEqual(combat.attack_remaining, PLAYER_ATTACKS["RUN_ATTACK"].duration)

    def test_jump_attack_duration_comes_from_attack_data(self):
        owner = FakeOwner()
        owner.movement.is_jumping = True
        combat = PlayerCombat()

        combat.start_jump_attack(owner)

        self.assertEqual(owner.state, owner.JUMP_ATTACK)
        self.assertEqual(combat.current_attack_name, owner.JUMP_ATTACK)
        self.assertEqual(combat.attack_remaining, PLAYER_ATTACKS["JUMP_ATTACK"].duration)

    def test_attack_timer_counts_up_until_attack_finishes(self):
        owner = FakeOwner()
        combat = PlayerCombat()

        combat.start_attack(owner)
        combat.update_timers(owner)

        self.assertEqual(combat.attack_timer, 1)
        self.assertEqual(combat.attack_remaining, PLAYER_ATTACKS["ATTACK_1"].duration - 1)

        for _ in range(PLAYER_ATTACKS["ATTACK_1"].duration - 1):
            combat.update_timers(owner)

        self.assertFalse(combat.is_attacking)
        self.assertEqual(combat.attack_timer, 0)
        self.assertEqual(owner.state, owner.IDLE)

    def test_player_combat_uses_per_target_hit_tracking(self):
        first_target = object()
        second_target = object()
        owner = FakeOwner()
        combat = PlayerCombat()

        combat.start_attack(owner)

        self.assertTrue(combat.can_hit_target(first_target))
        combat.mark_attack_hit(first_target)

        self.assertFalse(combat.can_hit_target(first_target))
        self.assertFalse(combat.can_hit_target(second_target))


if __name__ == "__main__":
    unittest.main()
