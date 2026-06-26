import unittest

import pygame

from game.controllers.player_combat_controller import PlayerCombatController
from game.components.player_combat_state import PlayerCombatState
from game.components.player_grab_state import PlayerGrabState
from game.data.player_config import DEFAULT_PLAYER_ATTACKS, DEFAULT_WEAPON_PLAYER_ATTACKS
from game.combat.damage_request import DamageRequest
from game.combat.hit_reaction import HitReaction
from game.input.player_input_state import PlayerInputState
from game.systems.combat_system import damage_enemy, handle_player_attack_collision


class FakeRunMovement:
    def __init__(self):
        self.can_run_attack = False

    def can_start_run_attack(self):
        return self.can_run_attack


class FakeMovement:
    def __init__(self):
        self.is_running = False
        self.last_run_attack_distance = 0
        self.run_movement = FakeRunMovement()

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
    ATTACK = "ATTACK"
    ATTACK2 = "ATTACK2"
    ATTACK3 = "ATTACK3"
    RUN_ATTACK = "RUN_ATTACK"
    JUMP_ATTACK = "JUMP_ATTACK"
    GRAB_KNEE = "GRAB_KNEE"
    DEAD = "DEAD"

    def __init__(self, weapon=None):
        self.x = 100
        self.y = 100
        self.state = self.ATTACK
        self.facing_right = True
        self.movement = FakeMovement()
        self.state_machine = FakeStateMachine()
        self.weapon_slot = FakeWeaponSlot(weapon)
        self.combat_controller = PlayerCombatController()
        self.combat_state = PlayerCombatState()
        self.combat_state.attacks = DEFAULT_PLAYER_ATTACKS
        self.combat_state.weapon_attacks = DEFAULT_WEAPON_PLAYER_ATTACKS
        self.grab_state = PlayerGrabState()
        self.input_state = PlayerInputState()
        self.combat_controller.start_attack(self)
        while not self.combat_state.attack_manager.is_active():
            self.combat_controller.update_attack(self)

    def start_running_attack(self):
        self.combat_controller.cancel_attack(self)
        self.movement.is_running = True
        self.movement.run_movement.can_run_attack = True
        self.combat_controller.start_attack(self)
        while not self.combat_state.attack_manager.is_active():
            self.combat_controller.update_attack(self)

    def get_attack_rect(self):
        return pygame.Rect(100, 100, 100, 100)

    def get_attack_data(self, attack_name):
        weapon = getattr(self.weapon_slot, "weapon", None)
        weapon_type = getattr(weapon, "weapon_type", weapon)
        weapon_attack = self.combat_state.weapon_attacks.get((weapon_type, attack_name))
        if weapon_attack and not getattr(weapon, "is_ranged", False):
            return weapon_attack
        return self.combat_state.attacks.get(attack_name)

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
        self.enemy_id = "ferris"
        self.health = FakeHealth()
        self.damage_taken = 0
        self.knockback_velocity_taken = None
        self.hit_stun_duration_taken = None

    def get_attack_rect(self):
        return None

    def get_hurt_rect(self):
        return pygame.Rect(120, 100, 40, 40)

    def get_frame_rect(self):
        return self.get_hurt_rect()

    def take_damage(
        self,
        damage,
        attacker_x,
        reaction=None,
    ):
        self.damage_taken += damage
        if reaction:
            self.knockback_velocity_taken = reaction.knockback_velocity
            self.hit_stun_duration_taken = reaction.stun_frames


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

    def test_damage_enemy_accepts_damage_request(self):
        enemy = ReactionEnemy()
        reaction = HitReaction(stun_frames=12, knockback_velocity=7)

        damage_enemy(enemy, DamageRequest(9, attacker_x=80, reaction=reaction))

        self.assertEqual(enemy.damage_taken, 9)
        self.assertEqual(enemy.attacker_x_taken, 80)
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
        normal_knockback = DEFAULT_PLAYER_ATTACKS["ATTACK"].knockback_velocity
        game_state.player.start_running_attack()

        handle_player_attack_collision(game_state)

        self.assertGreater(
            game_state.enemies[0].knockback_velocity_taken,
            normal_knockback,
        )

    def test_run_attack_uses_longer_enemy_hit_stun(self):
        game_state = FakeGameState()
        normal_hit_stun = DEFAULT_PLAYER_ATTACKS["ATTACK"].hit_stun_duration
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
