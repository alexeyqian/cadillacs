class EnemyIntent:
    NONE = "none"
    PATROL = "patrol"
    MOVE_TOWARD_PLAYER = "move_toward_player"
    RUN_TOWARD_PLAYER = "run_toward_player"
    RUN_ATTACK = "run_attack"
    JUMP = "jump"
    JUMP_ATTACK = "jump_attack"
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

    def run_toward_player(self):
        self.clear()
        self.action = self.RUN_TOWARD_PLAYER

    def jump(self):
        self.clear()
        self.action = self.JUMP

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

    def wants_run_toward_player(self):
        return self.action == self.RUN_TOWARD_PLAYER

    def wants_jump(self):
        return self.action == self.JUMP

    def run_attack(self):
        self.clear()
        self.action = self.RUN_ATTACK

    def wants_run_attack(self):
        return self.action == self.RUN_ATTACK

    def jump_attack(self):
        self.clear()
        self.action = self.JUMP_ATTACK

    def wants_jump_attack(self):
        return self.action == self.JUMP_ATTACK

    def wants_attack_player(self):
        return self.action == self.ATTACK_PLAYER

    def wants_flank(self):
        return self.action == self.FLANK
