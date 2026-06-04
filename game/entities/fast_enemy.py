from game.entities.enemy import Enemy
from game.animation.animation_config import *

class FastEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y,
                    idle_config=FAST_ENEMY_IDLE,
                    walk_config=FAST_ENEMY_WALK,
                    attack_config=FAST_ENEMY_ATTACK)

        self.max_hp = 60
        self.hp = self.max_hp
        self.speed = 4
        self.attack_damage = 8
        # give enemy different personalities
        self.detect_range = 350
