from game.combat.hit_reaction import HitReaction


class EnemyReactionController:
    def __init__(self):
        self.flinch_damage_threshold = 0
        self.attack_flinch_damage_threshold = 0
        self.knockdown_damage_threshold = 40

    def die(self, owner):
        self._clear_combat_commitment(owner)
        owner.health.hp = 0
        owner.state = owner.DEAD
        owner.condition.start_death_countdown(30)

    def take_damage(
        self,
        owner,
        damage,
        attacker_x,
        reaction=None,
    ):
        if reaction is None:
            reaction = HitReaction()
        self.apply_hit(owner, damage, attacker_x, reaction)

    def apply_hit(
        self,
        owner,
        damage,
        attacker_x,
        reaction=None,
    ):
        if reaction is None:
            reaction = HitReaction()

        if owner.state == owner.DEAD:
            return

        owner.health.take_damage(damage)

        if owner.health.hp > 0 and self.should_knockdown_from_damage(damage):
            self.knockdown(owner)
            return

        if owner.health.is_dead():
            self.die(owner)
            return

        if damage >= self.get_flinch_threshold(owner):
            self.apply_flinch(owner, attacker_x, reaction)

    def is_reaction_blocked(self, owner):
        """Pure read — returns True if the enemy is currently locked in a reaction."""
        return owner.condition.has_hit_stun()

    def update_reactions(self, owner):
        if self._update_hit_state(owner):
            return True

        self.apply_knockback(owner)
        return False

    def _update_hit_state(self, owner):
        if not owner.condition.has_hit_stun():
            return False

        owner.condition.tick_hit_stun()
        self.apply_knockback(owner)

        if owner.condition.has_hit_stun():
            owner.state = owner.HIT
        else:
            owner.state = owner.IDLE

        return True

    def apply_flinch(self, owner, attacker_x, reaction):
        stun_frames = reaction.stun_frames
        if stun_frames is None:
            stun_frames = owner.combat_controller.get_attack_data(owner).hit_stun_duration
        owner.condition.set_hit_stun(stun_frames)
        owner.state = owner.HIT
        # So if an enemy is interrupted, it releases the slot.
        self._clear_combat_commitment(owner)

        if attacker_x < owner.x:
            owner.condition.set_knockback(reaction.knockback_velocity)
        else:
            owner.condition.set_knockback(-reaction.knockback_velocity)

    def apply_knockback(self, owner):
        owner.condition.apply_knockback(owner)

    def should_knockdown_from_damage(self, damage):
        return damage >= self.knockdown_damage_threshold

    def get_flinch_threshold(self, owner):
        if owner.state == owner.ATTACK:
            return self.attack_flinch_damage_threshold
        return self.flinch_damage_threshold

    def knockdown(self, owner):
        if owner.state == owner.DEAD:
            return

        self._clear_combat_commitment(owner)
        owner.state = owner.KNOCKDOWN
        owner.condition.start_knockdown(60)
        owner.condition.clear_knockback()

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
        self.take_throw_damage(owner, damage)

    def take_grab_knee_damage(self, owner, damage):
        if owner.state == owner.DEAD:
            return

        self._clear_combat_commitment(owner)
        owner.health.take_damage(damage)

        if owner.health.is_dead():
            self.die(owner)
            return

        owner.state = owner.GRABBED

    def take_throw_damage(self, owner, damage):
        if owner.state == owner.DEAD:
            return
        self._clear_combat_commitment(owner)

        owner.health.take_damage(damage)

        if owner.health.is_dead():
            self.die(owner)

    def _clear_combat_commitment(self, owner):
        self._cancel_attack(owner)
        self._reset_attack_decision(owner)
        self._release_attack_slot(owner)

    def _cancel_attack(self, owner):
        owner.combat_controller.cancel_attack_timing(owner)

    def _reset_attack_decision(self, owner):
        owner.ai_controller.reset_decision_timer()

    def _release_attack_slot(self, owner):
        owner.combat_controller.release_attack_slot(owner)
