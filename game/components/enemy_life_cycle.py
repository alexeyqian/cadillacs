class EnemyLifeCycle:
    def __init__(self):
        # Lifecycle
        self.death_remaining = 30
        self.death_countdown_started = False
        # This keeps the clash fair on both sides: the player cannot instantly re-punch,
        # and the enemy cannot instantly resume pressure either.
        self.action_lock_remaining = 0

        # Reactions
        # hit reaction # enemy gets briefly white when hit by player
        self.knockback_velocity = 0
        self.hit_stun_remaining = 0
        # grab/throw
        self.thrown_velocity_x = 0
        self.thrown_remaining = 0
        self.throw_damage = 0
        self.thrown_hit_targets = set()

        #knockdown/getup
        self.knockdown_remaining = 0
        self.getup_remaining = 0

    def start_death_countdown(self, duration=30):
        self.death_remaining = duration
        self.death_countdown_started = False

    def begin_death_countdown(self):
        self.death_countdown_started = True

    def tick_death(self):
        if self.death_remaining > 0:
            self.death_remaining -= 1

    def is_death_finished(self):
        return self.death_remaining <= 0

    def has_action_lock(self):
        return self.action_lock_remaining > 0

    def set_action_lock(self, frames):
        self.action_lock_remaining = frames

    def tick_action_lock(self):
        if self.action_lock_remaining > 0:
            self.action_lock_remaining -= 1

    def has_hit_stun(self):
        return self.hit_stun_remaining > 0

    def set_hit_stun(self, frames):
        self.hit_stun_remaining = frames

    def clear_hit_stun(self):
        self.hit_stun_remaining = 0

    def tick_hit_stun(self):
        if self.hit_stun_remaining > 0:
            self.hit_stun_remaining -= 1

    def set_knockback(self, velocity):
        self.knockback_velocity = velocity

    def clear_knockback(self):
        self.knockback_velocity = 0

    def apply_knockback(self, owner, friction=0.8, stop_threshold=0.5):
        if self.knockback_velocity == 0:
            return

        owner.x += self.knockback_velocity
        self.knockback_velocity *= friction

        if abs(self.knockback_velocity) < stop_threshold:
            self.knockback_velocity = 0

    def start_thrown(self, direction, damage, velocity=14, duration=30):
        self.thrown_velocity_x = velocity * direction
        self.thrown_remaining = duration
        self.throw_damage = damage
        self.thrown_hit_targets.clear()

    def tick_thrown(self, owner, friction=0.9, stop_threshold=1):
        if self.thrown_velocity_x > 0:
            owner.facing_right = True
        elif self.thrown_velocity_x < 0:
            owner.facing_right = False

        owner.x += self.thrown_velocity_x
        self.thrown_velocity_x *= friction
        self.thrown_remaining -= 1

        return self.thrown_remaining <= 0 or abs(self.thrown_velocity_x) < stop_threshold

    def stop_thrown_motion(self):
        self.thrown_velocity_x = 0

    def has_thrown_hit(self, target):
        return id(target) in self.thrown_hit_targets

    def mark_thrown_hit(self, target):
        self.thrown_hit_targets.add(id(target))

    def start_knockdown(self, duration=60):
        self.knockdown_remaining = duration

    def tick_knockdown(self):
        if self.knockdown_remaining > 0:
            self.knockdown_remaining -= 1
        return self.knockdown_remaining <= 0

    def start_getup(self, duration=20):
        self.getup_remaining = duration

    def tick_getup(self):
        if self.getup_remaining > 0:
            self.getup_remaining -= 1
        return self.getup_remaining <= 0
