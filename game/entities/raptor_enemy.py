from game.entities.enemy import Enemy
from game.animation.animation_config import *
from game.assets.placeholder.enemy_frames import create_raptor_frames
from game.settings import *


class RaptorEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y,
            walk_config=RAPTOR_ENEMY_WALK,
            attack_config=RAPTOR_ENEMY_ATTACK,
            fallback_frame_factory=create_raptor_frames
        )
        self.width = RAPTOR_ENEMY_W
        self.height = RAPTOR_ENEMY_H
        self.max_hp = RAPTOR_ENEMY_MAX_HP
        self.hp = self.max_hp
        self.speed = RAPTOR_ENEMY_SPEED
        self.attack_damage = RAPTOR_ENEMY_ATTACK_DAMAGE

        # properties special to current raptor enemy
        self.leap_cooldown = 0
        self.leap_speed = 12

    def update(self, player, enemies):
        if self.leap_cooldown > 0:
            self.leap_cooldown -= 1
        # todo: why not call super() first
        super().update(player, enemies)

    def update_attack(self, player):
        if self.attack_timer == 0 and self.leap_cooldown == 0:
            self.leap_toward_player(player)
            self.leap_cooldown = 120

        super().update_attack(player)

    def leap_toward_player(self, player):
        if player.x > self.x:
            self.facing_right = True
            self.x += self.leap_speed
        else:
            self.facing_right = False
            self.x -= self.leap_speed
