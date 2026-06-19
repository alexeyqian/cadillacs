from game.settings import PROJECTILE_SPEED
from game.entities.projectile import Projectile


class PlayerWeaponSlot:
    def __init__(self):
        self.weapon = None
        self.fire_pressed = False
        self.drop_pressed = False

    def pick_up(self, weapon):
        self.weapon = weapon
        weapon.picked_up = True

    def drop(self, owner):
        if self.weapon is None:
            return

        self.weapon.picked_up = False
        self.weapon.x = owner.x - 80
        self.weapon.y = owner.y + 80
        self.weapon = None

    def fire(self, owner):
        if self.weapon is None:
            return
        if not self.weapon.is_ranged:
            return
        if self.weapon.ammo <= 0:
            return

        direction = 1
        if not owner.facing_right:
            direction = -1

        muzzle_x = owner.x + (40 if owner.facing_right else -40)
        muzzle_y = owner.get_top() + 105

        projectile = Projectile(
            muzzle_x,
            muzzle_y,
            direction,
            PROJECTILE_SPEED,
            self.weapon.damage
        )
        owner.events.emit("spawn_projectile", projectile)
        self.weapon.ammo -= 1