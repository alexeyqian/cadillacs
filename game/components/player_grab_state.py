from game.settings import PLAYER_GRAB_KNEE_DURATION, PLAYER_GRAB_KNEE_HIT_FRAME, PLAYER_GRAB_RANGE


class PlayerGrabState:
    def __init__(self):
        self.grabbed_enemy = None
        self.grab_range = PLAYER_GRAB_RANGE
        self.failed_grab_recovery_duration = 8

        self.throw_remaining = 0
        self.throw_duration = 14

        self.grab_knee_remaining = 0
        self.grab_knee_duration = PLAYER_GRAB_KNEE_DURATION
        self.grab_knee_hit_frame = PLAYER_GRAB_KNEE_HIT_FRAME
