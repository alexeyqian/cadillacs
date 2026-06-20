from game.components.character_health import CharacterHealth
from game.combat.hit_reaction import HitReaction


class PlayerHealth(CharacterHealth):
    def __init__(self, max_hp, lives, hit_stun_duration):
        super().__init__(max_hp)
        self.lives = lives
        self.hit_stun_duration = hit_stun_duration
        self.hit_stun_remaining = 0
        self.respawn_remaining = 0

    # A counter-hit should feel like “you got caught during your attack,” not just ordinary damage.
    def take_damage(self, damage, reaction=None, hit_stun_bonus=0):
        # Legacy callers used the second positional argument as hit_stun_bonus.
        if isinstance(reaction, (int, float)) and hit_stun_bonus == 0:
            hit_stun_bonus = reaction
            reaction = None

        self.hit_stun_remaining = self.get_hit_stun_frames(
            reaction,
            hit_stun_bonus,
        )

        if self.apply_damage(damage):
            return self.lose_life()

        return False

    def get_hit_stun_frames(self, reaction=None, hit_stun_bonus=0):
        if isinstance(reaction, HitReaction) and reaction.stun_frames is not None:
            return reaction.stun_frames

        return self.hit_stun_duration + hit_stun_bonus

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
        self.restore_full()
        self.hit_stun_remaining = 0
        self.respawn_remaining = 0
