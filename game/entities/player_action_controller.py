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

    # avoid doing this:
    # as soon as the attack timer ends, 
    # holding J immediately starts the next combo step. 
    # So the player can auto-chain punches by holding the button.
    def update_attack_input(self, owner, player_input):
        if player_input.attack:
            if owner.movement.is_jumping:
                if not owner.input_state.jump_attack_pressed:
                    owner.combat.start_jump_attack(owner)
                    owner.input_state.jump_attack_pressed = True
            else:
                if (
                    owner.movement.is_running
                    and owner.input_state.run_attack_requires_attack_release
                ):
                    owner.input_state.attack_pressed = True
                    return

                if not owner.input_state.attack_pressed:
                    if owner.grab.grabbed_enemy:
                        owner.combat.start_grab_knee_attack(owner)
                    else:
                        owner.combat.start_attack(owner)
                        if owner.combat.current_attack_name == owner.RUN_ATTACK:
                            owner.input_state.run_attack_requires_attack_release = True
                    owner.input_state.attack_pressed = True
        else:
            owner.input_state.attack_pressed = False
            owner.input_state.jump_attack_pressed = False
            owner.input_state.run_attack_requires_attack_release = False

    def update_fire_input(self, owner, player_input):
        if player_input.fire:
            if not owner.weapon_slot.fire_pressed:
                owner.weapon_slot.fire(owner)
                owner.weapon_slot.fire_pressed = True
        else:
            owner.weapon_slot.fire_pressed = False
