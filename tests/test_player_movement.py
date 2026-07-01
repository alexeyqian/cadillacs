import unittest

from game.settings import RUN_ATTACK_MOMENTUM_FRAMES, RUN_ATTACK_MOMENTUM_SPEED_SCALE
from game.components.player_air_state import PlayerAirState
from game.components.player_movement import PlayerMovement


class FakeCombatState:
    def __init__(self):
        self.is_attacking = False
        self.current_attack_name = None


class FakeCombatController:
    def cancel_attack(self, owner):
        owner.combat_state.is_attacking = False
        owner.combat_state.current_attack_name = None


class FakeOwner:
    IDLE = "IDLE"
    JUMP = "JUMP"
    JUMP_ATTACK = "JUMP_ATTACK"
    RUN_ATTACK = "RUN_ATTACK"
    ATTACK3 = "ATTACK3"

    def __init__(self):
        self.x = 300
        self.y = 500
        self.state = self.IDLE
        self.speed = 5
        self.run_speed = 9
        self.facing_right = True
        self.combat_state = FakeCombatState()
        self.combat_controller = FakeCombatController()
        self.grab_state = FakeGrab()
        self.input_state = FakeInputState()
        self.state_machine = FakeStateMachine()


class FakeGrab:
    grabbed_enemy = None


class FakeInputState:
    jump_attack_pressed = False


class FakeStateMachine:
    def change_to(self, owner, state):
        owner.state = state


class FakeInput:
    def __init__(self, left=False, right=False, up=False, down=False):
        self.left = left
        self.right = right
        self.up = up
        self.down = down


