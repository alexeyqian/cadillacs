import unittest

from game.entities.attack_data import PLAYER_ATTACKS
from game.entities.player_combat import PlayerCombat
from game.entities.player_hitboxes import PlayerHitboxes


class FakeMovement:
    is_running = False
    is_jumping = False


class FakeStateMachine:
    def change_to(self, owner, state):
        owner.state = state


class FakeFrame:
    attack_rect = (999, 999, 999, 999)
    counter_hurt_rect = (999, 999, 999, 999)


class FakeAnimationController:
    def get_current_frame(self):
        return FakeFrame()


class FakeOwner:
    IDLE = "IDLE"
    ATTACK_1 = "ATTACK_1"
    ATTACK_2 = "ATTACK_2"
    ATTACK_3 = "ATTACK_3"
    RUN_ATTACK = "RUN_ATTACK"
    DEAD = "DEAD"

    def __init__(self):
        self.x = 300
        self.y = 500
        self.facing_right = True
        self.state = self.IDLE
        self.movement = FakeMovement()
        self.state_machine = FakeStateMachine()
        self.animation_controller = FakeAnimationController()
        self.combat = PlayerCombat()


class PlayerCombatHitboxTests(unittest.TestCase):
    def test_animation_attack_rect_is_ignored_during_windup(self):
        owner = FakeOwner()
        hitboxes = PlayerHitboxes()

        owner.combat.start_attack(owner)

        self.assertIsNone(hitboxes.get_attack_rect(owner))

    def test_attack_rect_comes_from_attack_data_during_active_window(self):
        owner = FakeOwner()
        hitboxes = PlayerHitboxes()
        attack_data = PLAYER_ATTACKS["ATTACK_1"]

        owner.combat.start_attack(owner)
        for _ in range(attack_data.windup):
            owner.combat.update_timers(owner)

        attack_rect = hitboxes.get_attack_rect(owner)

        self.assertEqual(attack_rect.x, owner.x + attack_data.hitboxes[0].x)
        self.assertEqual(attack_rect.y, owner.y + attack_data.hitboxes[0].y)
        self.assertEqual(attack_rect.width, attack_data.hitboxes[0].width)
        self.assertEqual(attack_rect.height, attack_data.hitboxes[0].height)

    def test_attack_rect_mirrors_around_player_anchor_when_facing_left(self):
        owner = FakeOwner()
        owner.facing_right = False
        hitboxes = PlayerHitboxes()
        attack_data = PLAYER_ATTACKS["ATTACK_1"]

        owner.combat.start_attack(owner)
        for _ in range(attack_data.windup):
            owner.combat.update_timers(owner)

        attack_rect = hitboxes.get_attack_rect(owner)

        self.assertEqual(
            attack_rect.x,
            owner.x - attack_data.hitboxes[0].x - attack_data.hitboxes[0].width
        )

    def test_counter_hurtbox_uses_attack_data_active_window(self):
        owner = FakeOwner()
        hitboxes = PlayerHitboxes()
        attack_data = PLAYER_ATTACKS["ATTACK_1"]

        owner.combat.start_attack(owner)
        self.assertIsNone(hitboxes.get_counter_hurt_rect(owner))

        for _ in range(attack_data.windup):
            owner.combat.update_timers(owner)

        counter_rect = hitboxes.get_counter_hurt_rect(owner)

        self.assertEqual(counter_rect.x, owner.x + attack_data.counter_hurtboxes[0].x)
        self.assertEqual(counter_rect.y, owner.y + attack_data.counter_hurtboxes[0].y)


if __name__ == "__main__":
    unittest.main()
