from game.entities.enemy import Enemy
from game.entities.enemy_config import get_enemy_config
from game.entities.enemy_projectile import EnemyProjectile
from game.settings import *

class RangedEnemy(Enemy):
    def __init__(self, x, y, enemy_type="ranged"):
        super().__init__(x, y, enemy_config=get_enemy_config(enemy_type))
        
        # properties special to ranged enemy
        self.pending_projectile = None
        self.shoot_cooldown = 0

    def update_attack(self, player):
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
            self.state = self.IDLE
            return

        self.face_player(player)
        self.attack_timer += 1
        if (self.attack_timer == self.attack_windup
            and not self.attack_has_hit):
            direction = 1 if player.x > self.x else -1

            projectile = EnemyProjectile(self.x, self.get_top()+90,
                                        direction, PROJECTILE_SPEED*0.7, self.attack_damage)
            self.pending_projectile = projectile
            self.attack_has_hit = True

        if self.attack_timer >= self.attack_total_duration:
            self.state = self.IDLE
            self.attack_timer = 0
            self.attack_has_hit = False
            self.shoot_cooldown = 90
