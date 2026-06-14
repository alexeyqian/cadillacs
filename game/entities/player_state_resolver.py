class PlayerStateResolver:
    def update_after_movement(self, owner, moving):
        if owner.combat.is_attacking:
            return

        if owner.movement.is_jumping:
            if owner.state != owner.JUMP_ATTACK:
                owner.state = owner.JUMP
            return

        if owner.grab.throw_timer > 0:
            owner.state = owner.THROW
        elif owner.grab.grab_knee_timer > 0:
            owner.state = owner.GRAB_KNEE
        elif owner.grab.grabbed_enemy:
            owner.state = owner.GRAB
        else:
            if moving and owner.movement.is_running:
                owner.state = owner.RUN
            elif moving:
                owner.state = owner.WALK
            else:
                owner.state = owner.IDLE