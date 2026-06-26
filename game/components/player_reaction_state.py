class PlayerReactionState:
    def __init__(self, default_stun_frames):
        self.default_stun_frames = default_stun_frames
        self._hit_stun_remaining = 0
