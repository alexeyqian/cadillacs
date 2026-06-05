from game.entities.enemy import Enemy
from game.animation.animation_config import *
from game.settings import *

class HeavyEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, 
                        idle_config=HEAVY_ENEMY_IDLE,
                        walk_config=HEAVY_ENEMY_WALK,
                        attack_config=HEAVY_ENEMY_ATTACK)
        self.width = HEAVY_ENEMY_W
        self.height = HEAVY_ENEMY_H
        self.max_hp = HEAVY_ENEMY_MAX_HP
        self.hp = self.max_hp
        self.speed = HEAVY_ENEMY_SPEED
        self.attack_damage = HEAVY_ENEMY_ATTACK_DAMAGE
        self.detect_range = 180
