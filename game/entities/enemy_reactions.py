class EnemyReactionMixin:
    def die(self):
        self.reactions.die(self)

    def take_damage(self, damage, attacker_x):
        self.reactions.take_damage(self, damage, attacker_x)

    def apply_knockback(self):
        self.reactions.apply_knockback(self)

    def should_knockdown_from_damage(self, damage):
        return self.reactions.should_knockdown_from_damage(damage)

    def knockdown(self):
        self.reactions.knockdown(self)

    def grabbed_by_player(self):
        self.reactions.grabbed_by_player(self)

    def thrown_by_player(self, direction):
        self.reactions.thrown_by_player(self, direction)

    def take_grab_knee_damage(self, damage):
        self.reactions.take_grab_knee_damage(self, damage)

    def take_thrown_damage(self, damage):
        self.reactions.take_thrown_damage(self, damage)