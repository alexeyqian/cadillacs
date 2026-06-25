class PlayerAirState:
    def __init__(
        self,
        jump_power,
        gravity,
        air_move_speed,
        landing_recovery_frames,
    ):
        self.jump_power = jump_power
        self.gravity = gravity
        self.air_move_speed = air_move_speed
        self.landing_recovery_frames = landing_recovery_frames
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
        # post-landing recovery frames
        # The player can't act while it's counting down.
        self.landing_remaining = 0

    @property
    def is_jumping(self):
        return not self.is_grounded

    @property
    def is_landing(self):
        return self.landing_remaining > 0

    def start_jump(self, direction_x, direction_y):
        self.is_grounded = False
        self.z = 1
        self.jump_velocity_z = self.jump_power
        self.air_frames = 0
        self.direction_x = direction_x
        self.direction_y = direction_y
        self.has_used_jump_attack = False
        self.jump_attack_hit_enemies.clear()
        self.landing_remaining = 0

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

    def update_landing(self):
        if self.landing_remaining <= 0:
            return True

        self.landing_remaining -= 1
        return self.landing_remaining <= 0

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
        self.landing_remaining = self.landing_recovery_frames

    def get_visual_y(self, ground_y):
        return ground_y - self.z
