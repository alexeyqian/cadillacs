from game.entities.basic_melee_enemy import BasicMeleeEnemy


class WeaponEnemy(BasicMeleeEnemy):
    def __init__(self, x, y, enemy_type="blade"):
        super().__init__(x, y, enemy_type)
