import unittest

from game.entities.boss_enemy import BossEnemy
from game.entities.enemy_combat_controller import EnemyCombatController
from game.entities.enemy_reaction_controller import EnemyReactionController
from game.entities.enemy_state import EnemyState
from game.entities.enemy_state_resolver import EnemyStateResolver
from game.entities.raptor_enemy import RaptorEnemy
from game.entities.ranged_enemy import RangedEnemy


class AlwaysCollidingRect:
    def colliderect(self, other):
        return True


class SameLaneLevel:
    def get_lane_distance(self, a, b):
        return 0


class FakeAnimationController:
    def play(self, state):
        self.played_state = state

    def reset_current_animation(self):
        self.reset = True


class FakeEnemy:
    IDLE = EnemyState.IDLE
    PATROL = EnemyState.PATROL
    CHASE = EnemyState.CHASE
    ATTACK = EnemyState.ATTACK
    HIT = EnemyState.HIT
    RECOIL = EnemyState.RECOIL
    DEAD = EnemyState.DEAD
    GRABBED = EnemyState.GRABBED
    THROWN = EnemyState.THROWN
    KNOCKDOWN = EnemyState.KNOCKDOWN
    GETUP = EnemyState.GETUP

    def __init__(self):
        self.state = self.IDLE
        self.x = 0
        self.y = 0
        self.attack_timer = 0
        self.attack_decision_timer = 0
        self.attack_delay = 3
        self.attack_windup = 3
        self.attack_active = 2
        self.attack_recovery = 2
        self.attack_damage = 10
        self.attack_lane_reach = 0
        self.attack_range = 40
        self.attack_lane_range = 20
        self.attack_cooldown = 0
        self.attack_cooldown_duration = 30
        self.attack_clash_recovery_duration = 12
        self.attack_clash_cooldown_duration = 20
        self.attack_already_hit = False
        self.has_attack_slot = False
        self.action_lock_remaining = 0
        self.animation_controller = FakeAnimationController()

    def face_player(self, player):
        self.facing_right = player.x > self.x

    def get_attack_rect(self):
        return AlwaysCollidingRect()

    def is_attack_active(self):
        return self.attack_windup <= self.attack_timer < self.attack_windup + self.attack_active

    def get_attack_total_duration(self):
        return self.attack_windup + self.attack_active + self.attack_recovery

    def uses_melee_attack_slot(self):
        return True

    def start_attack(self):
        EnemyCombatController().start_attack(self)


class FakePlayer:
    def __init__(self):
        self.x = 10
        self.y = 0
        self.damage_taken = 0

    def get_hurt_rect(self):
        return AlwaysCollidingRect()

    def take_damage(self, damage):
        self.damage_taken += damage


class FakeRangedEnemy(FakeEnemy):
    def __init__(self):
        super().__init__()
        self.pending_projectile = None
        self.shot_fired = False
        self.attack_windup = 2
        self.attack_active = 2
        self.attack_recovery = 2


class FakeBoss:
    def __init__(self):
        self.special_attack_warning_duration = 2
        self.special_attack_warning_remaining = 0
        self.special_attack_warning_text = ""
        self.special_attack_cooldown = 0
        self.special_attack_cooldown_duration = 10
        self.performed_special_attack = False

    def face_player(self, player):
        self.faced_player = True

    def perform_special_attack(self, player):
        self.performed_special_attack = True

    def start_special_attack_warning(self):
        BossEnemy.start_special_attack_warning(self)


class FakeRaptor:
    def __init__(self):
        self.leap_cooldown = 0
        self.has_leaped_this_attack = False
        self.attack_windup = 18
        self.leap_startup_frames = 4
        self.attack_timer = 0


