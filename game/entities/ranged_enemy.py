from game.entities.enemy import Enemy


class RangedEnemy(Enemy):

    def __init__(self, x, y):
        super().__init__(x, y)

        self.max_hp = 80
        self.hp = self.max_hp

        self.attack_damage = 12

        self.attack_range = 250