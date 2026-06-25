class AttackManager:
    def __init__(self):
        # Read externally
        self.current_attack_name = None
        self.current_attack = None
        self.elapsed_frames = 0
        self.has_connected = False
        # Internal hit tracking
        self._hit_targets = set()

    # --- State queries ---

    @property
    def is_attacking(self):
        return self.current_attack is not None

    @property
    def remaining_frames(self):
        if not self.current_attack:
            return 0
        return max(0, self.current_attack.total_duration - self.elapsed_frames)

    def is_active(self):
        if not self.current_attack:
            return False
        active_start = self.current_attack.windup
        active_end = active_start + self.current_attack.active
        return active_start <= self.elapsed_frames < active_end

    def can_hit_more_targets(self):
        if not self.current_attack:
            return False
        return len(self._hit_targets) < self.current_attack.max_targets

    def can_hit_target(self, target):
        return self.can_hit_more_targets() and id(target) not in self._hit_targets

    def has_hit_target(self, target):
        return id(target) in self._hit_targets

    def get_hit_count(self):
        return len(self._hit_targets)

    def get_max_targets(self):
        return self.current_attack.max_targets if self.current_attack else 0

    # --- Lifecycle ---

    def start(self, attack_name, attack_data):
        self.current_attack_name = attack_name
        self.current_attack = attack_data
        self.elapsed_frames = 0
        self.has_connected = False
        self._hit_targets = set()

    def advance(self):
        """Tick one frame. Returns True when the attack duration is complete."""
        if not self.current_attack:
            return False
        self.elapsed_frames += 1
        return self.elapsed_frames >= self.current_attack.total_duration

    def mark_target_hit(self, target):
        self._hit_targets.add(id(target))
        self.has_connected = True

    def finish(self):
        """Snapshot current state and reset. Returns (name, data, connected)."""
        snapshot = (self.current_attack_name, self.current_attack, self.has_connected)
        self.cancel()
        return snapshot

    def cancel(self):
        self.current_attack_name = None
        self.current_attack = None
        self.elapsed_frames = 0
        self.has_connected = False
        self._hit_targets = set()

    # --- Debug ---

    def get_phase_name(self):
        if not self.current_attack:
            return ""
        if self.elapsed_frames < self.current_attack.windup:
            return "WINDUP"
        active_end = self.current_attack.windup + self.current_attack.active
        if self.elapsed_frames < active_end:
            return "ACTIVE"
        if self.elapsed_frames < self.current_attack.total_duration:
            return "RECOVERY"
        return "DONE"

    def get_timing_label(self):
        if not self.current_attack:
            return ""
        return (
            f"{self.current_attack_name} "
            f"{self.get_phase_name()} "
            f"{self.elapsed_frames}/{self.current_attack.total_duration}"
        )
