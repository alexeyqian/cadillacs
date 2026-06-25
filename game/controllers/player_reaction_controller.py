from game.combat.hit_reaction import HitReaction


class PlayerReactionController:
    def __init__(self, default_stun_frames):
        self.default_stun_frames = default_stun_frames
        self._hit_stun_remaining = 0

    # --- Public API ---

    def is_in_hit_stun(self):
        return self._hit_stun_remaining > 0

    def take_damage(self, owner, damage, reaction=None):
        if owner.state == owner.DEAD:
            return
        self._cancel_combat_commitment(owner)
        owner.health.take_damage(damage)
        owner.state_machine.change_to(owner, owner.HIT)
        if owner.health.is_dead():
            owner.lifecycle_controller.lose_life()
            owner.lifecycle_controller.enter_dead_state(owner)
            return
        self._start_hit_stun(reaction)

    def update_hit_state(self, owner):
        if not self.is_in_hit_stun():
            return
        self._tick()
        if self.is_in_hit_stun():
            owner.state_machine.change_to(owner, owner.HIT)
        else:
            owner.state_machine.change_to(owner, owner.IDLE)

    def reset(self):
        self._hit_stun_remaining = 0

    # --- Private helpers ---

    def _start_hit_stun(self, reaction=None):
        if isinstance(reaction, HitReaction) and reaction.stun_frames is not None:
            self._hit_stun_remaining = reaction.stun_frames
        else:
            self._hit_stun_remaining = self.default_stun_frames

    def _tick(self):
        if self._hit_stun_remaining > 0:
            self._hit_stun_remaining -= 1

    def _cancel_combat_commitment(self, owner):
        # Enemy lands hit -> player attack is canceled
        # Enemy lands hit -> combo step resets
        # Enemy lands hit -> grabbed enemy is released
        # Player must restart pressure after recovering
        owner.combat_controller.cancel_attack()
        owner.movement.cancel_run_attack_momentum()
        owner.movement.cancel_combo_finisher_nudge()
        owner.grab_controller.grabbed_enemy = None
