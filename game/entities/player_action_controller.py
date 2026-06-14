class PlayerActionController:
    def update(self, owner, player_input):
        self.update_jump_input(owner, player_input)
        self.update_attack_input(owner, player_input)
        self.update_fire_input(owner, player_input)

    def update_jump_input(self, owner, player_input):
        if player_input.jump:
            if not owner.jump_pressed:
                owner.start_jump(player_input)
                owner.jump_pressed = True
        else:
            owner.jump_pressed = False

    def update_attack_input(self, owner, player_input):
        if player_input.attack:
            if owner.is_jumping:
                if not owner.jump_attack_pressed:
                    owner.start_jump_attack()
                    owner.jump_attack_pressed = True
            else:
                if owner.grabbed_enemy:
                    owner.start_grab_knee_attack()
                else:
                    owner.start_attack()
        else:
            owner.jump_attack_pressed = False

    def update_fire_input(self, owner, player_input):
        if player_input.fire:
            if not owner.fire_pressed:
                owner.fire_weapon()
                owner.fire_pressed = True
        else:
            owner.fire_pressed = False