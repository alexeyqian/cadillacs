class InputBuffer:
    """
    InputBuffer solves a real problem — input leniency. 
    Without it, if you press jump or attack on frame N but the game can't act until frame N+1 (mid-attack recovery, etc.), 
    the press is silently lost. 
    The buffer keeps the press alive for a few frames so it fires as soon as possible.

    It's used for exactly two actions:
    Jump: 6-frame window — lets the jump register even if pressed slightly early
    Attack: 12-frame window — lets combo inputs queue up during recovery frames
    This is correct and necessary for the game to feel responsive. 
    Removing it would make attacks feel sluggish and jumps miss inputs regularly — a known pain point in beat-em-ups.
    """
    def __init__(self):
        self.jump_frames = 0
        self.attack_frames = 0

    def press_jump(self, frames):
        self.jump_frames = frames

    def press_attack(self, frames):
        self.attack_frames = frames

    def has_jump(self):
        return self.jump_frames > 0

    def has_attack(self):
        return self.attack_frames > 0

    def consume_jump(self):
        self.jump_frames = 0

    def consume_attack(self):
        self.attack_frames = 0

    def update(self):
        if self.jump_frames > 0:
            self.jump_frames -= 1
        if self.attack_frames > 0:
            self.attack_frames -= 1
