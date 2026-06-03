from game.entities.enemy import Enemy

class Wave:
    def __init__(self, trigger_x, enemy_positions):
        self.trigger_x = trigger_x
        self.enemy_positions = enemy_positions
        self.started = False
        self.completed = False

    def spawn(self):
        enemies = []
        for x, y in self.enemy_positions:
            enemies.append(Enemy(x,y))

        self.started = True
        return enemies

