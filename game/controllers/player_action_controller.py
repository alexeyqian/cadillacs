#  it translates inputs into intent
class PlayerActionController:
    ATTACK_ACTION = "attack"
    JUMP_ACTION = "jump"
    ATTACK_BUFFER_FRAMES = 12
    JUMP_BUFFER_FRAMES = 6

    def update(self, owner, player_input):
        owner.intent.clear()
        self._update_jump_input(owner, player_input)
        self._update_attack_input(owner, player_input)
        self._update_fire_input(owner, player_input)

    def advance_timers(self, owner):
        owner.input_buffer.update()

    def _update_jump_input(self, owner, player_input):
        if player_input.jump:
            if not owner.input_state.jump_pressed:
                owner.input_buffer.press(self.JUMP_ACTION, frames=self.JUMP_BUFFER_FRAMES)
                owner.input_state.jump_pressed = True
        else:
            owner.input_state.jump_pressed = False

        if owner.input_buffer.has(self.JUMP_ACTION):
            owner.intent.jump(player_input)

    # avoid doing this:
    # as soon as the attack timer ends,
    # holding J immediately starts the next combo step.
    # So the player can auto-chain punches by holding the button.
    def _update_attack_input(self, owner, player_input):
        if player_input.attack:
            if owner.movement.is_jumping:
                pass  # jump attack disabled
            else:
                if owner.input_state.run_attack_requires_attack_release:
                    owner.input_state.attack_pressed = True
                    owner.input_buffer.consume(self.ATTACK_ACTION)
                    return

                if not owner.input_state.attack_pressed:
                    owner.input_buffer.press(self.ATTACK_ACTION, frames=self.ATTACK_BUFFER_FRAMES)
                    owner.input_state.attack_pressed = True
        else:
            owner.input_state.attack_pressed = False
            owner.input_state.jump_attack_pressed = False
            owner.input_state.run_attack_requires_attack_release = False

        if owner.input_buffer.has(self.ATTACK_ACTION):
            owner.intent.attack()

    def _update_fire_input(self, owner, player_input):
        if player_input.fire:
            if not owner.input_state.fire_pressed:
                owner.intent.fire()
                owner.input_state.fire_pressed = True
        else:
            owner.input_state.fire_pressed = False
