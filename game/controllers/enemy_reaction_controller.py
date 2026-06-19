from game.combat.hit_reaction import HitReaction, normalize_hit_reaction


class EnemyReactionController:
    def __init__(self):
        self.flinch_damage_threshold = 0
        self.attack_flinch_damage_threshold = 0
        self.knockdown_damage_threshold = 40

    def die(self, owner):
        self.cancel_attack(owner)
        owner.health.hp = 0
        owner.state = owner.DEAD
        owner.life_cycle.start_death_countdown(30)
        self.reset_attack_decision(owner)
        self.release_attack_slot(owner)

    # Public damage entry point. It accepts the new HitReaction object and a
    # small legacy shape so older callers can migrate gradually.
    def take_damage(
        self,
        owner,
        damage,
        attacker_x,
        reaction=None,
        hit_stun_duration=None,
        knockback_velocity=None,
    ):
        reaction = normalize_hit_reaction(
            reaction,
            hit_stun_duration,
            knockback_velocity,
        )
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

        died = owner.health.take_damage(damage)

        if owner.health.hp > 0 and self.should_knockdown_from_damage(damage):
            self.knockdown(owner)
            return

        if died:
            self.die(owner)
            return

        flinch_threshold = self.get_flinch_threshold(owner)
        should_flinch = damage >= flinch_threshold

        if should_flinch:
            self.reset_attack_decision(owner)
            stun_frames = reaction.stun_frames
            if stun_frames is None:
                stun_frames = owner.combat_controller.get_attack_data(owner).hit_stun_duration
            owner.life_cycle.set_hit_stun(stun_frames)
            owner.state = owner.HIT
            # So if an enemy is interrupted, it releases the slot.
            self.cancel_attack(owner)
            self.release_attack_slot(owner)

            if attacker_x < owner.x:
                owner.life_cycle.set_knockback(reaction.knockback_velocity)
            else:
                owner.life_cycle.set_knockback(-reaction.knockback_velocity)
            return

    def apply_knockback(self, owner):
        owner.life_cycle.apply_knockback(owner)

    def should_knockdown_from_damage(self, damage):
        return damage >= self.knockdown_damage_threshold

    def get_flinch_threshold(self, owner):
        if owner.state == owner.ATTACK:
            return self.attack_flinch_damage_threshold
        return self.flinch_damage_threshold

    def knockdown(self, owner):
        if owner.state == owner.DEAD:
            return

        self.reset_attack_decision(owner)
        owner.state = owner.KNOCKDOWN
        owner.life_cycle.start_knockdown(60)
        owner.life_cycle.clear_knockback()
        self.cancel_attack(owner)
        self.release_attack_slot(owner)

    def grabbed_by_player(self, owner):
        if owner.state == owner.DEAD:
            return

        self.reset_attack_decision(owner)
        owner.state = owner.GRABBED
        owner.life_cycle.clear_knockback()
        owner.life_cycle.clear_hit_stun()
        self.cancel_attack(owner)
        self.release_attack_slot(owner)

    def thrown_by_player(self, owner, direction, damage):
        if owner.state == owner.DEAD:
            return

        self.reset_attack_decision(owner)
        owner.state = owner.THROWN
        owner.facing_right = direction > 0
        owner.life_cycle.start_thrown(direction, damage)
        self.cancel_attack(owner)
        self.release_attack_slot(owner)
        self.take_throw_damage(owner, damage)

    def take_grab_knee_damage(self, owner, damage):
        if owner.state == owner.DEAD:
            return

        self.reset_attack_decision(owner)
        died = owner.health.take_damage(damage)

        if died:
            self.die(owner)
            return

        self.cancel_attack(owner)
        self.release_attack_slot(owner)
        owner.state = owner.GRABBED

    def take_throw_damage(self, owner, damage):
        if owner.state == owner.DEAD:
            return
        self.reset_attack_decision(owner)
        self.cancel_attack(owner)
        self.release_attack_slot(owner)

        died = owner.health.take_damage(damage)

        if died:
            self.die(owner)

    def cancel_attack(self, owner):
        owner.combat_controller.cancel_attack_timing(owner)

    def reset_attack_decision(self, owner):
        owner.state_controller.reset_decision_timer()

    def release_attack_slot(self, owner):
        owner.combat_controller.release_attack_slot(owner)

    def set_action_lock_remaining(self, owner, value):
        owner.life_cycle.set_action_lock(value)
