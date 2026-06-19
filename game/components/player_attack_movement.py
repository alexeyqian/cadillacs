from game.settings import (
    ATTACK_3_FORWARD_NUDGE_FRAMES,
    ATTACK_3_FORWARD_NUDGE_SPEED_SCALE,
    RUN_ATTACK_MOMENTUM_FRAMES,
    RUN_ATTACK_MOMENTUM_SPEED_SCALE,
)


class PlayerAttackMovement:
    def __init__(self):
        self.last_run_attack_distance = 0

        self.run_attack_momentum_remaining = 0
        self.run_attack_momentum_direction = 0
        self.run_attack_momentum_speed = 0

        self.attack_nudge_remaining = 0
        self.attack_nudge_direction = 0
        self.attack_nudge_speed = 0

    def update_attack_movement(self, owner):
        if owner.combat_controller.current_attack_name == owner.RUN_ATTACK:
            return self.update_run_attack_momentum(owner)

        self.cancel_run_attack_momentum()
        return self.update_attack_nudge(owner)

    def start_run_attack_momentum(self, owner, run_direction, run_distance):
        direction = run_direction
        if direction == 0:
            direction = 1 if owner.facing_right else -1

        self.run_attack_momentum_direction = direction
        self.run_attack_momentum_remaining = RUN_ATTACK_MOMENTUM_FRAMES
        self.run_attack_momentum_speed = max(
            owner.speed,
            owner.run_speed * RUN_ATTACK_MOMENTUM_SPEED_SCALE,
        )
        self.last_run_attack_distance = run_distance

    def update_run_attack_momentum(self, owner):
        if self.run_attack_momentum_remaining <= 0:
            return False

        owner.x += self.run_attack_momentum_direction * self.run_attack_momentum_speed
        self.run_attack_momentum_remaining -= 1
        return True

    def cancel_run_attack_momentum(self):
        self.run_attack_momentum_remaining = 0
        self.run_attack_momentum_direction = 0
        self.run_attack_momentum_speed = 0

    def start_attack_3_nudge(self, owner):
        self.attack_nudge_direction = 1 if owner.facing_right else -1
        self.attack_nudge_remaining = ATTACK_3_FORWARD_NUDGE_FRAMES
        self.attack_nudge_speed = max(1, owner.speed * ATTACK_3_FORWARD_NUDGE_SPEED_SCALE)

    def update_attack_nudge(self, owner):
        if self.attack_nudge_remaining <= 0:
            return False

        owner.x += self.attack_nudge_direction * self.attack_nudge_speed
        self.attack_nudge_remaining -= 1
        return True

    def cancel_attack_nudge(self):
        self.attack_nudge_remaining = 0
        self.attack_nudge_direction = 0
        self.attack_nudge_speed = 0
