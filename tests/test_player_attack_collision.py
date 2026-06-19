import unittest

import pygame

from game.entities.player_combat_controller import PlayerCombatController
from game.data.player_config import PLAYER_ATTACKS, WEAPON_PLAYER_ATTACKS
from game.combat.hit_reaction import HitReaction
from game.systems.combat_system import damage_enemy, handle_player_attack_collision


class FakeMovement:
    def __init__(self):
        self.is_running = False
        self.can_run_attack = False

    def can_start_run_attack(self):
        return self.can_run_attack

    def start_run_attack_momentum(self, owner):
        pass


class FakeStateMachine:
    def change_to(self, owner, state):
        owner.state = state


class FakeWeaponSlot:
    def __init__(self, weapon=None):
        self.weapon = weapon


class FakeWeapon:
    def __init__(self, weapon_type, is_ranged=False):
        self.weapon_type = weapon_type
        self.is_ranged = is_ranged


class FakePlayer:
    ATTACK_1 = "ATTACK_1"
    ATTACK_2 = "ATTACK_2"
    ATTACK_3 = "ATTACK_3"
    RUN_ATTACK = "RUN_ATTACK"
    JUMP_ATTACK = "JUMP_ATTACK"
    GRAB_KNEE = "GRAB_KNEE"
    DEAD = "DEAD"

    def __init__(self, weapon=None):
        self.x = 100
        self.y = 100
        self.state = self.ATTACK_1
        self.facing_right = True
        self.movement = FakeMovement()
        self.state_machine = FakeStateMachine()
        self.weapon_slot = FakeWeaponSlot(weapon)
        self.attacks = PLAYER_ATTACKS
        self.weapon_attacks = WEAPON_PLAYER_ATTACKS
        self.combat = PlayerCombatController()
        self.combat.start_attack(self)
        while not self.combat.is_attack_active():
            self.combat.update_timers(self)
        self.grab = type("FakeGrab", (), {"grabbed_enemy": None})()

    def start_running_attack(self):
        self.combat.cancel_attack()
        self.movement.is_running = True
        self.movement.can_run_attack = True
        self.combat.start_attack(self)
        while not self.combat.is_attack_active():
            self.combat.update_timers(self)

    def get_attack_rect(self):
        return pygame.Rect(100, 100, 100, 100)

    def get_attack_data(self, attack_name):
        weapon = getattr(self.weapon_slot, "weapon", None)
        weapon_type = getattr(weapon, "weapon_type", weapon)
        weapon_attack = self.weapon_attacks.get((weapon_type, attack_name))
        if weapon_attack and not getattr(weapon, "is_ranged", False):
            return weapon_attack
        return self.attacks.get(attack_name)

class FakeHealth:
    hp = 100
    max_hp = 100


class FakeEnemy:
    ATTACK = "ATTACK"
    DEAD = "DEAD"

    def __init__(self):
        self.x = 120
        self.y = 100
        self.state = "IDLE"
        self.health = FakeHealth()
        self.damage_taken = 0
        self.knockback_velocity_taken = None
        self.hit_stun_duration_taken = None

    def get_attack_rect(self):
        return None

    def get_hurt_rect(self):
        return pygame.Rect(120, 100, 40, 40)

    def get_logical_rect(self):
        return self.get_hurt_rect()

    def take_damage(
        self,
        damage,
        attacker_x,
        knockback_velocity=10,
        hit_stun_duration=None,
    ):
        self.damage_taken += damage
        self.knockback_velocity_taken = knockback_velocity
        self.hit_stun_duration_taken = hit_stun_duration


class ReactionEnemy:
    def __init__(self):
        self.damage_taken = 0
        self.attacker_x_taken = None
        self.reaction_taken = None

    def take_damage(self, damage, attacker_x, reaction=None):
        self.damage_taken += damage
        self.attacker_x_taken = attacker_x
        self.reaction_taken = reaction


class FakeLevel:
    def get_lane_distance(self, a, b):
        return 0


class FakeScoreManager:
    def __init__(self):
        self.hit_count = 0

    def register_hit(self):
        self.hit_count += 1


class FakeGameState:
    def __init__(self, player_weapon=None, enemy_count=2):
        self.player = FakePlayer(player_weapon)
        self.enemies = [FakeEnemy() for _ in range(enemy_count)]
        self.objects = []
        self.level = FakeLevel()
        self.floating_texts = []
        self.hit_sparks = []
        self.score_manager = FakeScoreManager()


class PlayerAttackCollisionTests(unittest.TestCase):
    def test_damage_enemy_prefers_shared_hit_reaction_api(self):
        enemy = ReactionEnemy()
        reaction = HitReaction(stun_frames=14, knockback_velocity=8)

        damage_enemy(enemy, 12, attacker_x=100, hit_reaction=reaction)

        self.assertEqual(enemy.damage_taken, 12)
        self.assertEqual(enemy.attacker_x_taken, 100)
        self.assertIs(enemy.reaction_taken, reaction)

    def test_default_player_attack_hits_only_one_target(self):
        game_state = FakeGameState()

        handle_player_attack_collision(game_state)

        self.assertGreater(game_state.enemies[0].damage_taken, 0)
        self.assertEqual(game_state.enemies[1].damage_taken, 0)
        self.assertEqual(game_state.score_manager.hit_count, 1)

    def test_player_attack_can_hit_multiple_targets_when_data_allows_it(self):
        game_state = FakeGameState(player_weapon=FakeWeapon("bat"))

        handle_player_attack_collision(game_state)

        self.assertGreater(game_state.enemies[0].damage_taken, 0)
        self.assertGreater(game_state.enemies[1].damage_taken, 0)
        self.assertEqual(game_state.score_manager.hit_count, 2)

    def test_run_attack_uses_stronger_enemy_knockback(self):
        game_state = FakeGameState()
        normal_knockback = game_state.player.combat.get_attack_knockback_velocity(
            game_state.player
        )
        game_state.player.start_running_attack()

        handle_player_attack_collision(game_state)

        self.assertGreater(
            game_state.enemies[0].knockback_velocity_taken,
            normal_knockback,
        )

    def test_run_attack_uses_longer_enemy_hit_stun(self):
        game_state = FakeGameState()
        normal_hit_stun = game_state.player.combat.get_attack_enemy_hit_stun_duration(
            game_state.player
        )
        game_state.player.start_running_attack()

        handle_player_attack_collision(game_state)

        self.assertGreater(
            game_state.enemies[0].hit_stun_duration_taken,
            normal_hit_stun,
        )

    def test_run_attack_can_hit_multiple_attackable_enemies(self):
        game_state = FakeGameState(enemy_count=3)
        game_state.player.start_running_attack()

        handle_player_attack_collision(game_state)

        for enemy in game_state.enemies:
            self.assertGreater(enemy.damage_taken, 0)
        self.assertEqual(game_state.score_manager.hit_count, 3)


if __name__ == "__main__":
    unittest.main()
