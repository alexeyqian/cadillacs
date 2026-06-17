class PlayerAirState:
    def __init__(
        self,
        jump_power,
        gravity,
        air_move_speed,
        takeoff_frames,
        landing_recovery_frames,
    ):
        self.jump_power = jump_power
        self.gravity = gravity
        self.air_move_speed = air_move_speed
        self.takeoff_frames = takeoff_frames
        self.landing_recovery_frames = landing_recovery_frames
        self.reset()

    def reset(self):
        self.is_grounded = True
        self.z = 0
        self.jump_velocity_z = 0
        self.air_time = 0
        self.direction_x = 0
        self.direction_y = 0
        self.has_used_jump_attack = False
        self.jump_attack_hit_enemies = set()
        self.takeoff_timer = 0
        self.landing_timer = 0

    @property
    def is_jumping(self):
        return not self.is_grounded or self.takeoff_timer > 0

    @property
    def is_landing(self):
        return self.landing_timer > 0

    def start_takeoff(self, direction_x, direction_y):
        self.is_grounded = True
        self.z = 0
        self.jump_velocity_z = 0
        self.air_time = 0
        self.direction_x = direction_x
        self.direction_y = direction_y
        self.has_used_jump_attack = False
        self.jump_attack_hit_enemies.clear()
        self.takeoff_timer = self.takeoff_frames
        self.landing_timer = 0

    def update_takeoff(self):
        if self.takeoff_timer <= 0:
            return True

        self.takeoff_timer -= 1
        return self.takeoff_timer <= 0

    def begin_jump(self):
        self.is_grounded = False
        self.z = 1
        self.jump_velocity_z = self.jump_power
        self.air_time = 0

    def update_jump_arc(self):
        if self.is_grounded:
            return False

        self.z += self.jump_velocity_z
        self.jump_velocity_z -= self.gravity
        self.air_time += 1

        if self.z <= 0:
            self.land()
            return True

        return False

    def update_landing(self):
        if self.landing_timer <= 0:
            return True

        self.landing_timer -= 1
        return self.landing_timer <= 0

    def can_start_jump_attack(self):
        return (
            not self.is_grounded
            and not self.has_used_jump_attack
            and self.takeoff_timer <= 0
        )

    def mark_jump_attack_used(self):
        self.has_used_jump_attack = True

    def land(self):
        self.is_grounded = True
        self.z = 0
        self.jump_velocity_z = 0
        self.air_time = 0
        self.direction_x = 0
        self.direction_y = 0
        self.takeoff_timer = 0
        self.landing_timer = self.landing_recovery_frames

    def get_visual_y(self, ground_y):
        return ground_y - self.z
