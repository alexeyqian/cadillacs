import random

from game.entities.loot import Loot

# normal enemy: small chance health/ammo
# heavy enemy: higher chance health
# weapon enemy: chance to drop weapon
# boss enemy: guaranteed reward
class EnemyLootController:
    def __init__(self):
        self.loot_generated = False

    def create_loot(self, owner):
        roll = random.randint(1, 100)
        # todo: design a loot drop system
        # todo: only some configured enemy should drop loot, not every one.
        #if roll <= 30:
        #    return Loot(owner.x, owner.y, "health")

        #if roll <= 50:
        #    return Loot(owner.x, owner.y, "ammo")

        return None
