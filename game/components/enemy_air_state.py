from game.settings import ENEMY_JUMP_GRAVITY, ENEMY_JUMP_POWER


class EnemyAirState:
    def __init__(self, jump_power=ENEMY_JUMP_POWER, gravity=ENEMY_JUMP_GRAVITY):
        self.jump_power = jump_power
        self.gravity = gravity
        self.reset()

    def reset(self):
        self.z = 0
        self.jump_velocity_z = 0
        self.is_grounded = True

    @property
    def is_jumping(self):
        return not self.is_grounded

    def start_jump(self):
        self.is_grounded = False
        self.z = 1
        self.jump_velocity_z = self.jump_power

    def update(self):
        if self.is_grounded:
            return

        self.z += self.jump_velocity_z
        self.jump_velocity_z -= self.gravity

        if self.z <= 0:
            self.reset()

    def get_visual_y_offset(self):
        return -self.z

    def get_visual_y(self, ground_y):
        return ground_y + self.get_visual_y_offset()