class EnemyAttackTimingTests(unittest.TestCase):
    def test_attack_delay_waits_before_starting_attack(self):
        enemy = FakeEnemy()
        resolver = EnemyStateResolver()

        resolver.prepare_or_start_attack(enemy)
        self.assertEqual(enemy.state, enemy.IDLE)
        self.assertEqual(enemy.attack_decision_timer, 1)

        resolver.prepare_or_start_attack(enemy)
        self.assertEqual(enemy.state, enemy.IDLE)
        self.assertEqual(enemy.attack_decision_timer, 2)

        resolver.prepare_or_start_attack(enemy)
        self.assertEqual(enemy.state, enemy.ATTACK)
        self.assertEqual(enemy.attack_timer, 0)
        self.assertEqual(enemy.attack_decision_timer, 0)

    def test_enemy_attack_damages_only_during_active_frames(self):
        enemy = FakeEnemy()
        enemy.state = enemy.ATTACK
        player = FakePlayer()
        controller = EnemyCombatController()
        level = SameLaneLevel()

        controller.update_attack(enemy, level, player)
        controller.update_attack(enemy, level, player)
        self.assertEqual(player.damage_taken, 0)

        controller.update_attack(enemy, level, player)
        self.assertEqual(player.damage_taken, enemy.attack_damage)

    def test_enemy_attack_uses_shared_attack_controller_timer(self):
        enemy = FakeEnemy()
        controller = EnemyCombatController()

        enemy.start_attack()
        controller.update_attack_timer(enemy)

        self.assertTrue(hasattr(enemy, "attack_controller"))
        self.assertEqual(enemy.attack_controller.current_attack_name, enemy.ATTACK)
        self.assertEqual(enemy.attack_controller.attack_timer, 1)
        self.assertEqual(enemy.attack_timer, 1)

    def test_clash_recovery_cancels_enemy_attack(self):
        enemy = FakeEnemy()
        enemy.state = enemy.ATTACK
        enemy.attack_timer = 4
        enemy.attack_decision_timer = 2
        enemy.attack_already_hit = True
        enemy.has_attack_slot = True
        controller = EnemyCombatController()

        controller.start_clash_recovery(enemy)

        self.assertEqual(enemy.state, enemy.RECOIL)
        self.assertEqual(enemy.action_lock_remaining, enemy.attack_clash_recovery_duration)
        self.assertEqual(enemy.attack_timer, 0)
        self.assertEqual(enemy.attack_decision_timer, 0)
        self.assertFalse(enemy.attack_already_hit)
        self.assertFalse(enemy.has_attack_slot)
        self.assertEqual(enemy.attack_cooldown, enemy.attack_clash_cooldown_duration)

    def test_knockdown_cancels_enemy_attack_controller(self):
        enemy = FakeEnemy()
        enemy.start_attack()
        EnemyCombatController().update_attack_timer(enemy)

        EnemyReactionController().knockdown(enemy)

        self.assertEqual(enemy.state, enemy.KNOCKDOWN)
        self.assertEqual(enemy.attack_timer, 0)
        self.assertFalse(enemy.attack_controller.is_attacking)
        self.assertFalse(enemy.has_attack_slot)

    def test_ranged_enemy_fires_once_during_active_window(self):
        enemy = FakeRangedEnemy()
        enemy.state = enemy.ATTACK
        enemy.x = 100
        enemy.y = 300
        player = FakePlayer()
        player.x = 200
        level = SameLaneLevel()

        RangedEnemy.update_attack(enemy, level, player)
        self.assertIsNone(enemy.pending_projectile)

        RangedEnemy.update_attack(enemy, level, player)
        projectile = enemy.pending_projectile
        self.assertIsNotNone(projectile)
        self.assertEqual(projectile.lane_y, enemy.y)

        enemy.pending_projectile = None
        RangedEnemy.update_attack(enemy, level, player)
        self.assertIsNone(enemy.pending_projectile)

    def test_raptor_leaps_in_late_windup(self):
        raptor = FakeRaptor()

        raptor.attack_timer = raptor.attack_windup - raptor.leap_startup_frames - 1
        self.assertFalse(RaptorEnemy.should_leap_now(raptor))

        raptor.attack_timer = raptor.attack_windup - raptor.leap_startup_frames
        self.assertTrue(RaptorEnemy.should_leap_now(raptor))

    def test_boss_special_warning_fires_after_telegraph(self):
        boss = FakeBoss()
        player = FakePlayer()

        BossEnemy.update_special_attack(boss, player)
        self.assertEqual(boss.special_attack_warning_remaining, boss.special_attack_warning_duration)
        self.assertFalse(boss.performed_special_attack)

        BossEnemy.update_special_attack(boss, player)
        self.assertFalse(boss.performed_special_attack)

        BossEnemy.update_special_attack(boss, player)
        self.assertTrue(boss.performed_special_attack)
        self.assertEqual(boss.special_attack_cooldown, boss.special_attack_cooldown_duration)


if __name__ == "__main__":
    unittest.main()
