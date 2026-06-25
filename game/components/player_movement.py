from game.components.movement_math import clamp_to_world_and_lane
from game.components.player_attack_movement import PlayerAttackMovement
from game.components.player_jump_movement import PlayerJumpMovement
from game.components.player_run_movement import PlayerRunMovement
from game.settings import RUN_ATTACK_REQUIRED_DISTANCE


class PlayerMovement:
    def __init__(self, air_state=None, run_attack_min_distance=RUN_ATTACK_REQUIRED_DISTANCE):
        self.run_movement = PlayerRunMovement(run_attack_min_distance)
        self.jump_movement = PlayerJumpMovement(air_state)
        self.attack_movement = PlayerAttackMovement()

        # It means "the player moved at least one pixel this frame"
        self.moving = False

    @property
    def is_jumping(self):
        return self.jump_movement.is_jumping

    @is_jumping.setter
    def is_jumping(self, value):
        self.jump_movement.is_jumping = value

    @property
    def is_running(self):
        return self.run_movement.is_running

    @is_running.setter
    def is_running(self, value):
        self.run_movement.is_running = value

    @property
    def last_run_attack_distance(self):
        return self.attack_movement.last_run_attack_distance

    @last_run_attack_distance.setter
    def last_run_attack_distance(self, value):
        self.attack_movement.last_run_attack_distance = value

    def advance_timers(self):
        self.run_movement.advance_timers()

    # stop the player from walking while grounded attacks are active.
    def update_movement(self, owner, player_input):
        if self.is_jumping:
            self.moving = False
            return
        if owner.combat_controller.is_attacking:
            self.moving = self.attack_movement.update_attack_movement(owner)
            return

        self.moving = self.run_movement.update_ground_movement(owner, player_input)

    def can_start_run_attack(self):
        return self.run_movement.can_start_run_attack()

    def start_run_attack_cooldown(self, frames=None):
        self.run_movement.start_run_attack_cooldown(frames)

    def start_run_attack_momentum(self, owner):
        self.attack_movement.start_run_attack_momentum(
            owner,
            self.run_movement.run_direction,
            self.run_movement.run_distance,
        )
        self.run_movement.run_distance = 0

    def cancel_run_attack_momentum(self):
        self.attack_movement.cancel_run_attack_momentum()

    def start_combo_finisher_nudge(self, owner):
        self.attack_movement.start_combo_finisher_nudge(owner)

    def cancel_combo_finisher_nudge(self):
        self.attack_movement.cancel_combo_finisher_nudge()

    def update_jump_physics(self, owner, player_input):
        self.jump_movement.update_jump_physics(owner, player_input)

    def start_jump(self, owner, player_input):
        self.jump_movement.start_jump(owner, player_input)

    def apply_world_bounds(self, owner, world_width=None, lane_top=None, lane_bottom=None):
        clamp_to_world_and_lane(
            owner,
            world_width,
            lane_top,
            lane_bottom,
            half_width=int(owner.width / 2),
            owner_name="Player",
        )
