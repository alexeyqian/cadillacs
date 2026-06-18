import unittest

from game.entities.attack_controller import AttackController
from game.entities.attack_data import EnemyAttackData
from game.entities.enemy_combat_controller import EnemyCombatController
from game.entities.enemy_geometry import EnemyGeometry
from game.entities.enemy_state import EnemyState


class FakeFrame:
    attack_rect = (999, 999, 999, 999)


class FakeEnemy:
    ATTACK = EnemyState.ATTACK

    def __init__(self):
        self.x = 300
        self.y = 500
        self.facing_right = True
        self.state = self.ATTACK
        self.attack_timer = 0
        self.attack_damage = 10
        self.attack_delay = 0
        self.attack_cooldown_duration = 30
        self.attack_windup = 2
        self.attack_active = 2
        self.attack_recovery = 2
        self.attack_clash_recovery_duration = 12
        self.attack_clash_cooldown_duration = 20
        self.attack_controller = AttackController()
        self.attack_data = EnemyAttackData(
            damage=10,
            windup=2,
            active=2,
            recovery=2,
            hitbox_offset_x=40,
            hitbox_offset_y=-30,
            hitbox_w=50,
            hitbox_h=20,
        )
        self.combat = EnemyCombatController()

    def get_current_frame_data(self):
        return FakeFrame()


class EnemyCombatHitboxTests(unittest.TestCase):
    def test_animation_attack_rect_is_ignored_during_enemy_windup(self):
        enemy = FakeEnemy()
        enemy.combat.start_attack_timing(enemy)
        hitboxes = EnemyGeometry()

        self.assertIsNone(hitboxes.get_attack_rect(enemy))

    def test_enemy_attack_rect_comes_from_attack_data_during_active_window(self):
        enemy = FakeEnemy()
        enemy.combat.start_attack_timing(enemy)
        hitboxes = EnemyGeometry()

        for _ in range(enemy.attack_data.windup):
            enemy.combat.advance_attack_timing(enemy)

        attack_rect = hitboxes.get_attack_rect(enemy)

        self.assertEqual((attack_rect.x, attack_rect.y, attack_rect.width, attack_rect.height),
                         (340, 470, 50, 20))

    def test_enemy_attack_rect_mirrors_left_from_anchor(self):
        enemy = FakeEnemy()
        enemy.facing_right = False
        enemy.combat.start_attack_timing(enemy)
        hitboxes = EnemyGeometry()

        for _ in range(enemy.attack_data.windup):
            enemy.combat.advance_attack_timing(enemy)

        attack_rect = hitboxes.get_attack_rect(enemy)

        self.assertEqual((attack_rect.x, attack_rect.y, attack_rect.width, attack_rect.height),
                         (210, 470, 50, 20))


if __name__ == "__main__":
    unittest.main()
