class EnemyCombatController:
    def start_attack(self, owner):
        owner.state = owner.ATTACK
        owner.attack_already_hit = False
        owner.has_attack_slot = owner.uses_melee_attack_slot()
        owner.attack_timer = 0
        owner.animation_controller.play(owner.ATTACK)
        owner.animation_controller.reset_current_animation()

    # Enemy attack has explicit windup frames
    # Enemy attack only damages during active frames
    # Enemy attack has explicit recovery before it can act again
    def update_attack(self, owner, player):
        owner.face_player(player)
        owner.attack_timer += 1

        attack_rect = owner.get_attack_rect()
        player_hurt_rect = player.get_hurt_rect()

        if (owner.is_attack_active() 
            and attack_rect and player_hurt_rect 
            and not owner.attack_already_hit):
            if attack_rect.colliderect(player_hurt_rect):
                player.take_damage(owner.attack_damage)
                owner.attack_already_hit = True

        if owner.attack_timer >= owner.get_attack_total_duration():
            owner.state = owner.PATROL
            owner.attack_timer = 0
            owner.attack_already_hit = False
            owner.has_attack_slot = False
            owner.attack_cooldown = owner.attack_cooldown_duration
