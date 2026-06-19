from game.entities.hit_reaction import HitReaction, normalize_hit_reaction


class EnemyReactionController:
    def die(self, owner):
        self.cancel_attack(owner)
        owner.health.hp = 0
        owner.state = owner.DEAD
        self.set_death_remaining(owner, 30)
        self.set_death_countdown_started(owner, False)
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
                stun_frames = owner.combat.get_attack_data(owner).hit_stun_duration
            self.set_hit_stun_remaining(owner, stun_frames)
            owner.state = owner.HIT
            # So if an enemy is interrupted, it releases the slot.
            self.cancel_attack(owner)
            self.release_attack_slot(owner)

            if attacker_x < owner.x:
                self.set_knockback_velocity(owner, reaction.knockback_velocity)
            else:
                self.set_knockback_velocity(owner, -reaction.knockback_velocity)
            return

    def apply_knockback(self, owner):
        knockback_velocity = self.get_knockback_velocity(owner)
        if knockback_velocity == 0:
            return

        owner.x += knockback_velocity
        self.set_knockback_velocity(owner, knockback_velocity * 0.8)

        if abs(self.get_knockback_velocity(owner)) < 0.5:
            self.set_knockback_velocity(owner, 0)

    def should_knockdown_from_damage(self, damage):
        return damage >= 40

    def get_flinch_threshold(self, owner):
        if owner.state == owner.ATTACK:
            return getattr(
                owner,
                "attack_flinch_damage_threshold",
                getattr(owner, "flinch_damage_threshold", 0),
            )

        return getattr(owner, "flinch_damage_threshold", 0)

    def knockdown(self, owner):
        if owner.state == owner.DEAD:
            return

        self.reset_attack_decision(owner)
        owner.state = owner.KNOCKDOWN
        self.set_knockdown_remaining(owner, 60)
        self.set_knockback_velocity(owner, 0)
        self.cancel_attack(owner)
        self.release_attack_slot(owner)

    def grabbed_by_player(self, owner):
        if owner.state == owner.DEAD:
            return

        self.reset_attack_decision(owner)
        owner.state = owner.GRABBED
        self.set_knockback_velocity(owner, 0)
        self.set_hit_stun_remaining(owner, 0)
        self.cancel_attack(owner)
        self.release_attack_slot(owner)

    def thrown_by_player(self, owner, direction, damage):
        if owner.state == owner.DEAD:
            return

        self.reset_attack_decision(owner)
        owner.state = owner.THROWN
        owner.facing_right = direction > 0
        self.set_thrown_velocity_x(owner, 14 * direction)
        self.set_thrown_remaining(owner, 30)
        self.set_throw_damage(owner, damage)
        self.get_thrown_hit_targets(owner).clear()
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
        if hasattr(owner, "combat"):
            owner.combat.cancel_attack_timing(owner)
        elif hasattr(owner, "attack_manager"):
            owner.attack_manager.cancel()
            owner.attack_timer = 0
        else:
            owner.attack_timer = 0

    def reset_attack_decision(self, owner):
        if hasattr(owner, "combat"):
            owner.combat.reset_decision_timer(owner)
        else:
            owner.attack_decision_timer = 0

    def release_attack_slot(self, owner):
        if hasattr(owner, "combat"):
            owner.combat.release_attack_slot(owner)
        else:
            owner.has_attack_slot = False

    def get_lifecycle_state(self, owner):
        return getattr(owner, "lifecycle_state", None)

    def get_knockback_velocity(self, owner):
        state = self.get_lifecycle_state(owner)
        return state.knockback_velocity if state else owner.knockback_velocity

    def set_knockback_velocity(self, owner, value):
        state = self.get_lifecycle_state(owner)
        if state:
            state.knockback_velocity = value
        else:
            owner.knockback_velocity = value

    def set_hit_stun_remaining(self, owner, value):
        state = self.get_lifecycle_state(owner)
        if state:
            state.hit_stun_remaining = value
        else:
            owner.hit_stun_remaining = value

    def get_hit_stun_remaining(self, owner):
        state = self.get_lifecycle_state(owner)
        return state.hit_stun_remaining if state else owner.hit_stun_remaining

    def set_death_remaining(self, owner, value):
        state = self.get_lifecycle_state(owner)
        if state:
            state.death_remaining = value
        else:
            owner.death_remaining = value

    def set_death_countdown_started(self, owner, value):
        state = self.get_lifecycle_state(owner)
        if state:
            state.death_countdown_started = value
        else:
            owner.death_countdown_started = value

    def set_knockdown_remaining(self, owner, value):
        state = self.get_lifecycle_state(owner)
        if state:
            state.knockdown_remaining = value
        else:
            owner.knockdown_remaining = value

    def set_thrown_velocity_x(self, owner, value):
        state = self.get_lifecycle_state(owner)
        if state:
            state.thrown_velocity_x = value
        else:
            owner.thrown_velocity_x = value

    def set_thrown_remaining(self, owner, value):
        state = self.get_lifecycle_state(owner)
        if state:
            state.thrown_remaining = value
        else:
            owner.thrown_remaining = value

    def get_throw_damage(self, owner):
        state = self.get_lifecycle_state(owner)
        return state.throw_damage if state else getattr(owner, "throw_damage", 0)

    def set_throw_damage(self, owner, value):
        state = self.get_lifecycle_state(owner)
        if state:
            state.throw_damage = value
        else:
            owner.throw_damage = value

    def get_thrown_hit_targets(self, owner):
        state = self.get_lifecycle_state(owner)
        return state.thrown_hit_targets if state else owner.thrown_hit_targets

    def set_action_lock_remaining(self, owner, value):
        state = self.get_lifecycle_state(owner)
        if state:
            state.action_lock_remaining = value
        else:
            owner.action_lock_remaining = value
