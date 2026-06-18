import unittest

from game.entities.player_config import PLAYER_ATTACKS
from game.entities.player_combat_controller import PlayerCombatController
from game.entities.player_geometry import PlayerGeometry


class FakeMovement:
    is_running = False
    is_jumping = False

    def can_start_run_attack(self):
        return False


class FakeStateMachine:
    def change_to(self, owner, state):
        owner.state = state


class FakeFrame:
    pass


class FakeAnimationController:
    def get_current_frame(self):
        return FakeFrame()


class FakeOwner:
    IDLE = "IDLE"
    ATTACK_1 = "ATTACK_1"
    ATTACK_2 = "ATTACK_2"
    ATTACK_3 = "ATTACK_3"
    RUN_ATTACK = "RUN_ATTACK"
    JUMP_ATTACK = "JUMP_ATTACK"
    DEAD = "DEAD"

    def __init__(self):
        self.x = 300
        self.y = 500
        self.facing_right = True
        self.state = self.IDLE
        self.movement = FakeMovement()
        self.state_machine = FakeStateMachine()
        self.animation_controller = FakeAnimationController()
        self.combat = PlayerCombatController()
        self.air = None


class PlayerCombatControllerHitboxTests(unittest.TestCase):
    def test_attack_rect_is_empty_during_windup(self):
        owner = FakeOwner()
        hitboxes = PlayerGeometry()

        owner.combat.start_attack(owner)

        self.assertIsNone(hitboxes.get_attack_rect(owner))

    def test_attack_rect_comes_from_attack_data_during_active_window(self):
        owner = FakeOwner()
        hitboxes = PlayerGeometry()
        attack_data = PLAYER_ATTACKS["ATTACK_1"]

        owner.combat.start_attack(owner)
        for _ in range(attack_data.windup):
            owner.combat.update_timers(owner)

        attack_rect = hitboxes.get_attack_rect(owner)

        self.assertEqual(attack_rect.x, owner.x + attack_data.hitbox_offset_x)
        self.assertEqual(attack_rect.y, owner.y + attack_data.hitbox_offset_y)
        self.assertEqual(attack_rect.width, attack_data.hitbox_w)
        self.assertEqual(attack_rect.height, attack_data.hitbox_h)

    def test_attack_rect_mirrors_around_player_anchor_when_facing_left(self):
        owner = FakeOwner()
        owner.facing_right = False
        hitboxes = PlayerGeometry()
        attack_data = PLAYER_ATTACKS["ATTACK_1"]

        owner.combat.start_attack(owner)
        for _ in range(attack_data.windup):
            owner.combat.update_timers(owner)

        attack_rect = hitboxes.get_attack_rect(owner)

        self.assertEqual(
            attack_rect.x,
            owner.x - attack_data.hitbox_offset_x - attack_data.hitbox_w
        )

    def test_jump_attack_rect_uses_visual_air_height(self):
        class FakeAir:
            z = 40

            def get_visual_y(self, ground_y):
                return ground_y - self.z

        owner = FakeOwner()
        owner.air = FakeAir()
        hitboxes = PlayerGeometry()
        attack_data = PLAYER_ATTACKS["JUMP_ATTACK"]

        owner.combat.attack_controller.start(owner.JUMP_ATTACK, attack_data)
        for _ in range(attack_data.windup):
            owner.combat.update_timers(owner)

        attack_rect = hitboxes.get_attack_rect(owner)

        self.assertEqual(attack_rect.y, owner.y - owner.air.z + attack_data.hitbox_offset_y)


if __name__ == "__main__":
    unittest.main()
