class PlayerInputTracker:
    """
    Persists input state across frames for the action controller.

    Edge flags (attack_pressed, jump_pressed, etc.) detect new key presses
    vs. held keys, preventing auto-repeat on hold.

    Frame counters (attack_frames, jump_frames) keep an input alive for a
    short window so a press slightly before the game can act still registers.
    """
    JUMP_BUFFER_FRAMES = 6
    ATTACK_BUFFER_FRAMES = 12

    def __init__(self):
        self.attack_pressed = False
        self.jump_pressed = False
        self.jump_attack_pressed = False
        self.run_attack_requires_attack_release = False
        self.jump_frames = 0
        self.attack_frames = 0

    def press_jump(self):
        self.jump_frames = self.JUMP_BUFFER_FRAMES

    def press_attack(self):
        self.attack_frames = self.ATTACK_BUFFER_FRAMES

    def has_jump(self):
        return self.jump_frames > 0

    def has_attack(self):
        return self.attack_frames > 0

    def consume_jump(self):
        self.jump_frames = 0

    def consume_attack(self):
        self.attack_frames = 0

    def advance_timers(self):
        if self.jump_frames > 0:
            self.jump_frames -= 1
        if self.attack_frames > 0:
            self.attack_frames -= 1
