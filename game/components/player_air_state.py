# don't put owner-mutation in the state component 
class PlayerAirState:
    def __init__(self, jump_power, gravity, air_move_speed):
        self.jump_power = jump_power
        self.gravity = gravity
        self.air_move_speed = air_move_speed
        self.reset()

    def reset(self):
        self.is_grounded = True
        self.z = 0
        self.jump_velocity_z = 0
        self.air_frames = 0
        self.direction_x = 0
        self.direction_y = 0
        self.has_used_jump_attack = False
        self.jump_attack_hit_enemies = set()

    @property
    def is_jumping(self):
        return not self.is_grounded

    def start_jump(self, direction_x, direction_y):
        self.is_grounded = False
        self.z = 1
        self.jump_velocity_z = self.jump_power
        self.air_frames = 0
        self.direction_x = direction_x
        self.direction_y = direction_y
        self.has_used_jump_attack = False
        self.jump_attack_hit_enemies.clear()

    def update_jump_arc(self):
        if self.is_grounded:
            return False

        self.z += self.jump_velocity_z
        self.jump_velocity_z -= self.gravity
        self.air_frames += 1

        if self.z <= 0:
            self.land()
            return True

        return False

    def can_start_jump_attack(self):
        return not self.is_grounded and not self.has_used_jump_attack

    def mark_jump_attack_used(self):
        self.has_used_jump_attack = True

    def land(self):
        self.is_grounded = True
        self.z = 0
        self.jump_velocity_z = 0
        self.air_frames = 0
        self.direction_x = 0
        self.direction_y = 0

    def get_visual_y(self, ground_y):
        return ground_y - self.z
