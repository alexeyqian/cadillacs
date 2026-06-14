class EnemyCombatMixin:
    def start_attack(self):
        self.state = self.ATTACK
        self.attack_has_hit = False
        self.animation_controller.play(self.ATTACK)
        self.animation_controller.reset_current_animation()

    def update_attack(self, player):
        self.face_player(player)

        attack_rect = self.get_attack_rect()
        player_hurt_rect = player.get_hurt_rect()

        if attack_rect and player_hurt_rect and not self.attack_has_hit:
            if attack_rect.colliderect(player_hurt_rect):
                player.take_damage(self.attack_damage)
                self.attack_has_hit = True

        animation = self.animation_controller.get_current_animation()
        # use is_finished
        if animation.current_frame == len(animation.frames) - 1:
            self.state = self.PATROL
            self.attack_has_hit = False
            self.attack_cooldown = self.attack_cooldown_duration
