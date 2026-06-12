from game.entities.basic_melee_enemy import BasicMeleeEnemy


class HeavyEnemy(BasicMeleeEnemy):
    def __init__(self, x, y, enemy_type="heavy"):
        super().__init__(x, y, enemy_type)

        self.attack_windup = 26
        self.attack_active = 10
        self.attack_recovery = 34
        self.attack_total_duration = (
            self.attack_windup + self.attack_active + self.attack_recovery
        )

    def should_knockdown_from_damage(self, damage):
        return damage >= 55
