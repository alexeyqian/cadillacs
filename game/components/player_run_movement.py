from game.settings import (
    FPS,
    RUN_ATTACK_COOLDOWN,
    RUN_ATTACK_REQUIRED_DISTANCE,
    RUN_TAP_WINDOW,
)
from game.components.movement_math import get_input_direction


class PlayerRunMovement:
    def __init__(self, run_attack_min_distance=RUN_ATTACK_REQUIRED_DISTANCE):
        self.is_running = False
        self.double_tap_run_active = False
        self.run_direction = 0
        self.double_tap_timer = 0
        self.double_tap_window = max(1, int(RUN_TAP_WINDOW * FPS))
        self.run_distance = 0
        self.run_attack_min_distance = run_attack_min_distance
        self.run_attack_cooldown_remaining = 0
        self.run_attack_cooldown_frames = RUN_ATTACK_COOLDOWN
        self.left_was_down = False
        self.right_was_down = False

    def advance_timers(self):
        if self.double_tap_timer > 0:
            self.double_tap_timer -= 1
        if self.run_attack_cooldown_remaining > 0:
            self.run_attack_cooldown_remaining -= 1

    def update_ground_movement(self, owner, player_input):
        horizontal_direction, vertical_direction = get_input_direction(player_input)
        previous_run_direction = self.run_direction

        self.update_run_input(
            player_input.left,
            player_input.right,
            horizontal_direction,
        )
        self.is_running = horizontal_direction != 0 and (
            player_input.run or self.double_tap_run_active
        )

        move_speed = owner.run_speed if self.is_running else owner.speed
        moving = self.move_owner(owner, horizontal_direction, vertical_direction, move_speed)
        horizontal_run_distance = self.get_horizontal_run_distance(
            horizontal_direction,
            move_speed,
        )

        self.update_run_distance(horizontal_run_distance, previous_run_direction)

        return moving

    def move_owner(self, owner, horizontal_direction, vertical_direction, move_speed):
        if horizontal_direction < 0:
            owner.facing_right = False
        elif horizontal_direction > 0:
            owner.facing_right = True

        owner.x += horizontal_direction * move_speed
        owner.y += vertical_direction * move_speed
        return horizontal_direction != 0 or vertical_direction != 0

    def get_horizontal_run_distance(self, horizontal_direction, move_speed):
        if self.is_running and horizontal_direction != 0:
            return move_speed
        return 0

    def update_run_distance(self, horizontal_run_distance, previous_run_direction):
        if not self.is_running or horizontal_run_distance <= 0:
            self.run_distance = 0
            return

        if self.run_direction != previous_run_direction:
            self.run_distance = 0

        self.run_distance += horizontal_run_distance

    def can_start_run_attack(self):
        return (
            self.is_running
            and self.run_distance >= self.run_attack_min_distance
            and self.run_attack_cooldown_remaining <= 0
        )

    def start_run_attack_cooldown(self, frames=None):
        if frames is None:
            frames = self.run_attack_cooldown_frames
        self.run_attack_cooldown_remaining = max(0, int(frames))

    def update_run_input(self, left_down, right_down, horizontal_direction):
        if horizontal_direction == 0:
            self.double_tap_run_active = False
            self.left_was_down = left_down
            self.right_was_down = right_down
            return

        left_just_pressed = left_down and not self.left_was_down
        right_just_pressed = right_down and not self.right_was_down

        if left_just_pressed:
            self.check_run_double_tap(-1)
        elif right_just_pressed:
            self.check_run_double_tap(1)

        if self.double_tap_run_active and self.run_direction != horizontal_direction:
            self.double_tap_run_active = False

        self.left_was_down = left_down
        self.right_was_down = right_down

    def check_run_double_tap(self, direction):
        if self.run_direction == direction and self.double_tap_timer > 0:
            self.double_tap_run_active = True

        self.run_direction = direction
        self.double_tap_timer = self.double_tap_window
