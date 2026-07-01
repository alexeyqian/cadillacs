import unittest

from game.data.player_config import DEFAULT_PLAYER_ATTACKS, DEFAULT_WEAPON_PLAYER_ATTACKS
from game.settings import (
    PLAYER_COLLISION_H,
    PLAYER_COLLISION_W,
    PLAYER_HURTBOX_H,
    PLAYER_HURTBOX_OFFSET_X,
    PLAYER_HURTBOX_OFFSET_Y,
    PLAYER_HURTBOX_W,
    PLAYER_JUMP_BOX_Y_OFFSET,
)
from game.controllers.player_combat_controller import PlayerCombatController
from game.components.player_combat_state import PlayerCombatState
from game.components.character_geometry import CharacterGeometry
from game.input.player_input_tracker import PlayerInputTracker


class FakeRunMovement:
    def can_start_run_attack(self):
        return False


class FakeMovement:
    is_running = False
    is_jumping = False
    last_run_attack_distance = 0
    air = None
    run_movement = FakeRunMovement()


class FakeEnemyMovement:
    pass


class FakeStateMachine:
    def change_to(self, owner, state):
        owner.state = state


class FakeFrame:
    hitbox = None


class FakeAnimationController:
    def __init__(self):
        self.frame = FakeFrame()

    def get_current_frame(self):
        return self.frame


class FakeOwner:
    IDLE = "IDLE"
    ATTACK = "ATTACK"
    ATTACK2 = "ATTACK2"
    ATTACK3 = "ATTACK3"
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
        self.combat_controller = PlayerCombatController()
        self.combat_state = PlayerCombatState()
        self.combat_state.attacks = DEFAULT_PLAYER_ATTACKS
        self.combat_state.weapon_attacks = DEFAULT_WEAPON_PLAYER_ATTACKS
        self.input_tracker = PlayerInputTracker()
        self.movement = FakeMovement()

    def get_attack_data(self, attack_name):
        return self.combat_state.attacks.get(attack_name)


class FakeHurtboxOwner:
    x = 300
    y = 500
    facing_right = True
    movement = FakeMovement()
    hurt_box_w = PLAYER_HURTBOX_W
    hurt_box_h = PLAYER_HURTBOX_H
    hurt_box_offset_x = PLAYER_HURTBOX_OFFSET_X
    hurt_box_offset_y = PLAYER_HURTBOX_OFFSET_Y


