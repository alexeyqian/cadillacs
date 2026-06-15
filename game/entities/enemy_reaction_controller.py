class EnemyReactionController:
    def die(self, owner):
        owner.health.hp = 0
        owner.state = owner.DEAD
        owner.death_timer = 30
        owner.death_timer_started = False

    def take_damage(self, owner, damage, attacker_x):
        if owner.state == owner.DEAD:
            return

        died = owner.health.take_damage(damage)
        should_interrupt = damage >= owner.hit_interrupt_damage_threshold
        if died:
            should_interrupt = True

        if should_interrupt:
            owner.hit_timer = owner.hit_stun_duration
            owner.state = owner.HIT

            if attacker_x < owner.x:
                owner.knockback_velocity = 10
            else:
                owner.knockback_velocity = -10

        if owner.health.hp > 0 and owner.should_knockdown_from_damage(damage):
            owner.knockdown()
            return

        if died:
            owner.die()

    def apply_knockback(self, owner):
        if owner.knockback_velocity == 0:
            return

        owner.x += owner.knockback_velocity
        owner.knockback_velocity *= 0.8

        if abs(owner.knockback_velocity) < 0.5:
            owner.knockback_velocity = 0

    def should_knockdown_from_damage(self, damage):
        return damage >= 40

    def knockdown(self, owner):
        if owner.state == owner.DEAD:
            return

        owner.state = owner.KNOCKDOWN
        owner.knockdown_timer = 60
        owner.knockback_velocity = 0

    def grabbed_by_player(self, owner):
        if owner.state == owner.DEAD:
            return

        owner.state = owner.GRABBED
        owner.knockback_velocity = 0
        owner.hit_timer = 0

    def thrown_by_player(self, owner, direction):
        if owner.state == owner.DEAD:
            return

        owner.state = owner.THROWN
        owner.facing_right = direction > 0
        owner.thrown_velocity_x = 14 * direction
        owner.thrown_timer = 30
        owner.thrown_hit_targets.clear()
        owner.take_thrown_damage(owner.thrown_damage)

    def take_grab_knee_damage(self, owner, damage):
        if owner.state == owner.DEAD:
            return

        died = owner.health.take_damage(damage)

        if died:
            owner.die()
            return

        owner.state = owner.GRABBED

    def take_thrown_damage(self, owner, damage):
        if owner.state == owner.DEAD:
            return

        died = owner.health.take_damage(damage)

        if died:
            owner.die()
