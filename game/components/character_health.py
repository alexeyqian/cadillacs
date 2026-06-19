class CharacterHealth:
    def __init__(self, max_hp):
        self.max_hp = max_hp
        self.hp = max_hp

    def apply_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
            return True

        return False

    def restore_full(self):
        self.hp = self.max_hp

    def is_depleted(self):
        return self.hp <= 0
