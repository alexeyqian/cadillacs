class PlayerStateResolver:
    def resolve(self, owner, moving):
        if owner.combat_state.is_attacking:
            return

        if owner.movement.is_jumping:
            if owner.state != owner.JUMP_ATTACK:
                owner.state_machine.change_to(owner, owner.JUMP)
            return

        if owner.grab_controller.is_throwing(owner):
            owner.state_machine.change_to(owner, owner.THROW)
        elif owner.grab_controller.is_grab_kneeing(owner):
            owner.state_machine.change_to(owner, owner.GRAB_KNEE)
        elif owner.grab_state.grabbed_enemy:
            owner.state_machine.change_to(owner, owner.GRAB)
        else:
            if moving and owner.movement.is_running:
                owner.state_machine.change_to(owner, owner.RUN)
            elif moving:
                owner.state_machine.change_to(owner, owner.WALK)
            else:
                owner.state_machine.change_to(owner, owner.IDLE)
