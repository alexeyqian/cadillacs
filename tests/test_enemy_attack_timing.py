import unittest
from dataclasses import replace

from game.entities.boss_enemy import BossEnemy

from game.entities.attack_data import DEFAULT_ENEMY_ATTACK_DATA
from game.entities.enemy_config import get_enemy_config
from game.entities.enemy import Enemy
from game.entities.enemy_combat_controller import EnemyCombatController
from game.entities.enemy_lifecycle_controller import EnemyLifecycleController
from game.entities.enemy_reaction_controller import EnemyReactionController
from game.entities.enemy_state import EnemyState
from game.entities.enemy_state_resolver import EnemyStateResolver
from game.entities.raptor_enemy import RaptorEnemy
from game.entities.ranged_enemy import RangedEnemy
from game.settings import BAT_DAMAGE


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


class FakeHealth:
    def __init__(self, hp=100):
        self.hp = hp

    def take_damage(self, damage):
        self.hp -= damage
        return self.hp <= 0


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
        self.attack_delay = 3
        self.attack_windup = 3
        self.attack_active = 2
        self.attack_recovery = 2
        self.attack_damage = 10
        self.attack_lane_reach = 0
        self.attack_range = 40
        self.attack_lane_range = 20
        self.attack_cooldown_duration = 30
        self.action_lock_remaining = 0
        self.health = FakeHealth()
        self.hit_stun_duration = 15
        self.hit_stun_remaining = 0
        self.flinch_damage_threshold = 0
        self.attack_flinch_damage_threshold = 0
        self.knockback_velocity = 0
        self.animation_controller = FakeAnimationController()
        self.combat = EnemyCombatController()

    def face_player(self, player):
        self.facing_right = player.x > self.x

    def get_attack_rect(self):
        return AlwaysCollidingRect()

    def is_attack_active(self):
        attack_timer = self.combat.get_attack_timer(self)
        return self.attack_windup <= attack_timer < self.attack_windup + self.attack_active

    def get_attack_total_duration(self):
        return self.attack_windup + self.attack_active + self.attack_recovery

    def uses_melee_attack_slot(self):
        return True

    def start_attack(self):
        self.combat.start_attack(self)

    def update_animation(self):
        self.animation_controller.play(self.state)

    def should_knockdown_from_damage(self, damage):
        return False

    def knockdown(self):
        EnemyReactionController().knockdown(self)

    def die(self):
        EnemyReactionController().die(self)


class FakePlayer:
    def __init__(self):
        self.x = 10
        self.y = 0
        self.damage_taken = 0
        self.combat = None

    def get_hurt_rect(self):
        return AlwaysCollidingRect()

    def take_damage(self, damage):
        self.damage_taken += damage


