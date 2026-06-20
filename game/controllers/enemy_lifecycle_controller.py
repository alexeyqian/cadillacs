class EnemyLifecycleController:
    def __init__(self, spawn_x=0):
        self.spawn_x = spawn_x

    def update_lifecycle_state(self, owner):
        if owner.state == owner.DEAD:
            self._update_dead_state(owner)
            return True

        # give enemies their own clash recovery timer,
        if owner.condition.has_action_lock():
            owner.condition.tick_action_lock()
            owner.state = owner.RECOIL
            return True
        
        if owner.state == owner.GRABBED:
            return True

        if owner.state == owner.THROWN:
            self._update_thrown_state(owner)
            return True

        if owner.state == owner.KNOCKDOWN:
            self._update_knockdown_state(owner)
            return True

        if owner.state == owner.GETUP:
            self._update_getup_state(owner)
            return True

        return False

    def _update_thrown_state(self, owner):
        if owner.condition.tick_thrown(owner):
            owner.state = owner.KNOCKDOWN
            owner.condition.start_knockdown(60)
            owner.condition.stop_thrown_motion()

    def _update_knockdown_state(self, owner):
        if owner.condition.tick_knockdown():
            owner.state = owner.GETUP
            owner.condition.start_getup(20)

    def _update_getup_state(self, owner):
        if owner.condition.tick_getup():
            owner.state = owner.IDLE

    def _update_dead_state(self, owner):
        if not owner.condition.death_countdown_started:
            owner.condition.begin_death_countdown()

        owner.condition.tick_death()

    def is_ready_to_remove(self, owner):
        return owner.state == owner.DEAD and owner.condition.is_death_finished()
