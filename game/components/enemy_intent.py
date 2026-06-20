class EnemyIntent:
    NONE = "none"
    PATROL = "patrol"
    MOVE_TOWARD_PLAYER = "move_toward_player"
    ATTACK_PLAYER = "attack_player"
    FLANK = "flank"

    def __init__(self):
        self.clear()

    def clear(self):
        self.action = self.NONE
        self.flank_position = None

    def patrol(self):
        self.clear()
        self.action = self.PATROL

    def move_toward_player(self):
        self.clear()
        self.action = self.MOVE_TOWARD_PLAYER

    def attack_player(self):
        self.clear()
        self.action = self.ATTACK_PLAYER

    def flank_to(self, position):
        self.clear()
        self.action = self.FLANK
        self.flank_position = position

    def wants_patrol(self):
        return self.action == self.PATROL

    def wants_move_toward_player(self):
        return self.action == self.MOVE_TOWARD_PLAYER

    def wants_attack_player(self):
        return self.action == self.ATTACK_PLAYER

    def wants_flank(self):
        return self.action == self.FLANK
