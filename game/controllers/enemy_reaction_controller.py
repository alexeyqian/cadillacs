from game.combat.hit_reaction import HitReaction


class EnemyReactionController:
    def __init__(self):
        self.flinch_damage_threshold = 0
        self.attack_flinch_damage_threshold = 0
        self.knockdown_damage_threshold = 40

    # --- Public API ---

    def is_reaction_blocked(self, owner):
        """Pure read — returns True if the enemy is currently locked in a reaction."""
        return owner.condition.has_hit_stun()

    def update_reactions(self, owner):
        if self._tick_hit_stun(owner):
            return True
        self._apply_knockback(owner)
        return False

    def take_damage(self, owner, damage, attacker_x, reaction=None):
        if owner.state == owner.DEAD:
            return
        if reaction is None:
            reaction = HitReaction()

        owner.health.take_damage(damage)

        if owner.health.hp > 0 and damage >= self.knockdown_damage_threshold:
            self._knockdown(owner)
            return

        if owner.health.is_dead():
            self._die(owner)
            return

        if damage >= self._flinch_threshold(owner):
            self._apply_flinch(owner, attacker_x, reaction)

    def grabbed_by_player(self, owner):
        if owner.state == owner.DEAD:
            return
        self._clear_combat_commitment(owner)
        owner.state = owner.GRABBED
        owner.condition.clear_knockback()
        owner.condition.clear_hit_stun()

    def thrown_by_player(self, owner, direction, damage):
        if owner.state == owner.DEAD:
            return
        self._clear_combat_commitment(owner)
        owner.state = owner.THROWN
        owner.facing_right = direction > 0
        owner.condition.start_thrown(direction, damage)
        owner.health.take_damage(damage)
        if owner.health.is_dead():
            self._die(owner)

    def take_grab_knee_damage(self, owner, damage):
        if owner.state == owner.DEAD:
            return
        self._clear_combat_commitment(owner)
        owner.health.take_damage(damage)
        if owner.health.is_dead():
            self._die(owner)
            return
        owner.state = owner.GRABBED

    # --- Private helpers ---

    def _die(self, owner):
        self._clear_combat_commitment(owner)
        owner.health.hp = 0
        owner.state = owner.DEAD
        owner.condition.start_death_countdown(30)

    def _knockdown(self, owner):
        self._clear_combat_commitment(owner)
        owner.state = owner.KNOCKDOWN
        owner.condition.start_knockdown(60)
        owner.condition.clear_knockback()

    def _apply_flinch(self, owner, attacker_x, reaction):
        stun_frames = reaction.stun_frames
        if stun_frames is None:
            stun_frames = owner.combat_controller.get_attack_data(owner).hit_stun_duration
        owner.condition.set_hit_stun(stun_frames)
        owner.state = owner.HIT
        self._clear_combat_commitment(owner)

        knockback = reaction.knockback_velocity
        owner.condition.set_knockback(knockback if attacker_x < owner.x else -knockback)

    def _tick_hit_stun(self, owner):
        if not owner.condition.has_hit_stun():
            return False
        owner.condition.tick_hit_stun()
        self._apply_knockback(owner)
        owner.state = owner.HIT if owner.condition.has_hit_stun() else owner.IDLE
        return True

    def _apply_knockback(self, owner):
        owner.condition.apply_knockback(owner)

    def _flinch_threshold(self, owner):
        if owner.state == owner.ATTACK:
            return self.attack_flinch_damage_threshold
        return self.flinch_damage_threshold

    def _clear_combat_commitment(self, owner):
        owner.combat_controller.cancel_attack_timing(owner)
        owner.ai_controller.reset_decision_timer()
        owner.combat_controller.release_attack_slot(owner)