class PlayerMovementTests(unittest.TestCase):
    def update_until_state(self, movement, owner, state, max_frames=30):
        for _ in range(max_frames):
            movement.jump_movement.update_jump_physics(owner, FakeInput())
            if owner.state == state:
                return

    def test_run_attack_keeps_sliding_forward_for_a_short_time(self):
        owner = FakeOwner()
        movement = PlayerMovement()
        movement.run_movement.run_direction = 1
        owner.combat_state.is_attacking = True
        owner.combat_state.current_attack_name = owner.RUN_ATTACK

        movement.start_run_attack_momentum(owner)
        starting_momentum = movement.attack_movement._run_attack_momentum_remaining
        movement.update_movement(owner, FakeInput())

        self.assertEqual(starting_momentum, RUN_ATTACK_MOMENTUM_FRAMES)
        self.assertEqual(
            movement.attack_movement._run_attack_momentum_speed,
            max(owner.speed, owner.run_speed * RUN_ATTACK_MOMENTUM_SPEED_SCALE),
        )
        self.assertTrue(movement.moving)
        self.assertGreater(owner.x, 300)
        self.assertEqual(
            movement.attack_movement._run_attack_momentum_remaining,
            starting_momentum - 1,
        )

    def test_non_run_attack_clears_run_attack_momentum(self):
        owner = FakeOwner()
        movement = PlayerMovement()
        owner.combat_state.is_attacking = True
        owner.combat_state.current_attack_name = "ATTACK"

        movement.start_run_attack_momentum(owner)
        movement.update_movement(owner, FakeInput())

        self.assertFalse(movement.moving)
        self.assertEqual(owner.x, 300)
        self.assertEqual(movement.attack_movement._run_attack_momentum_remaining, 0)

    def test_player_can_run_diagonally(self):
        owner = FakeOwner()
        movement = PlayerMovement()
        movement.run_movement._double_tap_run_active = True

        movement.update_movement(owner, FakeInput(right=True, up=True))

        self.assertTrue(movement.moving)
        self.assertTrue(movement.is_running)
        self.assertEqual(owner.x, 300 + owner.run_speed)
        self.assertEqual(owner.y, 500 - owner.run_speed)

    def test_run_attack_requires_configured_run_distance(self):
        owner = FakeOwner()
        movement = PlayerMovement()
        movement.run_movement._double_tap_run_active = True
        movement.run_movement.run_attack_min_distance = owner.run_speed * 2

        movement.update_movement(owner, FakeInput(right=True))

        self.assertFalse(movement.run_movement.can_start_run_attack())

        movement.update_movement(owner, FakeInput(right=True))

        self.assertTrue(movement.run_movement.can_start_run_attack())

    def test_run_attack_distance_resets_when_player_stops_running(self):
        owner = FakeOwner()
        movement = PlayerMovement()
        movement.run_movement._double_tap_run_active = True
        movement.run_movement.run_attack_min_distance = owner.run_speed

        movement.update_movement(owner, FakeInput(right=True))
        self.assertTrue(movement.run_movement.can_start_run_attack())

        movement.update_movement(owner, FakeInput())

        self.assertFalse(movement.run_movement.can_start_run_attack())
        self.assertEqual(movement.run_movement.run_distance, 0)

    def test_run_attack_cooldown_blocks_only_run_attack_eligibility(self):
        owner = FakeOwner()
        movement = PlayerMovement()
        movement.run_movement._double_tap_run_active = True
        movement.run_movement.run_attack_min_distance = owner.run_speed

        movement.update_movement(owner, FakeInput(right=True))
        self.assertTrue(movement.run_movement.can_start_run_attack())

        movement.run_movement.start_run_attack_cooldown(frames=2)
        self.assertFalse(movement.run_movement.can_start_run_attack())

        movement.run_movement.advance_timers()
        self.assertFalse(movement.run_movement.can_start_run_attack())

        movement.run_movement.advance_timers()
        self.assertTrue(movement.run_movement.can_start_run_attack())

    def test_run_attack_records_run_distance_before_consuming_it(self):
        owner = FakeOwner()
        movement = PlayerMovement()
        movement.run_movement.run_distance = 180

        movement.start_run_attack_momentum(owner)

        self.assertEqual(movement.last_run_attack_distance, 180)
        self.assertEqual(movement.run_movement.run_distance, 0)

    def test_jump_starts_immediately_and_preserves_ground_y(self):
        owner = FakeOwner()
        movement = PlayerMovement(jump_power=12,
            gravity=0.7,
            air_move_speed=3,)

        movement.jump_movement.start_jump(owner, FakeInput(right=True))

        self.assertEqual(owner.state, owner.JUMP)
        self.assertTrue(movement.is_jumping)
        self.assertEqual(owner.y, 500)
        self.assertGreater(movement.air.z, 0)
        self.assertEqual(movement.air.direction_x, 1)

    def test_jump_uses_z_height_without_changing_ground_y(self):
        owner = FakeOwner()
        movement = PlayerMovement(jump_power=4,
            gravity=1,
            air_move_speed=3,)

        movement.jump_movement.start_jump(owner, FakeInput())
        movement.jump_movement.update_jump_physics(owner, FakeInput())
        self.assertEqual(owner.state, owner.JUMP)

        movement.jump_movement.update_jump_physics(owner, FakeInput())

        self.assertEqual(owner.y, 500)
        self.assertGreater(movement.air.z, 0)
        self.assertFalse(movement.air.is_grounded)

    def test_jump_lands_back_on_same_ground_anchor(self):
        owner = FakeOwner()
        movement = PlayerMovement(jump_power=3,
            gravity=2,
            air_move_speed=3,)

        movement.jump_movement.start_jump(owner, FakeInput())
        for _ in range(20):
            movement.jump_movement.update_jump_physics(owner, FakeInput())

        self.assertEqual(owner.y, 500)
        self.assertEqual(movement.air.z, 0)
        self.assertTrue(movement.air.is_grounded)
        self.assertFalse(movement.is_jumping)
        self.assertEqual(owner.state, owner.IDLE)

    def test_air_movement_uses_current_horizontal_input(self):
        owner = FakeOwner()
        movement = PlayerMovement(jump_power=4,
            gravity=1,
            air_move_speed=3,)

        movement.jump_movement.start_jump(owner, FakeInput(right=True, up=True))
        movement.jump_movement.update_jump_physics(owner, FakeInput())
        movement.jump_movement.update_jump_physics(owner, FakeInput())

        self.assertEqual(owner.x, 300)
        self.assertAlmostEqual(owner.y, 500 - 3.6)

        movement.jump_movement.update_jump_physics(owner, FakeInput(left=True))

        self.assertEqual(owner.x, 297)
        self.assertFalse(owner.facing_right)

        movement.jump_movement.update_jump_physics(owner, FakeInput(right=True))

        self.assertEqual(owner.x, 300)
        self.assertTrue(owner.facing_right)

    def test_landing_cancels_unfinished_jump_attack(self):
        owner = FakeOwner()
        movement = PlayerMovement(jump_power=3, gravity=2, air_move_speed=3)

        movement.jump_movement.start_jump(owner, FakeInput())
        owner.state = owner.JUMP_ATTACK
        owner.combat_state.is_attacking = True
        owner.combat_state.current_attack_name = owner.JUMP_ATTACK
        for _ in range(20):
            movement.jump_movement.update_jump_physics(owner, FakeInput())

        self.assertEqual(owner.state, owner.IDLE)
        self.assertIsNone(owner.combat_state.current_attack_name)

    def test_combo_finisher_nudge_moves_forward_briefly(self):
        owner = FakeOwner()
        movement = PlayerMovement()
        owner.combat_state.is_attacking = True
        owner.combat_state.current_attack_name = owner.ATTACK3

        movement.attack_movement.start_combo_finisher_nudge(owner)
        starting_nudge = movement.attack_movement._combo_finisher_nudge_remaining
        movement.update_movement(owner, FakeInput())

        self.assertTrue(movement.moving)
        self.assertGreater(owner.x, 300)
        self.assertEqual(
            movement.attack_movement._combo_finisher_nudge_remaining,
            starting_nudge - 1,
        )

    def test_combo_finisher_nudge_can_be_canceled(self):
        owner = FakeOwner()
        movement = PlayerMovement()

        movement.attack_movement.start_combo_finisher_nudge(owner)
        movement.attack_movement.cancel_combo_finisher_nudge()

        self.assertEqual(movement.attack_movement._combo_finisher_nudge_remaining, 0)
        self.assertEqual(movement.attack_movement._combo_finisher_nudge_direction, 0)
        self.assertEqual(movement.attack_movement._combo_finisher_nudge_speed, 0)


if __name__ == "__main__":
    unittest.main()
