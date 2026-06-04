from game.entities.enemy import Enemy
from game.entities.boss_enemy import BossEnemy
from game.entities.enemy_factory import EnemyFactory

class Wave:
    def __init__(self, trigger_x, enemy_types):
        self.trigger_x = trigger_x
        self.enemy_types = enemy_types
        self.started = False
        self.completed = False

    def spawn(self):
        enemies = []
        for i, enemy_type in enumerate(self.enemy_types):
            enemy = EnemyFactory.create_enemy(enemy_type, self.trigger_x + i*80, 350)
            enemies.append(enemy)

        self.started = True
        return enemies

class BossWave:
    def __init__(self, trigger_x):
        self.trigger_x = trigger_x
        self.started = False
        self.completed = False
    def spawn(self):
        self.started = True
        return [BossEnemy(self.trigger_x, 320)]
