class EnemyHealth:
    def __init__(self, max_hp):
        self.max_hp = max_hp
        self.hp = max_hp

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
            return True

        return False

    def is_dead(self):
        return self.hp <= 0