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

    def start_jump(self, owner, player_input):
        if not self.air_state or self.is_jumping:
            return
        if owner.combat_state.is_attacking:
            return
        if owner.grab_state.grabbed_enemy:
            return

        direction_x, direction_y = get_input_direction(player_input)
        if direction_x < 0:
            owner.facing_right = False
        elif direction_x > 0:
            owner.facing_right = True

        self.air_state.start_jump(direction_x, direction_y)
        owner.state_machine.change_to(owner, owner.JUMP)

    def update_jump_physics(self, owner, player_input):
        if not self.air_state or self.air_state.is_grounded:
            return

        if self.air_state.update_jump_arc():  # returns True on landing
            owner.input_state.jump_attack_pressed = False
            if owner.combat_state.current_attack_name == owner.JUMP_ATTACK:
                owner.combat_controller.cancel_attack(owner)
            if owner.state in [owner.JUMP, owner.JUMP_ATTACK]:
                owner.state_machine.change_to(owner, owner.IDLE)
            return

        self._update_air_movement(owner, player_input)

    # --- Private helpers ---

    def _update_air_movement(self, owner, player_input):
        horizontal_direction, _vertical_direction = get_input_direction(player_input)
        if horizontal_direction < 0:
            owner.facing_right = False
        elif horizontal_direction > 0:
            owner.facing_right = True
        owner.x += horizontal_direction * self.air_state.air_move_speed
        owner.y += self.air_state.direction_y * self.air_state.air_move_speed * 0.6
