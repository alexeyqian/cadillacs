class EnemyCondition:
    def __init__(self):
        # Death
        self._death_remaining = 30

        # Clash recovery — keeps the clash fair: enemy cannot instantly resume pressure.
        # enemy's clash/recoil lock
        self._action_lock_remaining = 0

        # Hit stun and knockback
        self._hit_stun_remaining = 0
        self._knockback_velocity = 0

        # Thrown state
        self._thrown_velocity_x = 0
        self._thrown_remaining = 0
        self.throw_damage = 0          # read directly by combat_system for thrown-enemy collision damage
        self._thrown_hit_targets = set()

        # Knockdown / getup
        self._knockdown_remaining = 0
        self._getup_remaining = 0

    # --- Death ---

    def start_death_countdown(self, duration=30):
        self._death_remaining = duration

    def tick_death(self):
        if self._death_remaining > 0:
            self._death_remaining -= 1

    def is_death_finished(self):
        return self._death_remaining <= 0

    # --- Action lock ---

    def has_action_lock(self):
        return self._action_lock_remaining > 0

    def set_action_lock(self, frames):
        self._action_lock_remaining = frames

    def tick_action_lock(self):
        if self._action_lock_remaining > 0:
            self._action_lock_remaining -= 1

    # --- Hit stun ---

    def has_hit_stun(self):
        return self._hit_stun_remaining > 0

    def set_hit_stun(self, frames):
        self._hit_stun_remaining = frames

    def clear_hit_stun(self):
        self._hit_stun_remaining = 0

    def tick_hit_stun(self):
        if self._hit_stun_remaining > 0:
            self._hit_stun_remaining -= 1

    # --- Knockback ---

    def set_knockback(self, velocity):
        self._knockback_velocity = velocity

    def clear_knockback(self):
        self._knockback_velocity = 0

    # --- Thrown ---

    def start_thrown(self, direction, damage, velocity=14, duration=30):
        self._thrown_velocity_x = velocity * direction
        self._thrown_remaining = duration
        self.throw_damage = damage
        self._thrown_hit_targets.clear()

    def has_thrown_hit(self, target):
        return id(target) in self._thrown_hit_targets

    def mark_thrown_hit(self, target):
        self._thrown_hit_targets.add(id(target))

    # --- Knockdown / getup ---

    def start_knockdown(self, duration=60):
        self._knockdown_remaining = duration

    def tick_knockdown(self):
        if self._knockdown_remaining > 0:
            self._knockdown_remaining -= 1
        return self._knockdown_remaining <= 0

    def start_getup(self, duration=20):
        self._getup_remaining = duration

    def tick_getup(self):
        if self._getup_remaining > 0:
            self._getup_remaining -= 1
        return self._getup_remaining <= 0
