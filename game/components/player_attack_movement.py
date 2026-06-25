from game.settings import (
    ATTACK_3_FORWARD_NUDGE_FRAMES,
    ATTACK_3_FORWARD_NUDGE_SPEED_SCALE,
    RUN_ATTACK_MOMENTUM_FRAMES,
    RUN_ATTACK_MOMENTUM_SPEED_SCALE,
)


class PlayerAttackMovement:
    def __init__(self):
        # Recorded so combat controller can scale run-attack knockback by how far the player ran.
        self.last_run_attack_distance = 0

        # Run attack momentum — player keeps sliding forward for a few frames after a run attack
        # lands, so hits feel like they have physical weight behind them.
        self._run_attack_momentum_remaining = 0
        self._run_attack_momentum_direction = 0
        self._run_attack_momentum_speed = 0

        # Combo finisher nudge — a short forward push on the final combo hit (ATTACK3)
        # so the player closes the small gap that opens up during the combo string.
        self._combo_finisher_nudge_remaining = 0
        self._combo_finisher_nudge_direction = 0
        self._combo_finisher_nudge_speed = 0

    def update_attack_movement(self, owner):
        if owner.combat_controller.current_attack_name == owner.RUN_ATTACK:
            return self._update_run_attack_momentum(owner)
        self.cancel_run_attack_momentum()
        return self._update_combo_finisher_nudge(owner)

    def start_run_attack_momentum(self, owner, run_direction, run_distance):
        # fall back to facing direction if run_direction wasn't committed yet
        direction = run_direction if run_direction != 0 else (1 if owner.facing_right else -1)
        self._run_attack_momentum_direction = direction
        self._run_attack_momentum_remaining = RUN_ATTACK_MOMENTUM_FRAMES
        self._run_attack_momentum_speed = max(
            owner.speed,
            owner.run_speed * RUN_ATTACK_MOMENTUM_SPEED_SCALE,
        )
        self.last_run_attack_distance = run_distance

    def cancel_run_attack_momentum(self):
        self._run_attack_momentum_remaining = 0
        self._run_attack_momentum_direction = 0
        self._run_attack_momentum_speed = 0

    def start_combo_finisher_nudge(self, owner):
        self._combo_finisher_nudge_direction = 1 if owner.facing_right else -1
        self._combo_finisher_nudge_remaining = ATTACK_3_FORWARD_NUDGE_FRAMES
        self._combo_finisher_nudge_speed = max(1, owner.speed * ATTACK_3_FORWARD_NUDGE_SPEED_SCALE)

    def cancel_combo_finisher_nudge(self):
        self._combo_finisher_nudge_remaining = 0
        self._combo_finisher_nudge_direction = 0
        self._combo_finisher_nudge_speed = 0

    # --- Private helpers ---

    def _update_run_attack_momentum(self, owner):
        if self._run_attack_momentum_remaining <= 0:
            return False
        owner.x += self._run_attack_momentum_direction * self._run_attack_momentum_speed
        self._run_attack_momentum_remaining -= 1
        return True

    def _update_combo_finisher_nudge(self, owner):
        if self._combo_finisher_nudge_remaining <= 0:
            return False
        owner.x += self._combo_finisher_nudge_direction * self._combo_finisher_nudge_speed
        self._combo_finisher_nudge_remaining -= 1
        return True
