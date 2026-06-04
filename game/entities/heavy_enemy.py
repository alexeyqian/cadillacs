from game.entities.enemy import Enemy
from game.animation.animation_config import *

class HeavyEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, 
                        idle_config=HEAVY_ENEMY_IDLE,
                        walk_config=HEAVY_ENEMY_WALK,
                        attack_config=HEAVY_ENEMY_ATTACK)

        self.max_hp = 250
        self.hp = self.max_hp
        self.speed = 1
        self.attack_damage = 25
        self.width = 70
        self.height = 100
        self.detect_range = 180