class PlayerCombatControllerHitboxTests(unittest.TestCase):
    def test_attack_rect_is_empty_during_windup(self):
        owner = FakeOwner()
        hitboxes = CharacterGeometry()

        owner.combat_controller.start_attack(owner)

        self.assertIsNone(hitboxes.get_attack_rect(owner))

    def test_attack_rect_comes_from_attack_data_during_active_window(self):
        owner = FakeOwner()
        hitboxes = CharacterGeometry()
        attack_data = DEFAULT_PLAYER_ATTACKS["ATTACK"]

        owner.combat_controller.start_attack(owner)
        for _ in range(attack_data.windup):
            owner.combat_controller.update_attack(owner)

        attack_rect = hitboxes.get_attack_rect(owner)

        self.assertEqual(attack_rect.x, owner.x + attack_data.hitbox_offset_x)
        self.assertEqual(attack_rect.y, owner.y + attack_data.hitbox_offset_y)
        self.assertEqual(attack_rect.width, attack_data.hitbox_w)
        self.assertEqual(attack_rect.height, attack_data.hitbox_h)

    def test_attack_rect_uses_animation_hitbox_when_available(self):
        owner = FakeOwner()
        owner.animation_controller.frame.hitbox = (64, -256, 128, 100)
        hitboxes = CharacterGeometry()
        attack_data = DEFAULT_PLAYER_ATTACKS["ATTACK"]

        owner.combat_controller.start_attack(owner)
        for _ in range(attack_data.windup):
            owner.combat_controller.update_attack(owner)

        attack_rect = hitboxes.get_attack_rect(owner)

        self.assertEqual(attack_rect.x, owner.x + 64)
        self.assertEqual(attack_rect.y, owner.y - 256)
        self.assertEqual(attack_rect.width, 128)
        self.assertEqual(attack_rect.height, 100)

    def test_animation_hitbox_mirrors_around_player_anchor_when_facing_left(self):
        owner = FakeOwner()
        owner.facing_right = False
        owner.animation_controller.frame.hitbox = (64, -256, 128, 100)
        hitboxes = CharacterGeometry()
        attack_data = DEFAULT_PLAYER_ATTACKS["ATTACK"]

        owner.combat_controller.start_attack(owner)
        for _ in range(attack_data.windup):
            owner.combat_controller.update_attack(owner)

        attack_rect = hitboxes.get_attack_rect(owner)

        self.assertEqual(attack_rect.x, owner.x - 64 - 128)
        self.assertEqual(attack_rect.y, owner.y - 256)
        self.assertEqual(attack_rect.width, 128)
        self.assertEqual(attack_rect.height, 100)

    def test_attack_rect_mirrors_around_player_anchor_when_facing_left(self):
        owner = FakeOwner()
        owner.facing_right = False
        hitboxes = CharacterGeometry()
        attack_data = DEFAULT_PLAYER_ATTACKS["ATTACK"]

        owner.combat_controller.start_attack(owner)
        for _ in range(attack_data.windup):
            owner.combat_controller.update_attack(owner)

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
        owner.movement.air = FakeAir()
        hitboxes = CharacterGeometry()
        attack_data = DEFAULT_PLAYER_ATTACKS["JUMP_ATTACK"]

        owner.combat_state.attack_manager.start(owner.JUMP_ATTACK, attack_data)
        for _ in range(attack_data.windup):
            owner.combat_controller.update_attack(owner)

        attack_rect = hitboxes.get_attack_rect(owner)

        self.assertEqual(attack_rect.y, owner.y - owner.movement.air.z + attack_data.hitbox_offset_y)

    def test_player_hurt_rect_comes_from_owner_config(self):
        owner = FakeHurtboxOwner()
        hitboxes = CharacterGeometry()

        hurt_rect = hitboxes.get_hurt_rect(owner)

        self.assertEqual(hurt_rect.x, owner.x + PLAYER_HURTBOX_OFFSET_X)
        self.assertEqual(hurt_rect.y, owner.y + PLAYER_HURTBOX_OFFSET_Y)
        self.assertEqual(hurt_rect.width, PLAYER_HURTBOX_W)
        self.assertEqual(hurt_rect.height, PLAYER_HURTBOX_H)

    def test_player_collision_rect_moves_up_while_jumping(self):
        owner = FakeOwner()
        owner.movement.is_jumping = True
        hitboxes = CharacterGeometry()

        collision_rect = hitboxes.get_collision_rect(owner)

        self.assertEqual(collision_rect.x, owner.x - PLAYER_COLLISION_W // 2)
        self.assertEqual(
            collision_rect.y,
            owner.y - PLAYER_JUMP_BOX_Y_OFFSET - PLAYER_COLLISION_H,
        )
        self.assertEqual(collision_rect.width, PLAYER_COLLISION_W)
        self.assertEqual(collision_rect.height, PLAYER_COLLISION_H)

    def test_player_hurt_rect_moves_up_while_jumping(self):
        owner = FakeOwner()
        owner.movement.is_jumping = True
        hitboxes = CharacterGeometry()

        hurt_rect = hitboxes.get_hurt_rect(owner)

        self.assertEqual(hurt_rect.x, owner.x + PLAYER_HURTBOX_OFFSET_X)
        self.assertEqual(
            hurt_rect.y,
            owner.y - PLAYER_JUMP_BOX_Y_OFFSET + PLAYER_HURTBOX_OFFSET_Y,
        )
        self.assertEqual(hurt_rect.width, PLAYER_HURTBOX_W)
        self.assertEqual(hurt_rect.height, PLAYER_HURTBOX_H)

    def test_collision_rect_does_not_require_enemy_movement_to_have_is_jumping(self):
        owner = FakeOwner()
        owner.movement = FakeEnemyMovement()
        hitboxes = CharacterGeometry()

        collision_rect = hitboxes.get_collision_rect(owner)

        self.assertEqual(collision_rect.x, owner.x - PLAYER_COLLISION_W // 2)
        self.assertEqual(collision_rect.y, owner.y - PLAYER_COLLISION_H)


if __name__ == "__main__":
    unittest.main()
