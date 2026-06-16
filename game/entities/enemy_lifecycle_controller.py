class EnemyLifecycleController:
    def update_special_states(self, owner):
        if owner.state == owner.DEAD:
            self.update_dead_state(owner)
            return True

        # give enemies their own clash recovery timer,
        if owner.action_lock_remaining > 0:
            owner.action_lock_remaining -= 1
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
        if owner.thrown_velocity_x > 0:
            owner.facing_right = True
        elif owner.thrown_velocity_x < 0:
            owner.facing_right = False

        owner.x += owner.thrown_velocity_x
        owner.thrown_velocity_x *= 0.9
        owner.thrown_remaining -= 1

        if owner.thrown_remaining <= 0 or abs(owner.thrown_velocity_x) < 1:
            owner.state = owner.KNOCKDOWN
            owner.knockdown_remaining = 60
            owner.thrown_velocity_x = 0

        owner.update_animation()

    def update_knockdown_state(self, owner):
        owner.knockdown_remaining -= 1

        if owner.knockdown_remaining <= 0:
            owner.state = owner.GETUP
            owner.getup_remaining = 20

        owner.update_animation()

    def update_getup_state(self, owner):
        owner.getup_remaining -= 1

        if owner.getup_remaining <= 0:
            owner.state = owner.IDLE

        owner.update_animation()

    def update_hit_state(self, owner):
        if owner.hit_stun_remaining <= 0:
            return False

        owner.hit_stun_remaining -= 1
        owner.reactions.apply_knockback(owner)

        if owner.hit_stun_remaining <= 0:
            owner.state = owner.IDLE
        else:
            owner.state = owner.HIT

        owner.update_animation()

        return True

    def update_dead_state(self, owner):
        if not owner.death_countdown_started:
            owner.death_countdown_started = True

        if owner.death_remaining > 0:
            owner.death_remaining -= 1

        owner.update_animation()

    def update_timers(self, owner):
        if hasattr(owner, "attack_state"):
            owner.attack_state.update_timers()
        elif owner.attack_cooldown > 0:
            owner.attack_cooldown -= 1
        owner.flanking.update_timers()

    def is_ready_to_remove(self, owner):
        return owner.state == owner.DEAD and owner.death_remaining <= 0
