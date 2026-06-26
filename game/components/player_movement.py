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

        # True when the player moved at least one pixel this frame
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

    # stop the player from walking while grounded attacks are active.
    def update_movement(self, owner, player_input):
        if self.is_jumping:
            self.moving = False
            return
        if owner.combat_state.is_attacking:
            self.moving = self.attack_movement.update_attack_movement(owner)
            return

        self.moving = self.run_movement.update_ground_movement(owner, player_input)

    def start_run_attack_momentum(self, owner):
        self.attack_movement.start_run_attack_momentum(
            owner,
            self.run_movement.run_direction,
            self.run_movement.run_distance,
        )
        self.run_movement.run_distance = 0

    def apply_world_bounds(self, owner, world_width=None, lane_top=None, lane_bottom=None):
        clamp_to_world_and_lane(
            owner,
            world_width,
            lane_top,
            lane_bottom,
            half_width=int(owner.width / 2),
            owner_name="Player",
        )
