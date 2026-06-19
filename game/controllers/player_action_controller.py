class PlayerActionController:
    ATTACK_ACTION = "attack"
    JUMP_ACTION = "jump"
    ATTACK_BUFFER_FRAMES = 12
    JUMP_BUFFER_FRAMES = 6

    def update(self, owner, player_input):
        self.update_jump_input(owner, player_input)
        self.update_attack_input(owner, player_input)
        self.update_fire_input(owner, player_input)
        self.update_input_buffer(owner)

    def update_jump_input(self, owner, player_input):
        if player_input.jump:
            if not owner.movement.jump_pressed:
                self.buffer_action(owner, self.JUMP_ACTION, self.JUMP_BUFFER_FRAMES)
                if self.try_start_jump(owner, player_input):
                    self.consume_action(owner, self.JUMP_ACTION)
                owner.movement.jump_pressed = True
        else:
            owner.movement.jump_pressed = False

        if self.has_buffered_action(owner, self.JUMP_ACTION):
            if self.try_start_jump(owner, player_input):
                self.consume_action(owner, self.JUMP_ACTION)

    # avoid doing this:
    # as soon as the attack timer ends, 
    # holding J immediately starts the next combo step. 
    # So the player can auto-chain punches by holding the button.
    def update_attack_input(self, owner, player_input):
        if player_input.attack:
            if owner.movement.is_jumping:
                if not owner.input_state.jump_attack_pressed:
                    self.buffer_action(owner, self.ATTACK_ACTION, self.ATTACK_BUFFER_FRAMES)
                    if self.try_start_attack(owner):
                        self.consume_action(owner, self.ATTACK_ACTION)
                    owner.input_state.jump_attack_pressed = True
            else:
                if owner.input_state.run_attack_requires_attack_release:
                    owner.input_state.attack_pressed = True
                    self.consume_action(owner, self.ATTACK_ACTION)
                    return

                if not owner.input_state.attack_pressed:
                    self.buffer_action(owner, self.ATTACK_ACTION, self.ATTACK_BUFFER_FRAMES)
                    if self.try_start_attack(owner):
                        self.consume_action(owner, self.ATTACK_ACTION)
                    owner.input_state.attack_pressed = True
        else:
            owner.input_state.attack_pressed = False
            owner.input_state.jump_attack_pressed = False
            owner.input_state.run_attack_requires_attack_release = False

        if self.has_buffered_action(owner, self.ATTACK_ACTION):
            if self.try_start_attack(owner):
                self.consume_action(owner, self.ATTACK_ACTION)

    def update_fire_input(self, owner, player_input):
        if player_input.fire:
            if not owner.weapon_slot.fire_pressed:
                owner.weapon_slot.fire(owner)
                owner.weapon_slot.fire_pressed = True
        else:
            owner.weapon_slot.fire_pressed = False

    def try_start_jump(self, owner, player_input):
        previous_state = owner.state
        owner.movement.start_jump(owner, player_input)
        return owner.state != previous_state

    def try_start_attack(self, owner):
        previous_attack_name = owner.combat_controller.current_attack_name

        if owner.movement.is_jumping:
            owner.combat_controller.start_jump_attack(owner)
        elif owner.grab_controller.grabbed_enemy:
            owner.combat_controller.start_grab_knee_attack(owner)
        else:
            owner.combat_controller.start_attack(owner)

        return owner.combat_controller.current_attack_name != previous_attack_name

    def buffer_action(self, owner, action, frames=None):
        input_buffer = getattr(owner, "input_buffer", None)
        if input_buffer:
            input_buffer.press(action, frames=frames)

    def consume_action(self, owner, action):
        input_buffer = getattr(owner, "input_buffer", None)
        if input_buffer:
            input_buffer.consume(action)

    def has_buffered_action(self, owner, action):
        input_buffer = getattr(owner, "input_buffer", None)
        return bool(input_buffer and input_buffer.has(action))

    def update_input_buffer(self, owner):
        input_buffer = getattr(owner, "input_buffer", None)
        if input_buffer:
            input_buffer.update()
