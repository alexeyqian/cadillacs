class EnemyReactionController:
    def die(self, owner):
        self.cancel_attack(owner)
        owner.health.hp = 0
        owner.state = owner.DEAD
        owner.death_remaining = 30
        owner.death_countdown_started = False
        self.reset_attack_decision(owner)
        self.release_attack_slot(owner)

    # temp for renaming
    def take_damage(self, owner, damage, attacker_x):
        self.apply_hit(owner, damage, attacker_x)

    def apply_hit(self, owner, damage, attacker_x):
        if owner.state == owner.DEAD:
            return

        self.reset_attack_decision(owner)
        died = owner.health.take_damage(damage)
        flinch_threshold = self.get_flinch_threshold(owner)
        should_flinch = damage >= flinch_threshold
        if died:
            should_flinch = True

        if should_flinch:
            owner.hit_stun_remaining = owner.hit_stun_duration
            owner.state = owner.HIT
            # So if an enemy is interrupted, it releases the slot.
            self.cancel_attack(owner)
            self.release_attack_slot(owner)

            if attacker_x < owner.x:
                owner.knockback_velocity = 10
            else:
                owner.knockback_velocity = -10

        if owner.health.hp > 0 and self.should_knockdown_from_damage(damage):
            self.knockdown(owner)
            return

        if died:
            self.die(owner)

    def apply_knockback(self, owner):
        if owner.knockback_velocity == 0:
            return

        owner.x += owner.knockback_velocity
        owner.knockback_velocity *= 0.8

        if abs(owner.knockback_velocity) < 0.5:
            owner.knockback_velocity = 0

    def should_knockdown_from_damage(self, damage):
        return damage >= 40

    def get_flinch_threshold(self, owner):
        if owner.state == owner.ATTACK:
            return getattr(
                owner,
                "attack_flinch_damage_threshold",
                getattr(owner, "flinch_damage_threshold", 0),
            )

        return getattr(owner, "flinch_damage_threshold", 0)

    def knockdown(self, owner):
        if owner.state == owner.DEAD:
            return

        self.reset_attack_decision(owner)
        owner.state = owner.KNOCKDOWN
        owner.knockdown_remaining = 60
        owner.knockback_velocity = 0
        self.cancel_attack(owner)
        self.release_attack_slot(owner)

    def grabbed_by_player(self, owner):
        if owner.state == owner.DEAD:
            return

        self.reset_attack_decision(owner)
        owner.state = owner.GRABBED
        owner.knockback_velocity = 0
        owner.hit_stun_remaining = 0
        self.cancel_attack(owner)
        self.release_attack_slot(owner)

    def thrown_by_player(self, owner, direction):
        if owner.state == owner.DEAD:
            return

        self.reset_attack_decision(owner)
        owner.state = owner.THROWN
        owner.facing_right = direction > 0
        owner.thrown_velocity_x = 14 * direction
        owner.thrown_remaining = 30
        owner.thrown_hit_targets.clear()
        self.cancel_attack(owner)
        self.release_attack_slot(owner)
        self.take_thrown_damage(owner, owner.thrown_damage)

    def take_grab_knee_damage(self, owner, damage):
        if owner.state == owner.DEAD:
            return

        self.reset_attack_decision(owner)
        died = owner.health.take_damage(damage)

        if died:
            self.die(owner)
            return

        self.cancel_attack(owner)
        self.release_attack_slot(owner)
        owner.state = owner.GRABBED

    def take_thrown_damage(self, owner, damage):
        if owner.state == owner.DEAD:
            return
        self.reset_attack_decision(owner)
        self.cancel_attack(owner)
        self.release_attack_slot(owner)

        died = owner.health.take_damage(damage)

        if died:
            self.die(owner)

    def cancel_attack(self, owner):
        if hasattr(owner, "combat"):
            owner.combat.cancel_attack_timing(owner)
        elif hasattr(owner, "attack_controller"):
            owner.attack_controller.cancel()
            owner.attack_timer = 0
        else:
            owner.attack_timer = 0

    def reset_attack_decision(self, owner):
        if hasattr(owner, "attack_state"):
            owner.attack_state.reset_decision_timer()
        else:
            owner.attack_decision_timer = 0

    def release_attack_slot(self, owner):
        if hasattr(owner, "attack_state"):
            owner.attack_state.release_slot()
        else:
            owner.has_attack_slot = False
