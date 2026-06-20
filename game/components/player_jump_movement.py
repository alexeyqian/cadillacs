from game.components.movement_math import get_input_direction


class PlayerJumpMovement:
    def __init__(self, air_state=None):
        self.air_state = air_state

    @property
    def is_jumping(self):
        if self.air_state:
            return self.air_state.is_jumping
        return False

    @is_jumping.setter
    def is_jumping(self, value):
        if not self.air_state:
            return
        if value:
            self.air_state.is_grounded = False
        else:
            self.air_state.reset()

    def update_jump_physics(self, owner, player_input):
        if not self.air_state:
            return

        if self.air_state.is_landing:
            self.update_landing(owner)
            return

        if owner.state == owner.JUMP_TAKEOFF:
            self.update_takeoff(owner)
            return

        if self.air_state.is_grounded:
            return

        self.update_air_movement(owner)
        self.update_jump_arc(owner)

    def update_landing(self, owner):
        if self.air_state.update_landing():
            owner.state_machine.change_to(owner, owner.IDLE)

    def update_takeoff(self, owner):
        if self.air_state.update_takeoff():
            self.air_state.begin_jump()
            owner.state_machine.change_to(owner, owner.JUMP)

    def update_jump_arc(self, owner):
        landed = self.air_state.update_jump_arc()
        if not landed:
            return

        owner.input_state.jump_attack_pressed = False
        if owner.combat_controller.current_attack_name == owner.JUMP_ATTACK:
            owner.combat_controller.cancel_attack()

        if owner.state in [owner.JUMP, owner.JUMP_ATTACK]:
            owner.state_machine.change_to(owner, owner.LANDING)

    def update_air_movement(self, owner):
        owner.x += self.air_state.direction_x * self.air_state.air_move_speed
        owner.y += self.air_state.direction_y * self.air_state.air_move_speed * 0.6

    def start_jump(self, owner, player_input):
        if not self.air_state:
            return
        if self.is_jumping:
            return
        if self.is_landing():
            return
        if owner.combat_controller.is_attacking:
            return
        if owner.grab_controller.grabbed_enemy:
            return

        direction_x, direction_y = get_input_direction(player_input)
        if direction_x < 0:
            owner.facing_right = False
        elif direction_x > 0:
            owner.facing_right = True

        self.air_state.start_takeoff(direction_x, direction_y)
        owner.state_machine.change_to(owner, owner.JUMP_TAKEOFF)

    def is_landing(self):
        return bool(self.air_state and self.air_state.is_landing)
