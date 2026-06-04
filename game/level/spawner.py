from game.entities.enemy_factory import EnemyFactory

class EnemySpawner:
    def __init__(self, spawn_x, spawn_y, enemy_type, total_count, spawn_delay):
        self.spawn_x = spawn_x
        self.spawn_y = spawn_y

        self.enemy_type = enemy_type

        self.total_count = total_count
        self.spawn_delay = spawn_delay

        self.spawned_count = 0
        self.timer = 0

    def update(self):
        if self.spawned_count >= self.total_count:
            return None

        self.timer += 1
        if self.timer < self.spawn_delay:
            return None

        self.timer = 0
        self.spawned_count += 1
        enemy = EnemyFactory.create_enemy(self.enemy_type, 
                        self.spawn_x, self.spawn_y)
        
        return enemy

    def finished(self):
        return self.spawned_count >= self.total_count

