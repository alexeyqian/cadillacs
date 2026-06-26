from game.combat.hit_reaction import HitReaction


class PlayerReactionController:
    def __init__(self):
        pass

    # --- Public API ---

    def is_in_hit_stun(self, owner):
        return owner.reaction_state._hit_stun_remaining > 0

    def take_damage(self, owner, damage, reaction=None):
        if owner.state == owner.DEAD:
            return
        self._cancel_combat_commitment(owner)
        owner.health.take_damage(damage)
        owner.state_machine.change_to(owner, owner.HIT)
        if owner.health.is_dead():
            owner._on_death()
            return
        self._start_hit_stun(owner, reaction)

    def update_hit_state(self, owner):
        if not self.is_in_hit_stun(owner):
            return
        self._tick(owner)
        if self.is_in_hit_stun(owner):
            owner.state_machine.change_to(owner, owner.HIT)
        else:
            owner.state_machine.change_to(owner, owner.IDLE)

    def reset(self, owner):
        owner.reaction_state._hit_stun_remaining = 0

    # --- Private helpers ---

    def _start_hit_stun(self, owner, reaction=None):
        rs = owner.reaction_state
        if isinstance(reaction, HitReaction) and reaction.stun_frames is not None:
            rs._hit_stun_remaining = reaction.stun_frames
        else:
            rs._hit_stun_remaining = rs.default_stun_frames

    def _tick(self, owner):
        rs = owner.reaction_state
        if rs._hit_stun_remaining > 0:
            rs._hit_stun_remaining -= 1

    def _cancel_combat_commitment(self, owner):
        owner._cancel_combat_commitment()
