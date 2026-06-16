import unittest

from game.settings import RUN_ATTACK_MOMENTUM_FRAMES, RUN_ATTACK_MOMENTUM_SPEED_SCALE
from game.entities.player_movement import PlayerMovement


class FakeCombat:
    def __init__(self):
        self.is_attacking = False
        self.current_attack_name = None


class FakeOwner:
    RUN_ATTACK = "RUN_ATTACK"

    def __init__(self):
        self.x = 300
        self.y = 500
        self.speed = 5
        self.run_speed = 9
        self.facing_right = True
        self.combat = FakeCombat()


class FakeInput:
    def __init__(self, left=False, right=False, up=False, down=False, run=False):
        self.left = left
        self.right = right
        self.up = up
        self.down = down
        self.run = run


class PlayerMovementTests(unittest.TestCase):
    def test_run_attack_keeps_sliding_forward_for_a_short_time(self):
        owner = FakeOwner()
        movement = PlayerMovement(owner.speed)
        movement.run_direction = 1
        owner.combat.is_attacking = True
        owner.combat.current_attack_name = owner.RUN_ATTACK

        movement.start_run_attack_momentum(owner)
        starting_momentum = movement.run_attack_momentum_remaining
        moved = movement.update_movement(owner, FakeInput())

        self.assertEqual(starting_momentum, RUN_ATTACK_MOMENTUM_FRAMES)
        self.assertEqual(
            movement.run_attack_momentum_speed,
            max(owner.speed, owner.run_speed * RUN_ATTACK_MOMENTUM_SPEED_SCALE),
        )
        self.assertTrue(moved)
        self.assertGreater(owner.x, 300)
        self.assertEqual(
            movement.run_attack_momentum_remaining,
            starting_momentum - 1,
        )

    def test_non_run_attack_clears_run_attack_momentum(self):
        owner = FakeOwner()
        movement = PlayerMovement(owner.speed)
        owner.combat.is_attacking = True
        owner.combat.current_attack_name = "ATTACK_1"

        movement.start_run_attack_momentum(owner)
        moved = movement.update_movement(owner, FakeInput())

        self.assertFalse(moved)
        self.assertEqual(owner.x, 300)
        self.assertEqual(movement.run_attack_momentum_remaining, 0)

    def test_player_can_run_diagonally(self):
        owner = FakeOwner()
        movement = PlayerMovement(owner.speed)

        moved = movement.update_movement(
            owner,
            FakeInput(right=True, up=True, run=True),
        )

        self.assertTrue(moved)
        self.assertTrue(movement.is_running)
        self.assertEqual(owner.x, 300 + owner.run_speed)
        self.assertEqual(owner.y, 500 - owner.run_speed)

    def test_run_attack_requires_configured_run_distance(self):
        owner = FakeOwner()
        movement = PlayerMovement(owner.speed)
        movement.run_attack_required_distance = owner.run_speed * 2

        movement.update_movement(owner, FakeInput(right=True, run=True))

        self.assertFalse(movement.can_start_run_attack())

        movement.update_movement(owner, FakeInput(right=True, run=True))

        self.assertTrue(movement.can_start_run_attack())

    def test_run_attack_distance_resets_when_player_stops_running(self):
        owner = FakeOwner()
        movement = PlayerMovement(owner.speed)
        movement.run_attack_required_distance = owner.run_speed

        movement.update_movement(owner, FakeInput(right=True, run=True))
        self.assertTrue(movement.can_start_run_attack())

        movement.update_movement(owner, FakeInput())

        self.assertFalse(movement.can_start_run_attack())
        self.assertEqual(movement.run_distance, 0)

    def test_run_attack_records_run_distance_before_consuming_it(self):
        owner = FakeOwner()
        movement = PlayerMovement(owner.speed)
        movement.run_distance = 180

        movement.start_run_attack_momentum(owner)

        self.assertEqual(movement.last_run_attack_distance, 180)
        self.assertEqual(movement.run_distance, 0)


if __name__ == "__main__":
    unittest.main()
