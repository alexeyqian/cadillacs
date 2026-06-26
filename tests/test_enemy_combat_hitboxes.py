import unittest
from dataclasses import replace

from game.combat.attack_data import DEFAULT_ENEMY_ATTACK_DATA
from game.controllers.enemy_combat_controller import EnemyCombatController
from game.components.enemy_combat_state import EnemyCombatState
from game.components.character_geometry import CharacterGeometry
from game.entities.enemy_state import EnemyState


class FakeFrame:
    pass


class FakeEnemy:
    ATTACK = EnemyState.ATTACK

    def __init__(self):
        self.x = 300
        self.y = 500
        self.facing_right = True
        self.state = self.ATTACK
        self.attack_data = replace(
            DEFAULT_ENEMY_ATTACK_DATA,
            damage=10,
            windup=2,
            active=2,
            recovery=2,
            hitbox_offset_x=40,
            hitbox_offset_y=-30,
            hitbox_w=50,
            hitbox_h=20,
        )
        self.combat_controller = EnemyCombatController()
        self.combat_state = EnemyCombatState(self.attack_data)
        self.movement = type('M', (), {'air': None})()
        self.animation_controller = self

    def get_current_frame(self):
        return FakeFrame()


class EnemyCombatHitboxTests(unittest.TestCase):
    def test_attack_rect_is_empty_during_enemy_windup(self):
        enemy = FakeEnemy()
        enemy.combat_state.attack_manager.start(enemy.ATTACK, enemy.attack_data)
        hitboxes = CharacterGeometry()

        self.assertIsNone(hitboxes.get_attack_rect(enemy))

    def test_enemy_attack_rect_comes_from_attack_data_during_active_window(self):
        enemy = FakeEnemy()
        enemy.combat_state.attack_manager.start(enemy.ATTACK, enemy.attack_data)
        hitboxes = CharacterGeometry()

        for _ in range(enemy.attack_data.windup):
            enemy.combat_state.attack_manager.advance()

        attack_rect = hitboxes.get_attack_rect(enemy)

        self.assertEqual((attack_rect.x, attack_rect.y, attack_rect.width, attack_rect.height),
                         (340, 470, 50, 20))

    def test_enemy_attack_rect_mirrors_left_from_anchor(self):
        enemy = FakeEnemy()
        enemy.facing_right = False
        enemy.combat_state.attack_manager.start(enemy.ATTACK, enemy.attack_data)
        hitboxes = CharacterGeometry()

        for _ in range(enemy.attack_data.windup):
            enemy.combat_state.attack_manager.advance()

        attack_rect = hitboxes.get_attack_rect(enemy)

        self.assertEqual((attack_rect.x, attack_rect.y, attack_rect.width, attack_rect.height),
                         (210, 470, 50, 20))


if __name__ == "__main__":
    unittest.main()
