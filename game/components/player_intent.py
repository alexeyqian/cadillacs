class PlayerIntent:
    def __init__(self):
        self.clear()

    def clear(self):
        self.jump_requested = None
        self.attack_requested = False

    def jump(self, player_input):
        self.jump_requested = player_input

    def attack(self):
        self.attack_requested = True

    def wants_jump(self):
        return self.jump_requested is not None

    def wants_attack(self):
        return self.attack_requested

    def clear_jump(self):
        self.jump_requested = None

    def clear_attack(self):
        self.attack_requested = False
