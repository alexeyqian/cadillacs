class EnemyLifecycleController:
    def update_special_states(self, owner):
        if owner.state == owner.DEAD:
            self.update_dead_state(owner)
            return True

        # give enemies their own clash recovery timer,
        if owner.life_cycle.has_action_lock():
            owner.life_cycle.tick_action_lock()
            owner.state = owner.RECOIL
            owner.animation_controller.update(owner)
            return True
        
        if owner.state == owner.GRABBED:
            owner.animation_controller.update(owner)
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
        if owner.life_cycle.tick_thrown(owner):
            owner.state = owner.KNOCKDOWN
            owner.life_cycle.start_knockdown(60)
            owner.life_cycle.stop_thrown_motion()

        owner.animation_controller.update(owner)

    def update_knockdown_state(self, owner):
        if owner.life_cycle.tick_knockdown():
            owner.state = owner.GETUP
            owner.life_cycle.start_getup(20)

        owner.animation_controller.update(owner)

    def update_getup_state(self, owner):
        if owner.life_cycle.tick_getup():
            owner.state = owner.IDLE

        owner.animation_controller.update(owner)

    def update_hit_state(self, owner):
        if not owner.life_cycle.has_hit_stun():
            return False

        owner.life_cycle.tick_hit_stun()
        owner.reaction_controller.apply_knockback(owner)

        if not owner.life_cycle.has_hit_stun():
            owner.state = owner.IDLE
        else:
            owner.state = owner.HIT

        owner.animation_controller.update(owner)

        return True

    def update_dead_state(self, owner):
        if not owner.life_cycle.death_countdown_started:
            owner.life_cycle.begin_death_countdown()

        owner.life_cycle.tick_death()

        owner.animation_controller.update(owner)

    def update_timers(self, owner):
        if hasattr(owner, "combat_controller"):
            owner.combat_controller.update_timers()
        elif owner.attack_cooldown > 0:
            owner.attack_cooldown -= 1
        owner.flanking.update_timers()

    def is_ready_to_remove(self, owner):
        return owner.state == owner.DEAD and owner.life_cycle.is_death_finished()
