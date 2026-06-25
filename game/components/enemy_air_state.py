from game.settings import ENEMY_JUMP_GRAVITY, ENEMY_JUMP_POWER

JUMP_COOLDOWN = 120


class EnemyAirState:
    def __init__(self, jump_power=ENEMY_JUMP_POWER, gravity=ENEMY_JUMP_GRAVITY):
        self.jump_power = jump_power  # initial upward velocity applied when a jump starts
        self.gravity = gravity        # velocity subtracted each tick, pulling z back to 0
        self._jump_cooldown = 0  # frames remaining before the enemy may jump again
        self.reset()

    def reset(self):
        self.z = 0               # current height above ground (0 = on ground)
        self.jump_velocity_z = 0 # vertical speed this frame; reduced by gravity each tick
        self.is_grounded = True  # True while on the ground; False during the jump arc

    @property
    def is_jumping(self):
        return not self.is_grounded

    def start_jump(self):
        self.is_grounded = False
        self.z = 1
        self.jump_velocity_z = self.jump_power

    @property
    def can_jump_now(self):
        return self.is_grounded and self._jump_cooldown == 0

    def on_jump_requested(self):
        self._jump_cooldown = JUMP_COOLDOWN

    def tick_cooldown(self):
        if self._jump_cooldown > 0:
            self._jump_cooldown -= 1

    def update(self):
        if self.is_grounded:
            return

        self.z += self.jump_velocity_z
        self.jump_velocity_z -= self.gravity

        if self.z <= 0:
            self.reset()

    def get_visual_y_offset(self):
        # z grows upward (positive = higher), but screen y grows downward,
        # so negate z to get the pixel offset to apply to the sprite's y position.
        return -self.z

    def get_visual_y(self, ground_y):
        return ground_y + self.get_visual_y_offset()
