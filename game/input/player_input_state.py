# Input edge flags
# stop the “hold attack to auto-combo” problem.
# expected gameplay for attack and attack combo:
# Hold J: one punch only
# Press J, release, press J: combo advances
# Mashing J: combo still works, but requires timing/input
class PlayerInputState:
    def __init__(self):
        self.attack_pressed = False
        self.jump_attack_pressed = False
        self.run_attack_requires_attack_release = False
