class EnemyReactionMixin:
    def die(self):
        self.hp = 0
        self.state = self.DEAD
        self.death_timer = 30
        self.death_timer_started = False

    def take_damage(self, damage, attacker_x):
        if self.state == self.DEAD:
            return

        died = self.health.take_damage(damage)
        self.hit_timer = self.hit_stun_duration
        self.state = self.HIT

        if attacker_x < self.x:
            self.knockback_velocity = 10
        else:
            self.knockback_velocity = -10

        if self.hp > 0 and self.should_knockdown_from_damage(damage):
            self.knockdown()
            return

        if died:
            self.die()

    def apply_knockback(self):
        if self.knockback_velocity == 0:
            return

        self.x += self.knockback_velocity
        self.knockback_velocity *= 0.8
        if abs(self.knockback_velocity) < 0.5:
            self.knockback_velocity = 0

    def should_knockdown_from_damage(self, damage):
        return damage >= 40

    def knockdown(self):
        if self.state == self.DEAD:
            return

        self.state = self.KNOCKDOWN
        self.knockdown_timer = 60
        self.knockback_velocity = 0

    def grabbed_by_player(self):
        if self.state == self.DEAD:
            return

        self.state = self.GRABBED
        self.knockback_velocity = 0
        self.hit_timer = 0

    def thrown_by_player(self, direction):
        if self.state == self.DEAD:
            return

        self.state = self.THROWN
        self.facing_right = direction > 0
        self.thrown_velocity_x = 14 * direction
        self.thrown_timer = 30
        self.thrown_hit_targets.clear()
        self.take_thrown_damage(self.thrown_damage)

    def take_grab_knee_damage(self, damage):
        if self.state == self.DEAD:
            return

        died = self.health.take_damage(damage)
        if died:
            self.die()
            return

        self.state = self.GRABBED

    def take_thrown_damage(self, damage):
        if self.state == self.DEAD:
            return

        died = self.health.take_damage(damage)
        if died:
            self.die()
