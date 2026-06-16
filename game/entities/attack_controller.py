class AttackController:
    def __init__(self):
        self.current_attack_name = None
        self.current_attack = None
        self.attack_timer = 0
        self.attack_connected = False
        self.hit_targets = set()

    @property
    def is_attacking(self):
        return self.current_attack is not None

    @property
    def attack_remaining(self):
        if not self.current_attack:
            return 0
        return max(0, self.get_attack_duration() - self.attack_timer)

    def start_attack(self, attack_name, attack_data):
        self.current_attack_name = attack_name
        self.current_attack = attack_data
        self.attack_timer = 0
        self.attack_connected = False
        self.hit_targets = set()

    def update_attack_timer(self):
        if not self.current_attack:
            return False

        self.attack_timer += 1
        return self.is_finished()

    def is_finished(self):
        if not self.current_attack:
            return False
        return self.attack_timer >= self.get_attack_duration()

    def is_active(self):
        if not self.current_attack:
            return False
        if not self.has_attack_phases():
            return True

        active_start = self.current_attack.windup
        active_end = self.current_attack.windup + self.current_attack.active
        return active_start <= self.attack_timer < active_end

    def get_phase_name(self):
        if not self.current_attack:
            return ""
        if not self.has_attack_phases():
            return "ACTIVE"

        if self.attack_timer < self.current_attack.windup:
            return "WINDUP"

        active_end = self.current_attack.windup + self.current_attack.active
        if self.attack_timer < active_end:
            return "ACTIVE"

        if self.attack_timer < self.get_attack_duration():
            return "RECOVERY"

        return "DONE"

    def get_timing_label(self):
        if not self.current_attack:
            return ""

        return (
            f"{self.current_attack_name} "
            f"{self.get_phase_name()} "
            f"{self.attack_timer}/{self.get_attack_duration()}"
        )

    def mark_connected(self):
        self.attack_connected = True

    def has_hit_target(self, target):
        return id(target) in self.hit_targets

    def mark_target_hit(self, target):
        self.hit_targets.add(id(target))
        self.mark_connected()

    def finish_attack(self):
        finished_attack_name = self.current_attack_name
        finished_attack = self.current_attack
        attack_connected = self.attack_connected
        self.cancel_attack()
        return finished_attack_name, finished_attack, attack_connected

    def cancel_attack(self):
        self.current_attack_name = None
        self.current_attack = None
        self.attack_timer = 0
        self.attack_connected = False
        self.hit_targets = set()

    def get_attack_duration(self):
        if not self.current_attack:
            return 0
        return self.current_attack.duration

    def has_attack_phases(self):
        return all(
            hasattr(self.current_attack, field_name)
            for field_name in ["windup", "active", "recovery"]
        )
