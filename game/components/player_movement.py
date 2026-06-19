from game.components.movement_math import clamp_to_world_and_lane
from game.components.player_attack_movement import PlayerAttackMovement
from game.components.player_jump_movement import PlayerJumpMovement
from game.components.player_run_movement import PlayerRunMovement
from game.settings import RUN_ATTACK_REQUIRED_DISTANCE


class PlayerMovement:
    def __init__(self, air_state=None, run_attack_min_distance=RUN_ATTACK_REQUIRED_DISTANCE):
        self.run = PlayerRunMovement(run_attack_min_distance)
        self.attack_motion = PlayerAttackMovement()
        self.jump = PlayerJumpMovement(air_state)
        self.jump_pressed = False

    @property
    def air_state(self):
        return self.jump.air_state

    @property
    def is_jumping(self):
        return self.jump.is_jumping

    @is_jumping.setter
    def is_jumping(self, value):
        self.jump.is_jumping = value

    @property
    def is_running(self):
        return self.run.is_running

    @is_running.setter
    def is_running(self, value):
        self.run.is_running = value

    @property
    def last_run_attack_distance(self):
        return self.attack_motion.last_run_attack_distance

    @last_run_attack_distance.setter
    def last_run_attack_distance(self, value):
        self.attack_motion.last_run_attack_distance = value

    @property
    def ground_y(self):
        return self.jump.ground_y

    @ground_y.setter
    def ground_y(self, value):
        self.jump.ground_y = value

    @property
    def vx(self):
        return self.jump.vx

    @vx.setter
    def vx(self, value):
        self.jump.vx = value

    @property
    def vy(self):
        return self.jump.vy

    @vy.setter
    def vy(self, value):
        self.jump.vy = value

    def update_timers(self):
        self.run.update_timers()

    # stop the player from walking while grounded attacks are active.
    def update_movement(self, owner, player_input):
        if self.is_jumping or self.is_landing():
            return False
        if owner.combat_controller.is_attacking:
            return self.attack_motion.update_attack_movement(owner)

        return self.run.update_ground_movement(owner, player_input)

    def can_start_run_attack(self):
        return self.run.can_start_run_attack()

    def start_run_attack_cooldown(self, frames=None):
        self.run.start_run_attack_cooldown(frames)

    def start_run_attack_momentum(self, owner):
        self.attack_motion.start_run_attack_momentum(
            owner,
            self.run.run_direction,
            self.run.run_distance,
        )
        self.run.run_distance = 0

    def update_run_attack_momentum(self, owner):
        return self.attack_motion.update_run_attack_momentum(owner)

    def cancel_run_attack_momentum(self):
        self.attack_motion.cancel_run_attack_momentum()

    def start_attack_3_nudge(self, owner):
        self.attack_motion.start_attack_3_nudge(owner)

    def update_attack_nudge(self, owner):
        return self.attack_motion.update_attack_nudge(owner)

    def cancel_attack_nudge(self):
        self.attack_motion.cancel_attack_nudge()

    def update_jump_physics(self, owner, player_input):
        self.jump.update_jump_physics(owner, player_input)

    def start_jump(self, owner, player_input):
        self.jump.start_jump(owner, player_input)

    def is_landing(self):
        return self.jump.is_landing()

    def apply_world_bounds(self, owner, world_width=None, lane_top=None, lane_bottom=None):
        clamp_to_world_and_lane(
            owner,
            world_width,
            lane_top,
            lane_bottom,
            half_width=int(owner.width / 2),
            owner_name="Player",
        )
