class EnemyStateController:
    def update(self, owner):
        if owner.state == owner.DEAD:
            self._update_dead_state(owner)
            return

        if owner.reaction_controller.has_action_lock(owner):
            owner.reaction_controller.tick_action_lock(owner)
            owner.state = owner.RECOIL
            return

        if owner.state == owner.GRABBED:
            return

        if owner.state == owner.THROWN:
            self._update_thrown_state(owner)
            return

        if owner.state == owner.KNOCKDOWN:
            self._update_knockdown_state(owner)
            return

        if owner.state == owner.GETUP:
            self._update_getup_state(owner)

    def _update_thrown_state(self, owner):
        if owner.reaction_controller.tick_thrown(owner):
            owner.state = owner.KNOCKDOWN
            owner.reaction_controller.start_knockdown(owner, 60)

    def _update_knockdown_state(self, owner):
        if owner.reaction_controller.tick_knockdown(owner):
            owner.state = owner.GETUP
            owner.reaction_controller.start_getup(owner, 20)

    def _update_getup_state(self, owner):
        if owner.reaction_controller.tick_getup(owner):
            owner.state = owner.IDLE

    def _update_dead_state(self, owner):
        owner.reaction_controller.tick_death(owner)
