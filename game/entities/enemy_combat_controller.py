class EnemyCombatController:
    def start_attack(self, owner):
        owner.state = owner.ATTACK
        owner.attack_has_hit = False
        owner.attack_timer = 0
        owner.animation_controller.play(owner.ATTACK)
        owner.animation_controller.reset_current_animation()

    def update_attack(self, owner, player):
        owner.face_player(player)
        owner.attack_timer += 1

        attack_rect = owner.get_attack_rect()
        player_hurt_rect = player.get_hurt_rect()

        if attack_rect and player_hurt_rect and not owner.attack_has_hit:
            if attack_rect.colliderect(player_hurt_rect):
                player.take_damage(owner.attack_damage)
                owner.attack_has_hit = True

        animation = owner.animation_controller.get_current_animation()
        is_last_frame = animation.current_frame == len(animation.frames) - 1
        last_frame_finished = animation.timer >= animation.frame_duration - 1
        # enemy attack hitbox is active for the visible final attack frame
        if is_last_frame and last_frame_finished:
            owner.state = owner.PATROL
            owner.attack_has_hit = False
            owner.attack_cooldown = owner.attack_cooldown_duration