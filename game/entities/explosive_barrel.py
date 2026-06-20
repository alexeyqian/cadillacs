from game.entities.breakable_object import BreakableObject

class ExplosiveBarrel(BreakableObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.width = 120
        self.height = 160
        self.hp = 30
        self.explosive = True
