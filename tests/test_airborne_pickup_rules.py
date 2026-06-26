import unittest

import pygame

from game.systems.inventory_system import update_player_weapon_interaction
from game.systems.loot_system import update_loot_pickup


class FakeAir:
    def __init__(self, is_grounded):
        self.is_grounded = is_grounded


class FakeWeaponSlot:
    def __init__(self):
        self.weapon = None
        self.picked_up_weapon = None

    def pick_up(self, weapon):
        self.weapon = weapon
        self.picked_up_weapon = weapon

    def drop(self, player):
        self.weapon = None


class FakePlayer:
    def __init__(self, is_grounded):
        self.x = 100
        self.y = 100
        self.width = 40
        self.height = 80
        self.movement = type("M", (), {"air": FakeAir(is_grounded)})()
        self.weapon_slot = FakeWeaponSlot()
        self.health = type("FakeHealth", (), {"hp": 50, "max_hp": 100})()

    def get_collision_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


class FakeWeapon:
    picked_up = False
    damage = 1

    def get_rect(self):
        return pygame.Rect(100, 100, 30, 30)


class FakeLoot:
    def __init__(self):
        self.active = True
        self.loot_type = "health"

    def get_rect(self):
        return pygame.Rect(100, 100, 30, 30)


class FakeGameState:
    def __init__(self, player):
        self.player = player
        self.weapons = [FakeWeapon()]
        self.loot_items = [FakeLoot()]


class FakeKeys:
    def __getitem__(self, key):
        return False


class AirbornePickupRuleTests(unittest.TestCase):
    def test_airborne_player_cannot_pick_up_weapon(self):
        player = FakePlayer(is_grounded=False)
        game_state = FakeGameState(player)

        update_player_weapon_interaction(game_state, FakeKeys())

        self.assertIsNone(player.weapon_slot.weapon)

    def test_grounded_player_can_pick_up_weapon(self):
        player = FakePlayer(is_grounded=True)
        game_state = FakeGameState(player)

        update_player_weapon_interaction(game_state, FakeKeys())

        self.assertIs(player.weapon_slot.weapon, game_state.weapons[0])

    def test_airborne_player_cannot_pick_up_loot(self):
        player = FakePlayer(is_grounded=False)
        game_state = FakeGameState(player)

        update_loot_pickup(game_state)

        self.assertTrue(game_state.loot_items[0].active)
        self.assertEqual(player.health.hp, 50)

    def test_grounded_player_can_pick_up_loot(self):
        player = FakePlayer(is_grounded=True)
        game_state = FakeGameState(player)

        update_loot_pickup(game_state)

        self.assertFalse(game_state.loot_items[0].active)
        self.assertEqual(player.health.hp, 70)


if __name__ == "__main__":
    unittest.main()
