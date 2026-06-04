from game.entities.enemy import Enemy
from game.entities.boss_enemy import BossEnemy
from game.entities.enemy_factory import EnemyFactory

class Wave:
    def __init__(self, trigger_x, enemy_types):
        self.trigger_x = trigger_x
        self.enemy_types = enemy_types
        self.started = False
        self.completed = False
        # Enemy enters after delay, one by one
        # instead of appear instantly together
        self.pending_enemies = []
        self.spawn_timer = 0
        self.spawn_interval = 90

    def spawn(self):
        self.started = True
        # reset spawn timer so first enemy can appear immediately
        self.spawn_timer = 0
        self.pending_enemies = []
        for i, enemy_type in enumerate(self.enemy_types):
            # store as tuples (type, x, y)
            self.pending_enemies.append((enemy_type, self.trigger_x + i*80, 350))

        return []
    
    def update_spawn(self):
        if len(self.pending_enemies) == 0:
            return []
        if self.spawn_timer > 0:
            self.spawn_timer -= 1
            return []
        
        enemy_type, x, y = self.pending_enemies.pop(0)
        # todo: add spawn_side, so enemy can spawn left, right
        enemy = EnemyFactory.create_enemy(enemy_type, x, y)
        self.spawn_timer = self.spawn_interval
        return [enemy]

class BossWave:
    def __init__(self, trigger_x):
        self.trigger_x = trigger_x
        self.started = False
        self.completed = False
    def spawn(self):
        self.started = True
        return [BossEnemy(self.trigger_x, 320)]
