from game.entities.enemy import Enemy
from game.animation.animation_config import *
from game.assets.placeholder.enemy_frames import create_raptor_frames


class RaptorEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(
            x,
            y,
            walk_config=RAPTOR_ENEMY_WALK,
            attack_config=RAPTOR_ENEMY_ATTACK,
            fallback_frame_factory=create_raptor_frames
        )

        self.max_hp = 90
        self.hp = self.max_hp
        self.width = 70
        self.height = 60
        self.speed = 5
        self.attack_damage = 14
        self.attack_range = 70
        self.detect_range = 420
        self.lunge_distance = 28

    def update_attack(self, player):
        if self.attack_cooldown > 0:
            return

        direction = 1
        if player.x < self.x:
            direction = -1

        # The raptor briefly lunges during its bite, making it feel different
        # from the human enemies without adding a complicated state machine.
        self.x += direction * self.lunge_distance
        player.take_damage(self.attack_damage)
        self.attack_cooldown = 75
