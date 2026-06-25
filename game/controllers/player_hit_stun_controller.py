from game.combat.hit_reaction import HitReaction


class PlayerHitStunController:
    def __init__(self, default_stun_frames):
        self.default_stun_frames = default_stun_frames
        self.hit_stun_remaining = 0

    def start_hit_stun(self, reaction=None):
        self.hit_stun_remaining = self.get_hit_stun_frames(reaction)

    def update_hit_state(self, owner):
        if not self.is_in_hit_stun():
            return

        self.advance_timers()
        if self.is_in_hit_stun():
            owner.state_machine.change_to(owner, owner.HIT)
        else:
            owner.state_machine.change_to(owner, owner.IDLE)

    def advance_timers(self):
        if self.hit_stun_remaining > 0:
            self.hit_stun_remaining -= 1

    def is_in_hit_stun(self):
        return self.hit_stun_remaining > 0

    def reset(self):
        self.hit_stun_remaining = 0

    def get_hit_stun_frames(self, reaction=None):
        if isinstance(reaction, HitReaction) and reaction.stun_frames is not None:
            return reaction.stun_frames

        return self.default_stun_frames
