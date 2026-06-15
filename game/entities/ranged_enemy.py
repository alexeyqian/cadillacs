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
        self.shoot_cooldown = 0
        self.shot_fired = False

    def update_attack(self, player):
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
            self.state = self.PATROL
            return

        self.face_player(player)

        # when attack animation reaches middle frame, fire projectile
        # when attack animation reaches final frame, leave attack state
        animation = self.animation_controller.get_current_animation()
        middle_frame = len(animation.frames) // 2

        if animation.current_frame >= middle_frame and not self.shot_fired:
            direction = 1 if player.x > self.x else -1

            self.pending_projectile = EnemyProjectile(
                self.x, self.y - 60, direction,
                PROJECTILE_SPEED * 0.7, self.attack_damage)

            self.shot_fired = True
            self.attack_already_hit = True

        if animation.current_frame == len(animation.frames) - 1:
            self.state = self.PATROL
            self.shot_fired = False
            self.attack_already_hit = False
            self.shoot_cooldown = self.attack_cooldown_duration