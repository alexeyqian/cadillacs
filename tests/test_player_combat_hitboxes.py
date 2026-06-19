import unittest

from game.data.player_config import PLAYER_ATTACKS, WEAPON_PLAYER_ATTACKS
from game.controllers.player_combat_controller import PlayerCombatController
from game.components.character_geometry import CharacterGeometry


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
        self.attacks = PLAYER_ATTACKS
        self.weapon_attacks = WEAPON_PLAYER_ATTACKS
        self.air = None

    def get_attack_data(self, attack_name):
        return self.attacks.get(attack_name)


class PlayerCombatControllerHitboxTests(unittest.TestCase):
    def test_attack_rect_is_empty_during_windup(self):
        owner = FakeOwner()
        hitboxes = CharacterGeometry()

        owner.combat.start_attack(owner)

        self.assertIsNone(hitboxes.get_attack_rect(owner))

    def test_attack_rect_comes_from_attack_data_during_active_window(self):
        owner = FakeOwner()
        hitboxes = CharacterGeometry()
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
        hitboxes = CharacterGeometry()
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
        hitboxes = CharacterGeometry()
        attack_data = PLAYER_ATTACKS["JUMP_ATTACK"]

        owner.combat.attack_manager.start(owner.JUMP_ATTACK, attack_data)
        for _ in range(attack_data.windup):
            owner.combat.update_timers(owner)

        attack_rect = hitboxes.get_attack_rect(owner)

        self.assertEqual(attack_rect.y, owner.y - owner.air.z + attack_data.hitbox_offset_y)


if __name__ == "__main__":
    unittest.main()
