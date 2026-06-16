from game.settings import WORLD_WIDTH, RUN_DOUBLE_TAP_TIME, FPS


class PlayerMovement:
    def __init__(self, speed):
        self.is_running = False
        self.run_active = False
        self.run_direction = 0
        self.run_tap_remaining = 0
        self.run_tap_window = max(1, int(RUN_DOUBLE_TAP_TIME * FPS))
        self.left_pressed = False
        self.right_pressed = False

        self.is_jumping = False
        self.jump_pressed = False
        self.ground_y = 0
        self.vx = 0
        self.vy = 0
        self.jump_power = -20
        self.gravity = 2
        self.air_speed = speed * 1.2
        self.air_friction = 0.92
        self.run_attack_momentum_remaining = 0
        self.run_attack_momentum_direction = 0
        self.run_attack_momentum_speed = 0

    def update_timers(self):
        if self.run_tap_remaining > 0:
            self.run_tap_remaining -= 1

    # stop the player from walking while grounded attacks are active.
    def update_movement(self, owner, player_input):
        moving = False
        if self.is_jumping:
            return False
        if owner.combat.is_attacking:
            if owner.combat.current_attack_name == owner.RUN_ATTACK:
                return self.update_run_attack_momentum(owner)
            self.cancel_run_attack_momentum()
            return False

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

        self.update_run_input(left_down, right_down, horizontal_direction)
        self.is_running = horizontal_direction != 0 and (
            shift_down or self.run_active
        )

        move_speed = owner.run_speed if self.is_running else owner.speed

        if left_down:
            owner.x -= move_speed
            owner.facing_right = False
            moving = True
        if right_down:
            owner.x += move_speed
            owner.facing_right = True
            moving = True
        if up_down:
            owner.y -= move_speed
            moving = True
        if down_down:
            owner.y += move_speed
            moving = True

        return moving

    def start_run_attack_momentum(self, owner):
        direction = self.run_direction
        if direction == 0:
            direction = 1 if owner.facing_right else -1

        self.run_attack_momentum_direction = direction
        self.run_attack_momentum_remaining = 20
        self.run_attack_momentum_speed = max(owner.speed, owner.run_speed * 0.75)

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
        if owner.combat.is_attacking:
            return
        if owner.grab.grabbed_enemy:
            return

        self.is_jumping = True
        self.ground_y = owner.y
        self.vy = self.jump_power
        self.vx = 0

        if player_input.left:
            self.vx = -self.air_speed
            owner.facing_right = False
        elif player_input.right:
            self.vx = self.air_speed
            owner.facing_right = True

        owner.state_machine.change_to(owner, owner.JUMP)

    def apply_world_bounds(self, owner, world_width=None, lane_top=None, lane_bottom=None):
        if world_width is None:
            world_width = WORLD_WIDTH
        if lane_top is None or lane_bottom is None:
            raise ValueError("Player.apply_world_bounds requires lane_top and lane_bottom")

        half_w = int(owner.width / 2)
        owner.x = max(half_w, owner.x)
        owner.x = min(owner.x, world_width - half_w)
        owner.y = max(lane_top, owner.y)
        owner.y = min(lane_bottom, owner.y)
