from game.settings import (
    FPS,
    RUN_ATTACK_COOLDOWN,
    RUN_ATTACK_REQUIRED_DISTANCE,
    RUN_TAP_WINDOW,
)
from game.components.movement_math import get_input_direction


class PlayerRunMovement:
    def __init__(self, run_attack_min_distance=RUN_ATTACK_REQUIRED_DISTANCE):
        # Running state
        self.is_running = False
        self.run_direction = 0    # last committed horizontal direction (-1 / 1); resets run_distance on reversal
        self.run_distance = 0     # cumulative pixels run without stopping; must reach run_attack_min_distance

        # Run attack gate
        self.run_attack_min_distance = run_attack_min_distance  # pixels of continuous running required
        self._run_attack_cooldown = 0  # frames until run attack is available again
        self._run_attack_cooldown_duration = RUN_ATTACK_COOLDOWN

        # Double-tap-to-run detection
        self._double_tap_run_active = False  # True once a valid double-tap is confirmed
        self._double_tap_window_remaining = 0           # frames left in the detection window for a second tap
        self._double_tap_window = max(1, int(RUN_TAP_WINDOW * FPS))  # max frames between two taps
        self._left_was_down = False   # previous-frame key state — used to detect the rising edge
        self._right_was_down = False

    def advance_timers(self):
        if self._double_tap_window_remaining > 0:
            self._double_tap_window_remaining -= 1
        if self._run_attack_cooldown > 0:
            self._run_attack_cooldown -= 1

    # the return boolean means: It means "the player moved at least one pixel this frame" 
    def update_ground_movement(self, owner, player_input) -> bool:
        horizontal_direction, vertical_direction = get_input_direction(player_input)
        previous_run_direction = self.run_direction

        self._update_run_input(player_input.left, player_input.right, horizontal_direction)
        self.is_running = horizontal_direction != 0 and self._double_tap_run_active

        move_speed = owner.run_speed if self.is_running else owner.speed
        self._move_owner(owner, horizontal_direction, vertical_direction, move_speed)
        self._update_run_distance(horizontal_direction, move_speed, previous_run_direction)

        return horizontal_direction != 0 or vertical_direction != 0

    def can_start_run_attack(self):
        return (
            self.is_running
            and self.run_distance >= self.run_attack_min_distance
            and self._run_attack_cooldown <= 0
        )

    def start_run_attack_cooldown(self, frames=None):
        if frames is None:
            frames = self._run_attack_cooldown_duration
        self._run_attack_cooldown = max(0, int(frames))

    # --- Private helpers ---

    def _move_owner(self, owner, horizontal_direction, vertical_direction, move_speed):
        if horizontal_direction < 0:
            owner.facing_right = False
        elif horizontal_direction > 0:
            owner.facing_right = True
        owner.x += horizontal_direction * move_speed
        owner.y += vertical_direction * move_speed

    def _update_run_distance(self, horizontal_direction, move_speed, previous_run_direction):
        if not self.is_running or horizontal_direction == 0:
            self.run_distance = 0
            return
        if self.run_direction != previous_run_direction:
            self.run_distance = 0
        self.run_distance += move_speed

    def _update_run_input(self, left_down, right_down, horizontal_direction):
        if horizontal_direction == 0:
            self._double_tap_run_active = False
            self._left_was_down = left_down
            self._right_was_down = right_down
            return

        if left_down and not self._left_was_down:
            self._register_tap(-1)
        elif right_down and not self._right_was_down:
            self._register_tap(1)

        if self._double_tap_run_active and self.run_direction != horizontal_direction:
            self._double_tap_run_active = False

        self._left_was_down = left_down
        self._right_was_down = right_down

    def _register_tap(self, direction):
        if self.run_direction == direction and self._double_tap_window_remaining > 0:
            self._double_tap_run_active = True
        self.run_direction = direction
        self._double_tap_window_remaining = self._double_tap_window
