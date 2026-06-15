from game.animation.raptor_data import RAPTOR_ANIMATIONS, RAPTOR_ANIM_FPS
from game.entities.enemy import Enemy


class RaptorEnemy(Enemy):

    def __init__(self, x, y):
        super().__init__(
            x,
            y,
            enemy_type="raptor",
            animation_data=RAPTOR_ANIMATIONS,
            anim_fps=RAPTOR_ANIM_FPS,
            sprite_scale=4,
        )

        # properties special to current raptor enemy
        self.leap_cooldown = 0
        self.leap_speed = 12
        self.has_leaped_this_attack = False

    def update(self, player, enemies):
        if self.leap_cooldown > 0:
            self.leap_cooldown -= 1

        super().update(player, enemies)

    def choose_state(self, distance_x, distance_y):
        if self.state == self.ATTACK:
            return

        can_attack = (
            self.attack_cooldown <= 0
            and distance_x <= self.attack_range
            and distance_y <= self.attack_lane_range
        )

        if can_attack:
            self.state = self.ATTACK
            self.has_leaped_this_attack = False
        elif distance_x <= self.detect_range:
            self.state = self.CHASE
        else:
            self.state = self.PATROL

    def update_attack(self, player):
        if self.leap_cooldown <= 0 and not self.has_leaped_this_attack:
            self.leap_toward_player(player)
            self.leap_cooldown = 120
            self.has_leaped_this_attack = True

        super().update_attack(player)

        if self.state != self.ATTACK:
            self.has_leaped_this_attack = False

    def leap_toward_player(self, player):
        if player.x > self.x:
            self.facing_right = True
            self.x += self.leap_speed
        else:
            self.facing_right = False
            self.x -= self.leap_speed
