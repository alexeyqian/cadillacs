class EnemyCombatMixin:
    def start_attack(self):
        self.state = self.ATTACK
        self.attack_timer = 0
        self.attack_has_hit = False

    def update_attack(self, player):
        self.facing_right = player.x > self.x
        self.attack_timer += 1

        attack_rect = self.get_attack_rect()
        player_hurt_rect = player.get_hurt_rect()

        if attack_rect and player_hurt_rect and not self.attack_has_hit:
            if attack_rect.colliderect(player_hurt_rect):
                player.take_damage(self.attack_damage)
                self.attack_has_hit = True
        
        if self.attack_timer >= self.attack_total_duration:
            self.state = self.PATROL # TODO: what state should be here
            self.attack_timer = 0
            self.attack_has_hit = False
            self.attack_cooldown = self.attack_cooldown_duration # ?
        
