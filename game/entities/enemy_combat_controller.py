class EnemyCombatController:
    def start_attack(self, owner):
        owner.state = owner.ATTACK
        owner.attack_has_hit = False
        owner.animation_controller.play(owner.ATTACK)
        owner.animation_controller.reset_current_animation()

    def update_attack(self, owner, player):
        owner.face_player(player)

        attack_rect = owner.get_attack_rect()
        player_hurt_rect = player.get_hurt_rect()

        if attack_rect and player_hurt_rect and not owner.attack_has_hit:
            if attack_rect.colliderect(player_hurt_rect):
                player.take_damage(owner.attack_damage)
                owner.attack_has_hit = True

        animation = owner.animation_controller.get_current_animation()

        if animation.current_frame == len(animation.frames) - 1:
            owner.state = owner.PATROL
            owner.attack_has_hit = False
            owner.attack_cooldown = owner.attack_cooldown_duration
