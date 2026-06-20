class PlayerIntent:
    def __init__(self):
        self.clear()

    def clear(self):
        self.jump_input = None
        self.attack_requested = False
        self.fire_requested = False

    def jump(self, player_input):
        self.jump_input = player_input

    def attack(self):
        self.attack_requested = True

    def fire(self):
        self.fire_requested = True

    def wants_jump(self):
        return self.jump_input is not None

    def wants_attack(self):
        return self.attack_requested

    def wants_fire(self):
        return self.fire_requested

    def clear_jump(self):
        self.jump_input = None

    def clear_attack(self):
        self.attack_requested = False

    def clear_fire(self):
        self.fire_requested = False
