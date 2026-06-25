class PlayerStateResolver:
    def resolve(self, owner, moving):
        if owner.combat_controller.is_attacking:
            return

        if owner.air and owner.air.is_landing:
            owner.state_machine.change_to(owner, owner.LANDING)
            return

        if owner.movement.is_jumping:
            if owner.state not in [owner.JUMP_TAKEOFF, owner.JUMP_ATTACK]:
                owner.state_machine.change_to(owner, owner.JUMP)
            return

        if owner.grab_controller.throw_remaining > 0:
            owner.state_machine.change_to(owner, owner.THROW)
        elif owner.grab_controller.grab_knee_remaining > 0:
            owner.state_machine.change_to(owner, owner.GRAB_KNEE)
        elif owner.grab_controller.grabbed_enemy:
            owner.state_machine.change_to(owner, owner.GRAB)
        else:
            if moving and owner.movement.is_running:
                owner.state_machine.change_to(owner, owner.RUN)
            elif moving:
                owner.state_machine.change_to(owner, owner.WALK)
            else:
                owner.state_machine.change_to(owner, owner.IDLE)
