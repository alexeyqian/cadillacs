from game.components.character_health import CharacterHealth


class EnemyHealth(CharacterHealth):
    def __init__(self, max_hp):
        super().__init__(max_hp)

    def take_damage(self, damage):
        return self.apply_damage(damage)

    def is_dead(self):
        return self.is_depleted()
