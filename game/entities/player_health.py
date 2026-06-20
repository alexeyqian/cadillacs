from game.components.character_health import CharacterHealth
from game.combat.hit_reaction import HitReaction


class PlayerHealth(CharacterHealth):
    def __init__(self, max_hp, lives, hit_stun_duration):
        super().__init__(max_hp)
        self.lives = lives
        self.hit_stun_duration = hit_stun_duration
        self.hit_stun_remaining = 0
        self.respawn_remaining = 0

    def take_damage(self, damage, reaction=None):
        self.hit_stun_remaining = self.get_hit_stun_frames(reaction)

        self.apply_damage(damage)
        if self.is_dead():
            return self.lose_life()

        return False

    def get_hit_stun_frames(self, reaction=None):
        if isinstance(reaction, HitReaction) and reaction.stun_frames is not None:
            return reaction.stun_frames

        return self.hit_stun_duration

    def lose_life(self):
        self.lives -= 1
        self.respawn_remaining = 90
        return True

    def advance_timers(self):
        self._advance_hit_stun_timer()
        self._advance_respawn_timer()

    def is_in_hit_stun(self):
        return self.hit_stun_remaining > 0

    def is_respawn_ready(self):
        return self.lives > 0 and self.respawn_remaining <= 0

    def _advance_hit_stun_timer(self):
        if self.hit_stun_remaining > 0:
            self.hit_stun_remaining -= 1

    def _advance_respawn_timer(self):
        if self.lives > 0 and self.respawn_remaining > 0:
            self.respawn_remaining -= 1

    def reset_for_respawn(self):
        self.hp = self.max_hp
        self.hit_stun_remaining = 0
        self.respawn_remaining = 0
