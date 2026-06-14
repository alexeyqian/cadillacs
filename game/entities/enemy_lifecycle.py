class EnemyLifecycleMixin:
    def update_special_states(self):
        if self.state == self.GRABBED:
            self.update_animation()
            return True
        if self.state == self.THROWN:
            self.update_thrown_state()
            return True
        if self.state == self.KNOCKDOWN:
            self.update_knockdown_state()
            return True
        if self.state == self.GETUP:
            self.update_getup_state()
            return True
        if self.state == self.DEAD:
            self.update_dead_state()
            return True

        return False

    def update_thrown_state(self):
        if self.thrown_velocity_x > 0:
            self.facing_right = True
        elif self.thrown_velocity_x < 0:
            self.facing_right = False

        self.x += self.thrown_velocity_x
        self.thrown_velocity_x *= 0.9
        self.thrown_timer -= 1

        if self.thrown_timer <= 0 or abs(self.thrown_velocity_x) < 1:
            self.state = self.KNOCKDOWN
            self.knockdown_timer = 60
            self.thrown_velocity_x = 0

        self.update_animation()

    def update_knockdown_state(self):
        self.knockdown_timer -= 1
        if self.knockdown_timer <= 0:
            self.state = self.GETUP
            self.getup_timer = 20
        self.update_animation()

    def update_getup_state(self):
        self.getup_timer -= 1
        if self.getup_timer <= 0:
            self.state = self.IDLE
        self.update_animation()

    def update_hit_state(self):
        if self.hit_timer <= 0:
            return False

        self.hit_timer -= 1
        self.apply_knockback()
        if self.hit_timer <= 0:
            self.state = self.IDLE
        else:
            self.state = self.HIT
        self.update_animation()

        return True

    def update_dead_state(self):
        if not self.death_timer_started:
            self.death_timer_started = True
        if self.death_timer > 0:
            self.death_timer -= 1
        self.update_animation()

    def update_timers(self):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

    def is_ready_to_remove(self):
        return self.state == self.DEAD and self.death_timer <= 0
