class PlayerActionController:
    def update(self, owner, player_input):
        self.update_jump_input(owner, player_input)
        self.update_attack_input(owner, player_input)
        self.update_fire_input(owner, player_input)

    def update_jump_input(self, owner, player_input):
        if player_input.jump:
            if not owner.movement.jump_pressed:
                owner.movement.start_jump(player_input)
                owner.movement.jump_pressed = True
        else:
            owner.movement.jump_pressed = False

    def update_attack_input(self, owner, player_input):
        if player_input.attack:
            if owner.movement.is_jumping:
                if not owner.jump_attack_pressed:
                    owner.combat.start_jump_attack()
                    owner.jump_attack_pressed = True
            else:
                if owner.grab.grabbed_enemy:
                    owner.combat.start_grab_knee_attack()
                else:
                    owner.combat.start_attack()
        else:
            owner.jump_attack_pressed = False

    def update_fire_input(self, owner, player_input):
        if player_input.fire:
            if not owner.weapon_slot.fire_pressed:
                owner.weapon_slot.fire(owner)
                owner.weapon_slot.fire_pressed = True
        else:
            owner.weapon_slot.fire_pressed = False