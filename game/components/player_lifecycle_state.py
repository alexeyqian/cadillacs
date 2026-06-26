class PlayerLifecycleState:
    def __init__(self, respawn_x, respawn_y, lives):
        self.lives = lives
        self.respawn_x = respawn_x
        self.respawn_y = respawn_y
        self.respawn_remaining = 0
