from game.entities.enemy import Enemy
from game.entities.enemy_projectile import EnemyProjectile
from game.settings import *

class RangedEnemy(Enemy):

    def __init__(self, x, y):
        super().__init__(x, y)

        self.max_hp = RANGED_ENEMY_MAX_HP
        self.hp = self.max_hp

        self.attack_damage = RANGED_ENEMY_ATTACK_DAMAGE
        self.pending_projectile = None
        self.attack_range = RANGED_ENEMY_ATTACK_RANGE
        self.shoot_cooldown = 0

    def update_attack(self, player):
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
            return

        direction = -1
        if player.x > self.x:
            direction = 1

        projectile = EnemyProjectile(self.x + self.width // 2,
            self.y + 30, direction, self.attack_damage)
        self.pending_projectile = projectile
        self.shoot_cooldown = 90