class FakePlayerCombat:
    def __init__(self, phase_name):
        self.phase_name = phase_name
        self.is_attacking = True

    def get_attack_phase_name(self):
        return self.phase_name


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
        self.assertEqual(enemy.combat.decision_timer, 1)

        resolver.prepare_or_start_attack(enemy)
        self.assertEqual(enemy.state, enemy.IDLE)
        self.assertEqual(enemy.combat.decision_timer, 2)

        resolver.prepare_or_start_attack(enemy)
        self.assertEqual(enemy.state, enemy.ATTACK)
        self.assertEqual(enemy.combat.get_attack_timer(enemy), 0)
        self.assertEqual(enemy.combat.decision_timer, 0)

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

    def test_enemy_attack_uses_shared_attack_manager_timer(self):
        enemy = FakeEnemy()

        enemy.start_attack()
        enemy.combat.advance_attack_timing(enemy)

        self.assertEqual(enemy.combat.attack_manager.current_attack_name, enemy.ATTACK)
        self.assertEqual(enemy.combat.attack_manager.attack_timer, 1)

    def test_real_enemy_total_duration_comes_from_attack_data(self):
        enemy = Enemy.__new__(Enemy)
        enemy.attack_data = replace(
            DEFAULT_ENEMY_ATTACK_DATA,
            windup=3,
            active=2,
            recovery=1,
        )

        self.assertEqual(enemy.get_attack_total_duration(), 6)

    def test_clash_recovery_cancels_enemy_attack(self):
        enemy = FakeEnemy()
        enemy.state = enemy.ATTACK
        enemy.combat.set_attack_timer(enemy, 4)
        enemy.combat.decision_timer = 2
        enemy.combat.already_hit = True
        enemy.combat.has_attack_slot = True
        controller = enemy.combat

        controller.start_clash_recovery(enemy)

        self.assertEqual(enemy.state, enemy.RECOIL)
        self.assertEqual(enemy.action_lock_remaining, enemy.attack_cooldown_duration)
        self.assertEqual(enemy.combat.get_attack_timer(enemy), 0)
        self.assertEqual(enemy.combat.decision_timer, 0)
        self.assertFalse(enemy.combat.already_hit)
        self.assertFalse(enemy.combat.has_attack_slot)
        self.assertEqual(enemy.combat.cooldown, enemy.attack_cooldown_duration)

    def test_knockdown_cancels_enemy_attack_manager(self):
        enemy = FakeEnemy()
        enemy.start_attack()
        enemy.combat.advance_attack_timing(enemy)

        EnemyReactionController().knockdown(enemy)

        self.assertEqual(enemy.state, enemy.KNOCKDOWN)
        self.assertEqual(enemy.combat.get_attack_timer(enemy), 0)
        self.assertFalse(enemy.combat.attack_manager.is_attacking)
        self.assertFalse(enemy.combat.has_attack_slot)

    def test_heavy_attack_poise_ignores_light_flinch_during_attack(self):
        enemy = FakeEnemy()
        enemy.flinch_damage_threshold = 10
        enemy.attack_flinch_damage_threshold = BAT_DAMAGE
        enemy.start_attack()

        EnemyReactionController().take_damage(enemy, BAT_DAMAGE - 1, attacker_x=-100)

        self.assertEqual(enemy.state, enemy.ATTACK)
        self.assertTrue(enemy.combat.attack_manager.is_attacking)

        EnemyReactionController().take_damage(enemy, BAT_DAMAGE, attacker_x=-100)

        self.assertEqual(enemy.state, enemy.HIT)
        self.assertFalse(enemy.combat.attack_manager.is_attacking)

    def test_enemy_reaction_uses_custom_knockback_velocity(self):
        enemy = FakeEnemy()
        enemy.x = 100

        EnemyReactionController().take_damage(
            enemy,
            10,
            attacker_x=50,
            knockback_velocity=18,
        )

        self.assertEqual(enemy.state, enemy.HIT)
        self.assertEqual(enemy.knockback_velocity, 18)

    def test_enemy_reaction_uses_custom_hit_stun_duration(self):
        enemy = FakeEnemy()

        EnemyReactionController().take_damage(
            enemy,
            10,
            attacker_x=-100,
            hit_stun_duration=24,
        )

        self.assertEqual(enemy.state, enemy.HIT)
        self.assertEqual(enemy.hit_stun_remaining, 24)

    def test_enemy_uses_shorter_attack_delay_during_player_recovery(self):
        enemy = FakeEnemy()
        player = FakePlayer()
        player.combat = FakePlayerCombat("RECOVERY")
        resolver = EnemyStateResolver()

        self.assertEqual(resolver.get_required_attack_delay(enemy, player), enemy.attack_delay)

    def test_enemy_attack_delay_stays_normal_outside_player_recovery(self):
        enemy = FakeEnemy()
        player = FakePlayer()
        player.combat = FakePlayerCombat("ACTIVE")
        resolver = EnemyStateResolver()

        self.assertEqual(resolver.get_required_attack_delay(enemy, player), enemy.attack_delay)

    def test_enemy_configs_raise_pressure_without_removing_archetype_identity(self):
        ferris = get_enemy_config("ferris")
        gneiss = get_enemy_config("gneiss")
        black_elmer = get_enemy_config("black_elmer")
        ranged = get_enemy_config("ranged")
        boss = get_enemy_config("boss")

        self.assertGreater(ferris.attack_range, 90)
        self.assertLess(ferris.attack.cooldown, 45)
        self.assertLess(gneiss.attack.delay, ferris.attack.delay)
        self.assertLess(gneiss.attack.cooldown, ferris.attack.cooldown)
        self.assertGreater(black_elmer.attack_range, ferris.attack_range)
        self.assertEqual(black_elmer.attack_flinch_damage_threshold, BAT_DAMAGE)
        self.assertEqual(boss.attack_flinch_damage_threshold, BAT_DAMAGE)
        self.assertLess(ranged.attack.cooldown, 90)

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
