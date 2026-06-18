from game.entities.hit_reaction import HitReaction


class EnemyReactionController:
    def die(self, owner):
        self.cancel_attack(owner)
        owner.health.hp = 0
        owner.state = owner.DEAD
        self.set_death_remaining(owner, 30)
        self.set_death_countdown_started(owner, False)
        self.reset_attack_decision(owner)
        self.release_attack_slot(owner)

    # temp for renaming
    def take_damage(
        self,
        owner,
        damage,
        attacker_x,
        reaction=None,
        hit_stun_duration=None,
        knockback_velocity=None,
    ):
        if knockback_velocity is not None:
            reaction = knockback_velocity
        if isinstance(reaction, (int, float)):
            reaction = HitReaction(
                knockback_velocity=reaction,
                stun_frames=hit_stun_duration,
            )
        elif reaction is None:
            reaction = HitReaction(stun_frames=hit_stun_duration)
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
        self.register_recent_hit(owner, attacker_x)

        if owner.health.hp > 0 and self.should_knockdown_from_damage(damage):
            self.knockdown(owner)
            return

        if died:
            self.die(owner)
            return

        flinch_threshold = self.get_flinch_threshold(owner)
        should_flinch = (
            damage >= flinch_threshold
            and not self.is_stun_resistant(owner)
        )

        if should_flinch:
            self.reset_attack_decision(owner)
            stun_frames = reaction.stun_frames
            if stun_frames is None:
                stun_frames = owner.hit_stun_duration
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

        if self.is_stun_resistant(owner):
            self.apply_resisted_hit(owner)

    def register_recent_hit(self, owner, attacker_x):
        hit_window = getattr(owner, "anti_stunlock_hit_window", 90)
        hit_limit = getattr(owner, "anti_stunlock_hit_limit", 3)

        # A quick-hit window is easier to reason about than permanent armor:
        # pressure builds resistance, but backing off lets the enemy reset.
        self.set_recent_hit_count(owner, self.get_recent_hit_count(owner) + 1)
        self.set_recent_hit_timer(owner, hit_window)

        if self.get_recent_hit_count(owner) >= hit_limit:
            self.set_stun_resistance_remaining(
                owner,
                getattr(owner, "stun_resistance_duration", 45),
            )
            self.start_breakout_recoil(owner, attacker_x)
            self.set_recent_hit_count(owner, 0)

    def is_stun_resistant(self, owner):
        return self.get_stun_resistance_remaining(owner) > 0

    def start_breakout_recoil(self, owner, attacker_x):
        if owner.state == owner.ATTACK:
            return

        # Breakout gives the enemy a tiny "get off me" step after repeated
        # hits. It does not damage the player; it simply creates room so the
        # enemy AI can resume instead of being held in HIT forever.
        direction = 1 if owner.x >= attacker_x else -1
        self.set_breakout_velocity_x(
            owner,
            getattr(owner, "breakout_velocity", 6) * direction,
        )
        self.set_action_lock_remaining(
            owner,
            getattr(owner, "breakout_recoil_duration", 10),
        )
        self.set_hit_stun_remaining(owner, 0)
        owner.state = owner.RECOIL

    def apply_resisted_hit(self, owner):
        resisted_stun = getattr(owner, "resisted_hit_stun_duration", 4)
        current_stun = self.get_hit_stun_remaining(owner)

        # During resistance, damage still lands, but we stop refreshing a full
        # HIT state. This is the actual anti-stunlock moment: the enemy can
        # finish the tiny reaction and return to AI instead of being pinned.
        if owner.state != owner.HIT:
            self.set_hit_stun_remaining(owner, 0)
        elif current_stun > resisted_stun:
            self.set_hit_stun_remaining(owner, resisted_stun)

        if owner.state == owner.HIT and resisted_stun <= 0:
            owner.state = owner.IDLE

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

    def thrown_by_player(self, owner, direction):
        if owner.state == owner.DEAD:
            return

        self.reset_attack_decision(owner)
        owner.state = owner.THROWN
        owner.facing_right = direction > 0
        self.set_thrown_velocity_x(owner, 14 * direction)
        self.set_thrown_remaining(owner, 30)
        self.get_thrown_hit_targets(owner).clear()
        self.cancel_attack(owner)
        self.release_attack_slot(owner)
        self.take_thrown_damage(owner, owner.thrown_damage)

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

    def take_thrown_damage(self, owner, damage):
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
        elif hasattr(owner, "attack_controller"):
            owner.attack_controller.cancel()
            owner.attack_timer = 0
        else:
            owner.attack_timer = 0

    def reset_attack_decision(self, owner):
        if hasattr(owner, "attack_state"):
            owner.attack_state.reset_decision_timer()
        else:
            owner.attack_decision_timer = 0

    def release_attack_slot(self, owner):
        if hasattr(owner, "attack_state"):
            owner.attack_state.release_slot()
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

    def get_thrown_hit_targets(self, owner):
        state = self.get_lifecycle_state(owner)
        return state.thrown_hit_targets if state else owner.thrown_hit_targets

    def get_recent_hit_count(self, owner):
        state = self.get_lifecycle_state(owner)
        return state.recent_hit_count if state else getattr(owner, "recent_hit_count", 0)

    def set_recent_hit_count(self, owner, value):
        state = self.get_lifecycle_state(owner)
        if state:
            state.recent_hit_count = value
        else:
            owner.recent_hit_count = value

    def get_recent_hit_timer(self, owner):
        state = self.get_lifecycle_state(owner)
        return state.recent_hit_timer if state else getattr(owner, "recent_hit_timer", 0)

    def set_recent_hit_timer(self, owner, value):
        state = self.get_lifecycle_state(owner)
        if state:
            state.recent_hit_timer = value
        else:
            owner.recent_hit_timer = value

    def get_stun_resistance_remaining(self, owner):
        state = self.get_lifecycle_state(owner)
        if state:
            return state.stun_resistance_remaining
        return getattr(owner, "stun_resistance_remaining", 0)

    def set_stun_resistance_remaining(self, owner, value):
        state = self.get_lifecycle_state(owner)
        if state:
            state.stun_resistance_remaining = value
        else:
            owner.stun_resistance_remaining = value

    def set_action_lock_remaining(self, owner, value):
        state = self.get_lifecycle_state(owner)
        if state:
            state.action_lock_remaining = value
        else:
            owner.action_lock_remaining = value

    def set_breakout_velocity_x(self, owner, value):
        state = self.get_lifecycle_state(owner)
        if state:
            state.breakout_velocity_x = value
        else:
            owner.breakout_velocity_x = value
