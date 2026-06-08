from game.entities.enemy import Enemy
from game.entities.enemy_projectile import EnemyProjectile
from game.settings import *

class RangedEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)

        self.max_hp = RANGED_ENEMY_MAX_HP
        self.hp = self.max_hp
        self.attack_damage = RANGED_ENEMY_ATTACK_DAMAGE
        
        # properties special to ranged enemy
        self.pending_projectile = None
        self.shoot_cooldown = 0

    def update_attack(self, player):
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
            self.state = self.IDLE
            return

        #self.facing_right = player.x > self.x
        self.attack_timer += 1
        if (self.attack_timer == self.attack_windup
            and not self.attack_has_hit):
            direction = 1 if player.x > self.x else -1

            projectile = EnemyProjectile(self.x + self.width // 2, self.y + 30,
                                        direction, PROJECTILE_SPEED*0.7 self.attack_damage)
            self.pending_projectile = projectile
            self.attack_has_hit = True

        if self.attack_timer >= self.attack_total_duration:
            self.state = self.IDLE
            self.attack_timer = 0
            self.attack_has_hit = False
            self.shoot_cooldown = 90
