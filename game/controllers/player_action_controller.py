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
            if not owner.input_state.jump_pressed:
                self.buffer_and_try_action(
                    owner,
                    self.JUMP_ACTION,
                    self.JUMP_BUFFER_FRAMES,
                    lambda: self.try_start_jump(owner, player_input),
                )
                owner.input_state.jump_pressed = True
        else:
            owner.input_state.jump_pressed = False

        self.try_buffered_action(
            owner,
            self.JUMP_ACTION,
            lambda: self.try_start_jump(owner, player_input),
        )

    # avoid doing this:
    # as soon as the attack timer ends, 
    # holding J immediately starts the next combo step. 
    # So the player can auto-chain punches by holding the button.
    def update_attack_input(self, owner, player_input):
        if player_input.attack:
            if owner.movement.is_jumping:
                if not owner.input_state.jump_attack_pressed:
                    self.buffer_and_try_action(
                        owner,
                        self.ATTACK_ACTION,
                        self.ATTACK_BUFFER_FRAMES,
                        lambda: self.try_start_attack(owner),
                    )
                    owner.input_state.jump_attack_pressed = True
            else:
                if owner.input_state.run_attack_requires_attack_release:
                    owner.input_state.attack_pressed = True
                    self.consume_action(owner, self.ATTACK_ACTION)
                    return

                if not owner.input_state.attack_pressed:
                    self.buffer_and_try_action(
                        owner,
                        self.ATTACK_ACTION,
                        self.ATTACK_BUFFER_FRAMES,
                        lambda: self.try_start_attack(owner),
                    )
                    owner.input_state.attack_pressed = True
        else:
            owner.input_state.attack_pressed = False
            owner.input_state.jump_attack_pressed = False
            owner.input_state.run_attack_requires_attack_release = False

        self.try_buffered_action(
            owner,
            self.ATTACK_ACTION,
            lambda: self.try_start_attack(owner),
        )

    def update_fire_input(self, owner, player_input):
        if player_input.fire:
            if not owner.input_state.fire_pressed:
                owner.weapon_slot.fire(owner)
                owner.input_state.fire_pressed = True
        else:
            owner.input_state.fire_pressed = False

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
        owner.input_buffer.press(action, frames=frames)

    def buffer_and_try_action(self, owner, action, frames, start_action):
        self.buffer_action(owner, action, frames)
        if start_action():
            self.consume_action(owner, action)

    def try_buffered_action(self, owner, action, start_action):
        if self.has_buffered_action(owner, action):
            if start_action():
                self.consume_action(owner, action)

    def consume_action(self, owner, action):
        owner.input_buffer.consume(action)

    def has_buffered_action(self, owner, action):
        return owner.input_buffer.has(action)

    def update_input_buffer(self, owner):
        owner.input_buffer.update()
