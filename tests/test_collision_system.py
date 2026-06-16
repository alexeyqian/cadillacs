import unittest

import pygame

from game.systems.collision_system import resolve_player_enemy_collisions


class FakePlayer:
    DEAD = "DEAD"

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = "IDLE"
        self.collision_box_w = 40
        self.collision_box_h = 20

    def get_collision_rect(self):
        return pygame.Rect(
            int(self.x - self.collision_box_w / 2),
            int(self.y - self.collision_box_h),
            self.collision_box_w,
            self.collision_box_h,
        )


class FakeEnemy:
    DEAD = "DEAD"
    GRABBED = "GRABBED"
    THROWN = "THROWN"

    def __init__(self, x, y, state="IDLE"):
        self.x = x
        self.y = y
        self.state = state
        self.collision_box_w = 40
        self.collision_box_h = 20

    def get_collision_rect(self):
        return pygame.Rect(
            int(self.x - self.collision_box_w / 2),
            int(self.y - self.collision_box_h),
            self.collision_box_w,
            self.collision_box_h,
        )


class FakeGameState:
    def __init__(self, player, enemies):
        self.player = player
        self.enemies = enemies


class CollisionSystemTests(unittest.TestCase):
    def test_player_is_blocked_when_walking_into_enemy_from_left(self):
        player = FakePlayer(125, 500)
        enemy = FakeEnemy(140, 500)
        game_state = FakeGameState(player, [enemy])

        resolve_player_enemy_collisions(game_state, old_player_x=90, old_player_y=500)

        self.assertEqual(player.get_collision_rect().right, enemy.get_collision_rect().left)

    def test_player_is_blocked_when_walking_into_enemy_from_same_x_lane(self):
        player = FakePlayer(140, 505)
        enemy = FakeEnemy(140, 500)
        game_state = FakeGameState(player, [enemy])

        resolve_player_enemy_collisions(game_state, old_player_x=140, old_player_y=535)

        self.assertEqual(player.get_collision_rect().top, enemy.get_collision_rect().bottom)

    def test_thrown_enemy_does_not_block_player_movement(self):
        player = FakePlayer(125, 500)
        enemy = FakeEnemy(140, 500, state=FakeEnemy.THROWN)
        game_state = FakeGameState(player, [enemy])

        resolve_player_enemy_collisions(game_state, old_player_x=90, old_player_y=500)

        self.assertTrue(player.get_collision_rect().colliderect(enemy.get_collision_rect()))


if __name__ == "__main__":
    unittest.main()
