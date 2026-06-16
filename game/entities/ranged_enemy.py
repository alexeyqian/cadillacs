from game.animation.ferris_data import FERRIS_ANIMATIONS, FERRIS_ANIM_FPS
from game.entities.enemy import Enemy
from game.entities.enemy_projectile import EnemyProjectile
from game.settings import PROJECTILE_SPEED

class RangedEnemy(Enemy):
    def __init__(self, x, y, enemy_type="ranged"):
        super().__init__(x, y,
            enemy_type=enemy_type,
            animation_data=FERRIS_ANIMATIONS,
            anim_fps=FERRIS_ANIM_FPS,
            sprite_scale=4,
        )

        # properties special to ranged enemy
        self.pending_projectile = None
        self.shot_fired = False

    def start_attack(self):
        super().start_attack()
        self.shot_fired = False

    def update_attack(self, level, player):
        self.face_player(player)
        self.attack_timer += 1

        if self.is_attack_active() and not self.shot_fired:
            direction = 1 if player.x > self.x else -1

            self.pending_projectile = EnemyProjectile(
                self.x,
                self.y - 60,
                direction,
                PROJECTILE_SPEED * 0.7,
                self.attack_damage,
                lane_y=self.y,
            )

            self.shot_fired = True
            self.attack_already_hit = True

        if self.attack_timer >= self.get_attack_total_duration():
            self.state = self.PATROL
            self.attack_timer = 0
            self.shot_fired = False
            self.attack_already_hit = False
            self.has_attack_slot = False
            self.attack_cooldown = self.attack_cooldown_duration
