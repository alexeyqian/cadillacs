from game.components.character_health import CharacterHealth


class PlayerHealth(CharacterHealth):
    def __init__(self, max_hp, lives):
        super().__init__(max_hp)
        self.lives = lives
        self.respawn_remaining = 0

    def take_damage(self, damage):
        self.apply_damage(damage)
        if self.is_dead():
            return self.lose_life()

        return False

    def lose_life(self):
        self.lives -= 1
        self.respawn_remaining = 90
        return True

    def advance_timers(self):
        self._advance_respawn_timer()

    def is_respawn_ready(self):
        return self.lives > 0 and self.respawn_remaining <= 0

    def _advance_respawn_timer(self):
        if self.lives > 0 and self.respawn_remaining > 0:
            self.respawn_remaining -= 1

    def reset_for_respawn(self):
        self.hp = self.max_hp
        self.respawn_remaining = 0
