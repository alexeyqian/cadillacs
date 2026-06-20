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
        self.leap_cooldown_duration = 120
        self.leap_startup_frames = 4
        self.leap_speed = 12
        self.has_leaped_this_attack = False

    def update(self, level, player, enemies):
        super().update(level, player, enemies)

    def advance_timers(self):
        if self.leap_cooldown > 0:
            self.leap_cooldown -= 1
        super().advance_timers()

    def start_attack(self):
        super().start_attack()
        self.has_leaped_this_attack = False

    def update_attack(self, level, player):
        if self.state != self.ATTACK:
            return

        if self.should_leap_now():
            self.leap_toward_player(player)
            self.leap_cooldown = self.leap_cooldown_duration
            self.has_leaped_this_attack = True

        super().update_attack(level, player)

        if self.state != self.ATTACK:
            self.has_leaped_this_attack = False

    def leap_toward_player(self, player):
        if player.x > self.x:
            self.facing_right = True
            self.x += self.leap_speed
        else:
            self.facing_right = False
            self.x -= self.leap_speed

    def should_leap_now(self):
        if self.leap_cooldown > 0:
            return False
        if self.has_leaped_this_attack:
            return False

        attack_windup = self.combat_controller.get_attack_data(self).windup
        leap_frame = max(0, attack_windup - self.leap_startup_frames)

        attack_timer = self.combat_controller.get_attack_timer(self)
        return attack_timer >= leap_frame
