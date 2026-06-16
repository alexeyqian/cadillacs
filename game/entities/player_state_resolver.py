class PlayerStateResolver:
    def update_after_movement(self, owner, moving):
        if owner.combat.is_attacking:
            return

        if owner.movement.is_jumping:
            if owner.state != owner.JUMP_ATTACK:
                owner.state_machine.change_to(owner, owner.JUMP)
            return

        if owner.grab.throw_remaining > 0:
            owner.state_machine.change_to(owner, owner.THROW)
        elif owner.grab.grab_knee_remaining > 0:
            owner.state_machine.change_to(owner, owner.GRAB_KNEE)
        elif owner.grab.grabbed_enemy:
            owner.state_machine.change_to(owner, owner.GRAB)
        else:
            if moving and owner.movement.is_running:
                owner.state_machine.change_to(owner, owner.RUN)
            elif moving:
                owner.state_machine.change_to(owner, owner.WALK)
            else:
                owner.state_machine.change_to(owner, owner.IDLE)
