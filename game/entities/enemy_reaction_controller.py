class EnemyReactionController:
    def die(self, owner):
        owner.health.hp = 0
        owner.state = owner.DEAD
        owner.death_timer = 30
        owner.death_timer_started = False
        owner.has_attack_slot = False

    # temp for renaming
    def take_damage(self, owner, damage, attacker_x):
        self.apply_hit(owner, damage, attacker_x)

    def apply_hit(self, owner, damage, attacker_x):
        if owner.state == owner.DEAD:
            return

        died = owner.health.take_damage(damage)
        should_flinch = damage >= owner.flinch_damage_threshold
        if died:
            should_flinch = True

        if should_flinch:
            owner.hit_timer = owner.hit_stun_duration
            owner.state = owner.HIT
            # So if an enemy is interrupted, it releases the slot.
            owner.has_attack_slot = False

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
        owner.has_attack_slot = False

    def grabbed_by_player(self, owner):
        if owner.state == owner.DEAD:
            return

        owner.state = owner.GRABBED
        owner.knockback_velocity = 0
        owner.hit_timer = 0
        owner.has_attack_slot = False

    def thrown_by_player(self, owner, direction):
        if owner.state == owner.DEAD:
            return

        owner.state = owner.THROWN
        owner.facing_right = direction > 0
        owner.thrown_velocity_x = 14 * direction
        owner.thrown_timer = 30
        owner.thrown_hit_targets.clear()
        owner.has_attack_slot = False
        owner.take_thrown_damage(owner.thrown_damage)

    def take_grab_knee_damage(self, owner, damage):
        if owner.state == owner.DEAD:
            return

        died = owner.health.take_damage(damage)

        if died:
            owner.die()
            return

        owner.has_attack_slot = False
        owner.state = owner.GRABBED

    def take_thrown_damage(self, owner, damage):
        if owner.state == owner.DEAD:
            return
        owner.has_attack_slot = False

        died = owner.health.take_damage(damage)

        if died:
            owner.die()
