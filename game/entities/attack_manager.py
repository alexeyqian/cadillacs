class AttackManager:
    def __init__(self):
        self.current_attack_name = None
        self.current_attack = None
        self.elapsed_frames = 0
        self.has_connected = False
        self.hit_targets = set()

    @property
    def is_attacking(self):
        return self.current_attack is not None

    @property
    def remaining_frames(self):
        if not self.current_attack:
            return 0
        return max(0, self.get_attack_duration() - self.elapsed_frames)

    @property
    def attack_timer(self):
        return self.elapsed_frames

    @attack_timer.setter
    def attack_timer(self, value):
        self.elapsed_frames = value

    @property
    def attack_remaining(self):
        return self.remaining_frames

    @property
    def attack_connected(self):
        return self.has_connected

    @attack_connected.setter
    def attack_connected(self, value):
        self.has_connected = value

    def start(self, attack_name, attack_data):
        self.current_attack_name = attack_name
        self.current_attack = attack_data
        self.elapsed_frames = 0
        self.has_connected = False
        self.hit_targets = set()

    def advance(self):
        if not self.current_attack:
            return False

        self.elapsed_frames += 1
        return self.is_finished()

    def is_finished(self):
        if not self.current_attack:
            return False
        return self.elapsed_frames >= self.get_attack_duration()

    def is_active(self):
        if not self.current_attack:
            return False
        # why return true here?
        # It is a fallback for older/simple attack data that does not define windup, active, and recovery.
        if not self.has_attack_phases():
            return True

        active_start = self.current_attack.windup
        active_end = self.current_attack.windup + self.current_attack.active
        return active_start <= self.elapsed_frames < active_end

    def get_phase_name(self):
        if not self.current_attack:
            return ""
        if not self.has_attack_phases():
            return "ACTIVE"

        if self.elapsed_frames < self.current_attack.windup:
            return "WINDUP"

        active_end = self.current_attack.windup + self.current_attack.active
        if self.elapsed_frames < active_end:
            return "ACTIVE"

        if self.elapsed_frames < self.get_attack_duration():
            return "RECOVERY"

        return "DONE"

    def get_timing_label(self):
        if not self.current_attack:
            return ""

        return (
            f"{self.current_attack_name} "
            f"{self.get_phase_name()} "
            f"{self.elapsed_frames}/{self.get_attack_duration()}"
        )

    def mark_connected(self):
        self.has_connected = True

    def has_hit_target(self, target):
        return id(target) in self.hit_targets

    def mark_target_hit(self, target):
        self.hit_targets.add(id(target))
        self.mark_connected()

    def get_hit_count(self):
        return len(self.hit_targets)

    def can_hit_more_targets(self):
        if not self.current_attack:
            return False
        return self.get_hit_count() < self.get_max_targets()

    def can_hit_target(self, target):
        return self.can_hit_more_targets() and not self.has_hit_target(target)

    def get_max_targets(self):
        if not self.current_attack:
            return 0
        return getattr(self.current_attack, "max_targets", 1)

    def finish(self):
        finished_attack_name = self.current_attack_name
        finished_attack = self.current_attack
        attack_connected = self.has_connected
        self.cancel()
        return finished_attack_name, finished_attack, attack_connected

    def cancel(self):
        self.current_attack_name = None
        self.current_attack = None
        self.elapsed_frames = 0
        self.has_connected = False
        self.hit_targets = set()

    def get_attack_duration(self):
        if not self.current_attack:
            return 0
        if hasattr(self.current_attack, "duration"):
            return self.current_attack.duration
        return self.current_attack.total_duration

    def has_attack_phases(self):
        return all(
            hasattr(self.current_attack, field_name)
            for field_name in ["windup", "active", "recovery"]
        )

    # Compatibility aliases for older call sites while migration continues.
    def start_attack(self, attack_name, attack_data):
        self.start(attack_name, attack_data)

    def update_attack_timer(self):
        return self.advance()

    def finish_attack(self):
        return self.finish()

    def cancel_attack(self):
        self.cancel()
