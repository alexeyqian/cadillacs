import unittest

from game.entities.attack_data import PLAYER_ATTACKS, WEAPON_PLAYER_ATTACKS
from game.entities.player_combat import PlayerCombat


class FakeMovement:
    def __init__(self):
        self.is_running = False
        self.is_jumping = False


class FakeStateMachine:
    def change_to(self, owner, state):
        owner.state = state


class FakeWeapon:
    def __init__(self, weapon_type, is_ranged=False):
        self.weapon_type = weapon_type
        self.is_ranged = is_ranged


class FakeWeaponSlot:
    def __init__(self):
        self.weapon = None


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
        self.weapon_slot = FakeWeaponSlot()


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

    def test_knife_attack_uses_weapon_attack_data(self):
        owner = FakeOwner()
        owner.weapon_slot.weapon = FakeWeapon("knife")
        combat = PlayerCombat()

        combat.start_attack(owner)

        self.assertEqual(
            combat.attack_controller.current_attack,
            WEAPON_PLAYER_ATTACKS[("knife", owner.ATTACK_1)],
        )
        self.assertEqual(
            combat.get_attack_damage(owner),
            WEAPON_PLAYER_ATTACKS[("knife", owner.ATTACK_1)].damage,
        )
        self.assertEqual(combat.get_attack_lane_reach(owner), 1)

    def test_bat_attack_can_hit_two_targets_from_weapon_attack_data(self):
        owner = FakeOwner()
        owner.weapon_slot.weapon = FakeWeapon("bat")
        combat = PlayerCombat()

        combat.start_attack(owner)

        self.assertEqual(
            combat.attack_controller.current_attack,
            WEAPON_PLAYER_ATTACKS[("bat", owner.ATTACK_1)],
        )
        self.assertEqual(combat.attack_controller.current_attack.max_targets, 2)

    def test_ranged_weapon_does_not_change_melee_attack_data(self):
        owner = FakeOwner()
        owner.weapon_slot.weapon = FakeWeapon("pistol", is_ranged=True)
        combat = PlayerCombat()

        combat.start_attack(owner)

        self.assertEqual(combat.attack_controller.current_attack, PLAYER_ATTACKS["ATTACK_1"])


if __name__ == "__main__":
    unittest.main()
