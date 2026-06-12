from game.entities.basic_melee_enemy import BasicMeleeEnemy


class FastSmallEnemy(BasicMeleeEnemy):
    def __init__(self, x, y, enemy_type="fast"):
        super().__init__(x, y, enemy_type)

        self.attack_windup = 14
        self.attack_active = 8
        self.attack_recovery = 20
        self.attack_total_duration = (
            self.attack_windup + self.attack_active + self.attack_recovery
        )


class FastEnemy(FastSmallEnemy):
    def __init__(self, x, y):
        super().__init__(x, y, "fast")
