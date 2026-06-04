from game.entities.enemy import Enemy

class FastEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)

        self.max_hp = 60
        self.hp = self.max_hp
        self.speed = 4
        self.attack_damage = 8
