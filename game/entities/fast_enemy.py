from game.entities.enemy import Enemy
from game.animation.animation_config import *
from game.settings import *

class FastEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y,
                    idle_config=FAST_ENEMY_IDLE,
                    walk_config=FAST_ENEMY_WALK,
                    attack_config=FAST_ENEMY_ATTACK)

        self.width = FAST_ENEMY_W
        self.height = FAST_ENEMY_H
        self.max_hp = FAST_ENEMY_MAX_HP
        self.hp = self.max_hp
        self.speed = FAST_ENEMY_SPEED
        self.attack_damage = FAST_ENEMY_ATTACK_DAMAGE
        # give enemy different personalities
        self.detect_range = FAST_ENEMY_DETECT_RANGE
