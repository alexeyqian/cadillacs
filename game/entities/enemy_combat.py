class EnemyCombatMixin:
    def start_attack(self):
        self.combat.start_attack(self)

    def update_attack(self, level, player):
        self.combat.update_attack(self, level, player)