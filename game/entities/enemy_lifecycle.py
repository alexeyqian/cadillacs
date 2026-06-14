class EnemyLifecycleMixin:
    def update_special_states(self):
        return self.lifecycle.update_special_states(self)

    def update_thrown_state(self):
        self.lifecycle.update_thrown_state(self)

    def update_knockdown_state(self):
        self.lifecycle.update_knockdown_state(self)

    def update_getup_state(self):
        self.lifecycle.update_getup_state(self)

    def update_hit_state(self):
        return self.lifecycle.update_hit_state(self)

    def update_dead_state(self):
        self.lifecycle.update_dead_state(self)

    def update_timers(self):
        self.lifecycle.update_timers(self)

    def is_ready_to_remove(self):
        return self.lifecycle.is_ready_to_remove(self)