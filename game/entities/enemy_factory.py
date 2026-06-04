from game.entities.enemy import Enemy
from game.entities.fast_enemy import FastEnemy
from game.entities.heavy_enemy import HeavyEnemy
from game.entities.ranged_enemy import RangedEnemy

class EnemyFactory:
    @staticmethod
    def create_enemy(enemy_type, x, y):
        if enemy_type == "fast":
            return FastEnemy(x, y)
        if enemy_type == "heavy":
            return HeavyEnemy(x, y)
        if enemy_type == "ranged":
            return RangedEnemy(x, y)
        
        return Enemy(x, y)

