class PlayerActionController:

    # pre tick operation
    def request_actions(self, owner, player_input):
        owner.intent.clear()
        player_can_act = owner.can_act()
        if not player_can_act:
            return

        self._update_jump_intent(owner, player_input)
        self._update_attack_intent(owner, player_input)
        if player_input.drop:
            owner.weapon_slot.drop(owner)

    def _update_jump_intent(self, owner, player_input):
        if player_input.jump:
            if not owner.input_tracker.jump_pressed:
                owner.input_tracker.press_jump()
                owner.input_tracker.jump_pressed = True
        else:
            owner.input_tracker.jump_pressed = False

        if owner.input_tracker.has_jump():
            owner.intent.jump(player_input)

    def _update_attack_intent(self, owner, player_input):
        if player_input.attack:
            if owner.movement.is_jumping:
                pass  # jump attack disabled
            else:
                if owner.input_tracker.run_attack_requires_attack_release:
                    owner.input_tracker.attack_pressed = True
                    owner.input_tracker.consume_attack()
                    return

                if not owner.input_tracker.attack_pressed:
                    owner.input_tracker.press_attack()
                    owner.input_tracker.attack_pressed = True
        else:
            owner.input_tracker.attack_pressed = False
            owner.input_tracker.jump_attack_pressed = False
            owner.input_tracker.run_attack_requires_attack_release = False

        if owner.input_tracker.has_attack():
            owner.intent.attack()
