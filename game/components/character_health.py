class CharacterHealth:
    def __init__(self, max_hp):
        self.max_hp = max_hp
        self.hp = max_hp

    def apply_damage(self, damage):
        self.hp = max(0, self.hp - damage)

    def is_dead(self):
        return self.hp <= 0
