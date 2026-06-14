class EnemyCombatMixin:
    def die(self):
        self.hp = 0
        self.state = self.DEAD
        self.death_timer = 30
        self.death_timer_started = False

    def start_attack(self):
        self.state = self.ATTACK
        self.attack_timer = 0
        self.attack_has_hit = False

    def update_attack(self, player):
        self.facing_right = player.x > self.x
        self.attack_timer += 1

        active_start = self.attack_windup
        active_end = self.attack_windup + self.attack_active
        is_active_frame = active_start <= self.attack_timer < active_end
        if is_active_frame and not self.attack_has_hit:
            attack_rect = self.get_attack_rect()
            player_hurt_rect = player.get_hurt_rect()
            if attack_rect and player_hurt_rect and attack_rect.colliderect(player_hurt_rect):
                player.take_damage(self.attack_damage)
                self.attack_has_hit = True
        
        if self.attack_timer >= self.attack_total_duration:
            self.state = self.PATROL # TODO: what state should be here
            self.attack_timer = 0
            self.attack_has_hit = False
            self.attack_cooldown = self.attack_cooldown_duration # ?

    def take_damage(self, damage, attacker_x):
        if self.state == self.DEAD:
            return

        self.hp -= damage
        self.hit_timer = self.hit_stun_duration
        self.state = self.HIT

        # knockback direction based on attacker's position
        if attacker_x < self.x:
            self.knockback_velocity = 10
        else:
            self.knockback_velocity = -10
            
        if self.hp > 0 and self.should_knockdown_from_damage(damage):
            self.knockdown()
            return

        if self.hp <= 0:
            self.die()

    def apply_knockback(self):
        if self.knockback_velocity == 0:
            return
        self.x += self.knockback_velocity
        # friction slows down knockback over time
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

    # this prevents knee attacks from accidentally knocking the enemy out of grab state
    def take_grab_knee_damage(self, damage):
        if self.state == self.DEAD:
            return
        self.hp -= damage
        if self.hp <= 0:
            self.die()
            return

        self.state = self.GRABBED

    def take_thrown_damage(self, damage):
        if self.state == self.DEAD:
            return

        self.hp -= damage
        if self.hp <= 0:
            self.die()
        
