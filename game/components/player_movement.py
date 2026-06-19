from game.settings import (
    RUN_TAP_WINDOW,
    FPS,
    RUN_ATTACK_REQUIRED_DISTANCE,
    RUN_ATTACK_MOMENTUM_FRAMES,
    RUN_ATTACK_MOMENTUM_SPEED_SCALE,
    ATTACK_3_FORWARD_NUDGE_FRAMES,
    ATTACK_3_FORWARD_NUDGE_SPEED_SCALE,
)
from game.components.movement_math import clamp_to_world_and_lane


class PlayerMovement:
    def __init__(self, speed, air_state=None):
        self.air_state = air_state
        self.is_running = False
        self.run_active = False
        self.run_direction = 0
        self.run_tap_remaining = 0
        self.run_tap_window = max(1, int(RUN_TAP_WINDOW * FPS))
        self.run_distance = 0
        self.last_run_attack_distance = 0
        self.run_attack_required_distance = RUN_ATTACK_REQUIRED_DISTANCE
        self.left_pressed = False
        self.right_pressed = False

        self._is_jumping = False
        self.jump_pressed = False
        self.ground_y = 0
        self.vx = 0
        self.vy = 0
        self.jump_power = 12
        self.gravity = 0.7
        self.air_speed = speed * 1.2
        self.air_friction = 0.92
        self.run_attack_momentum_remaining = 0
        self.run_attack_momentum_direction = 0
        self.run_attack_momentum_speed = 0
        self.attack_nudge_remaining = 0
        self.attack_nudge_direction = 0
        self.attack_nudge_speed = 0

    @property
    def is_jumping(self):
        if self.air_state:
            return self.air_state.is_jumping
        return self._is_jumping

    @is_jumping.setter
    def is_jumping(self, value):
        if self.air_state:
            if value:
                self.air_state.is_grounded = False
            else:
                self.air_state.reset()
            return

        self._is_jumping = value

    def update_timers(self):
        if self.run_tap_remaining > 0:
            self.run_tap_remaining -= 1

    # stop the player from walking while grounded attacks are active.
    def update_movement(self, owner, player_input):
        moving = False
        if self.is_jumping or self.is_landing():
            return False
        if owner.combat_controller.is_attacking:
            if owner.combat_controller.current_attack_name == owner.RUN_ATTACK:
                return self.update_run_attack_momentum(owner)
            self.cancel_run_attack_momentum()
            return self.update_attack_nudge(owner)

        left_down = player_input.left
        right_down = player_input.right
        up_down = player_input.up
        down_down = player_input.down
        shift_down = player_input.run

        horizontal_direction = 0
        if left_down and not right_down:
            horizontal_direction = -1
        elif right_down and not left_down:
            horizontal_direction = 1

        previous_run_direction = self.run_direction
        self.update_run_input(left_down, right_down, horizontal_direction)
        self.is_running = horizontal_direction != 0 and (
            shift_down or self.run_active
        )

        move_speed = owner.run_speed if self.is_running else owner.speed
        horizontal_run_distance = 0

        if left_down:
            owner.x -= move_speed
            owner.facing_right = False
            moving = True
            if self.is_running:
                horizontal_run_distance += move_speed
        if right_down:
            owner.x += move_speed
            owner.facing_right = True
            moving = True
            if self.is_running:
                horizontal_run_distance += move_speed
        if up_down:
            owner.y -= move_speed
            moving = True
        if down_down:
            owner.y += move_speed
            moving = True

        self.update_run_distance(horizontal_run_distance, previous_run_direction)

        return moving

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
            and self.run_distance >= self.run_attack_required_distance
        )

    def start_run_attack_momentum(self, owner):
        direction = self.run_direction
        if direction == 0:
            direction = 1 if owner.facing_right else -1

        self.run_attack_momentum_direction = direction
        self.run_attack_momentum_remaining = RUN_ATTACK_MOMENTUM_FRAMES
        self.run_attack_momentum_speed = max(
            owner.speed,
            owner.run_speed * RUN_ATTACK_MOMENTUM_SPEED_SCALE,
        )
        self.last_run_attack_distance = self.run_distance
        self.run_distance = 0

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

    def update_run_input(self, left_down, right_down, horizontal_direction):
        if horizontal_direction == 0:
            self.run_active = False
            self.left_pressed = left_down
            self.right_pressed = right_down
            return

        left_just_pressed = left_down and not self.left_pressed
        right_just_pressed = right_down and not self.right_pressed

        if left_just_pressed:
            self.check_run_double_tap(-1)
        elif right_just_pressed:
            self.check_run_double_tap(1)

        if self.run_active and self.run_direction != horizontal_direction:
            self.run_active = False

        self.left_pressed = left_down
        self.right_pressed = right_down

    def check_run_double_tap(self, direction):
        if self.run_direction == direction and self.run_tap_remaining > 0:
            self.run_active = True

        self.run_direction = direction
        self.run_tap_remaining = self.run_tap_window

    def update_jump_physics(self, owner, player_input):
        if not self.air_state:
            self.update_legacy_jump_physics(owner, player_input)
            return

        if self.air_state.is_landing:
            if self.air_state.update_landing():
                owner.state_machine.change_to(owner, owner.IDLE)
            return

        if owner.state == owner.JUMP_TAKEOFF:
            if self.air_state.update_takeoff():
                self.air_state.begin_jump()
                owner.state_machine.change_to(owner, owner.JUMP)
            return

        if self.air_state.is_grounded:
            return

        self.update_air_movement(owner)
        landed = self.air_state.update_jump_arc()
        if landed:
            self.vx = 0
            self.vy = 0
            owner.input_state.jump_attack_pressed = False
            if owner.combat_controller.current_attack_name == owner.JUMP_ATTACK:
                owner.combat_controller.cancel_attack()

            if owner.state in [owner.JUMP, owner.JUMP_ATTACK]:
                owner.state_machine.change_to(owner, owner.LANDING)

    def update_air_movement(self, owner):
        owner.x += self.air_state.direction_x * self.air_state.air_move_speed
        owner.y += self.air_state.direction_y * self.air_state.air_move_speed * 0.6

    def update_legacy_jump_physics(self, owner, player_input):
        if not self.is_jumping:
            return

        if player_input.left:
            self.vx = -self.air_speed
            owner.facing_right = False
        elif player_input.right:
            self.vx = self.air_speed
            owner.facing_right = True

        owner.x += self.vx
        owner.y += self.vy
        self.vx *= self.air_friction
        self.vy += self.gravity

        if owner.y >= self.ground_y:
            owner.y = self.ground_y
            self.vx = 0
            self.vy = 0
            self.is_jumping = False
            owner.input_state.jump_attack_pressed = False

            if owner.state in [owner.JUMP, owner.JUMP_ATTACK]:
                owner.state_machine.change_to(owner, owner.IDLE)

    def start_jump(self, owner, player_input):
        if self.is_jumping:
            return
        if self.is_landing():
            return
        if owner.combat_controller.is_attacking:
            return
        if owner.grab_controller.grabbed_enemy:
            return

        self.ground_y = owner.y
        self.vx = 0

        direction_x = 0
        direction_y = 0

        if player_input.left and not player_input.right:
            direction_x = -1
            owner.facing_right = False
        elif player_input.right and not player_input.left:
            direction_x = 1
            owner.facing_right = True

        if player_input.up and not player_input.down:
            direction_y = -1
        elif player_input.down and not player_input.up:
            direction_y = 1

        if self.air_state:
            self.air_state.start_takeoff(direction_x, direction_y)
            owner.state_machine.change_to(owner, owner.JUMP_TAKEOFF)
            return

        self.is_jumping = True
        self.vy = -self.jump_power
        self.vx = direction_x * self.air_speed
        owner.state_machine.change_to(owner, owner.JUMP)

    def is_landing(self):
        return bool(self.air_state and self.air_state.is_landing)

    def apply_world_bounds(self, owner, world_width=None, lane_top=None, lane_bottom=None):
        clamp_to_world_and_lane(
            owner,
            world_width,
            lane_top,
            lane_bottom,
            half_width=int(owner.width / 2),
            owner_name="Player",
        )
