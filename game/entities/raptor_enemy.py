from game.entities.enemy import Enemy
from game.animation.animation_config import *
from game.assets.placeholder.enemy_frames import create_raptor_frames


class RaptorEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(
            x,
            y,
            walk_config=RAPTOR_ENEMY_WALK,
            attack_config=RAPTOR_ENEMY_ATTACK,
            fallback_frame_factory=create_raptor_frames
        )

        self.max_hp = 120
        self.hp = self.max_hp
        self.width = 70
        self.height = 60
        self.speed = 3.5
        self.attack_damage = 14
        self.attack_range = 70
        self.detect_range = 400
        self.leap_cooldown = 0
        self.leap_speed = 12

    def update(self, player, enemies):
        if self.leap_cooldown > 0:
            self.leap_cooldown -= 1
        # todo: why not call super() first
        super().update(player, enemies)

    def update_attack(self, player):
        if self.attack_cooldown > 0:
            return
        player.take_damage(self.attack_damage)
        self.attack_cooldown = 50
        
        if self.leap_cooldown == 0:
            self.leap_toward_player(player)
            self.leap_cooldown = 120

    def leap_toward_player(self, player):
        if player.x > self.x:
            self.x += self.leap_speed
        else:
            self.x -= self.leap_speed
