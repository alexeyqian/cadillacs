from game.entities.enemy import Enemy

class HeavyEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)

        self.max_hp = 250
        self.hp = self.max_hp
        self.speed = 1
        self.attack_damage = 25
        self.width = 70
        self.height = 100
        self.detect_range = 180