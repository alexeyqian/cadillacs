from game.entities.basic_melee_enemy import BasicMeleeEnemy


class WeaponEnemy(BasicMeleeEnemy):
    def __init__(self, x, y, enemy_type="blade"):
        super().__init__(x, y, enemy_type)

        # Weapon enemies should threaten farther than bare-handed thugs,
        # but they still use the same readable attack timing model.
        self.attack_windup = 18
        self.attack_active = 10
        self.attack_recovery = 28
        self.attack_total_duration = (
            self.attack_windup + self.attack_active + self.attack_recovery
        )
