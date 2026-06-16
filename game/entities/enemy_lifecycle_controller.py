class EnemyLifecycleController:
    def update_special_states(self, owner):
        if owner.state == owner.DEAD:
            self.update_dead_state(owner)
            return True

        # give enemies their own clash recovery timer,
        if self.get_action_lock_remaining(owner) > 0:
            self.set_action_lock_remaining(
                owner,
                self.get_action_lock_remaining(owner) - 1,
            )
            owner.state = owner.RECOIL
            owner.update_animation()
            return True
        
        if owner.state == owner.GRABBED:
            owner.update_animation()
            return True

        if owner.state == owner.THROWN:
            self.update_thrown_state(owner)
            return True

        if owner.state == owner.KNOCKDOWN:
            self.update_knockdown_state(owner)
            return True

        if owner.state == owner.GETUP:
            self.update_getup_state(owner)
            return True

        return False

    def update_thrown_state(self, owner):
        thrown_velocity_x = self.get_thrown_velocity_x(owner)
        if thrown_velocity_x > 0:
            owner.facing_right = True
        elif thrown_velocity_x < 0:
            owner.facing_right = False

        owner.x += thrown_velocity_x
        self.set_thrown_velocity_x(owner, thrown_velocity_x * 0.9)
        self.set_thrown_remaining(owner, self.get_thrown_remaining(owner) - 1)

        if self.get_thrown_remaining(owner) <= 0 or abs(self.get_thrown_velocity_x(owner)) < 1:
            owner.state = owner.KNOCKDOWN
            self.set_knockdown_remaining(owner, 60)
            self.set_thrown_velocity_x(owner, 0)

        owner.update_animation()

    def update_knockdown_state(self, owner):
        self.set_knockdown_remaining(owner, self.get_knockdown_remaining(owner) - 1)

        if self.get_knockdown_remaining(owner) <= 0:
            owner.state = owner.GETUP
            self.set_getup_remaining(owner, 20)

        owner.update_animation()

    def update_getup_state(self, owner):
        self.set_getup_remaining(owner, self.get_getup_remaining(owner) - 1)

        if self.get_getup_remaining(owner) <= 0:
            owner.state = owner.IDLE

        owner.update_animation()

    def update_hit_state(self, owner):
        if self.get_hit_stun_remaining(owner) <= 0:
            return False

        self.set_hit_stun_remaining(owner, self.get_hit_stun_remaining(owner) - 1)
        owner.reactions.apply_knockback(owner)

        if self.get_hit_stun_remaining(owner) <= 0:
            owner.state = owner.IDLE
        else:
            owner.state = owner.HIT

        owner.update_animation()

        return True

    def update_dead_state(self, owner):
        if not self.get_death_countdown_started(owner):
            self.set_death_countdown_started(owner, True)

        if self.get_death_remaining(owner) > 0:
            self.set_death_remaining(owner, self.get_death_remaining(owner) - 1)

        owner.update_animation()

    def update_timers(self, owner):
        if hasattr(owner, "attack_state"):
            owner.attack_state.update_timers()
        elif owner.attack_cooldown > 0:
            owner.attack_cooldown -= 1
        self.update_anti_stunlock_timers(owner)
        owner.flanking.update_timers()

    def update_anti_stunlock_timers(self, owner):
        # Recent-hit tracking decays over time. If the player stops pressure,
        # the enemy becomes fully stunnable again instead of staying armored.
        if self.get_recent_hit_timer(owner) > 0:
            self.set_recent_hit_timer(owner, self.get_recent_hit_timer(owner) - 1)
        else:
            self.set_recent_hit_count(owner, 0)

        if self.get_stun_resistance_remaining(owner) > 0:
            self.set_stun_resistance_remaining(
                owner,
                self.get_stun_resistance_remaining(owner) - 1,
            )

    def is_ready_to_remove(self, owner):
        return owner.state == owner.DEAD and self.get_death_remaining(owner) <= 0

    def get_lifecycle_state(self, owner):
        return getattr(owner, "lifecycle_state", None)

    def get_death_remaining(self, owner):
        state = self.get_lifecycle_state(owner)
        return state.death_remaining if state else owner.death_remaining

    def set_death_remaining(self, owner, value):
        state = self.get_lifecycle_state(owner)
        if state:
            state.death_remaining = value
        else:
            owner.death_remaining = value

    def get_death_countdown_started(self, owner):
        state = self.get_lifecycle_state(owner)
        return state.death_countdown_started if state else owner.death_countdown_started

    def set_death_countdown_started(self, owner, value):
        state = self.get_lifecycle_state(owner)
        if state:
            state.death_countdown_started = value
        else:
            owner.death_countdown_started = value

    def get_action_lock_remaining(self, owner):
        state = self.get_lifecycle_state(owner)
        return state.action_lock_remaining if state else owner.action_lock_remaining

    def set_action_lock_remaining(self, owner, value):
        state = self.get_lifecycle_state(owner)
        if state:
            state.action_lock_remaining = value
        else:
            owner.action_lock_remaining = value

    def get_thrown_velocity_x(self, owner):
        state = self.get_lifecycle_state(owner)
        return state.thrown_velocity_x if state else owner.thrown_velocity_x

    def set_thrown_velocity_x(self, owner, value):
        state = self.get_lifecycle_state(owner)
        if state:
            state.thrown_velocity_x = value
        else:
            owner.thrown_velocity_x = value

    def get_thrown_remaining(self, owner):
        state = self.get_lifecycle_state(owner)
        return state.thrown_remaining if state else owner.thrown_remaining

    def set_thrown_remaining(self, owner, value):
        state = self.get_lifecycle_state(owner)
        if state:
            state.thrown_remaining = value
        else:
            owner.thrown_remaining = value

    def get_knockdown_remaining(self, owner):
        state = self.get_lifecycle_state(owner)
        return state.knockdown_remaining if state else owner.knockdown_remaining

    def set_knockdown_remaining(self, owner, value):
        state = self.get_lifecycle_state(owner)
        if state:
            state.knockdown_remaining = value
        else:
            owner.knockdown_remaining = value

    def get_getup_remaining(self, owner):
        state = self.get_lifecycle_state(owner)
        return state.getup_remaining if state else owner.getup_remaining

    def set_getup_remaining(self, owner, value):
        state = self.get_lifecycle_state(owner)
        if state:
            state.getup_remaining = value
        else:
            owner.getup_remaining = value

    def get_hit_stun_remaining(self, owner):
        state = self.get_lifecycle_state(owner)
        return state.hit_stun_remaining if state else owner.hit_stun_remaining

    def set_hit_stun_remaining(self, owner, value):
        state = self.get_lifecycle_state(owner)
        if state:
            state.hit_stun_remaining = value
        else:
            owner.hit_stun_remaining = value

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
