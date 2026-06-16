import pygame
from game.settings import *
from game.colors import *

from game.entities.enemy import Enemy
from game.entities.enemy_projectile import EnemyProjectile
from game.animation.animation_config import *
from game.animation.boss_data import BOSS_ANIMATIONS, BOSS_ANIM_FPS

# boss phase system
# make boss behavior change as HP decreases
# Phase 1: normal boss
# Phase 2: faster attacks below 60% HP
# Phase 3: dangerous final phase below 30% HP
class BossEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(
            x,
            y,
            enemy_type="boss",
            animation_data=BOSS_ANIMATIONS,
            anim_fps=BOSS_ANIM_FPS,
            sprite_scale=4
        )

        self.health.max_hp = BOSS_ENEMY_MAX_HP
        self.health.hp = self.health.max_hp
        self.speed = BOSS_ENEMY_SPEED

        # properties special to boss enemy
        self.special_attack_cooldown_duration = 300
        self.special_attack_cooldown = self.special_attack_cooldown_duration
        self.phase = 1
        self.phase_message_remaining = 0
        self.phase_message = ""

        self.base_speed = self.speed
        self.base_attack_damage = self.attack_damage
        self.base_attack_range = self.attack_range
        self.base_attack_lane_range = self.attack_lane_range
        self.base_attack_cooldown_duration = self.attack_cooldown_duration
        self.base_special_attack_cooldown_duration = self.special_attack_cooldown_duration

        self.pending_projectile = None

    def update(self, level, player, enemies):
        super().update(level, player, enemies)

        if self.state == self.DEAD:
            return
        if self.state == self.HIT:
            return

        self.update_phase()
        if self.phase_message_remaining > 0:
            self.phase_message_remaining -= 1

        if self.special_attack_cooldown > 0:
            self.special_attack_cooldown -= 1
        else:
            self.perform_special_attack(player)
            self.special_attack_cooldown = self.special_attack_cooldown_duration

    def draw(self, screen, camera_x):
        super().draw(screen, camera_x)

        screen_x = self.x - camera_x
        bar_width = self.collision_box_w
        bar_x = int(screen_x - bar_width / 2)
        bar_y = self.y - 24
        hp_width = int(bar_width * (self.health.hp / self.health.max_hp))
        pygame.draw.rect(screen, (60, 20, 60),
            (bar_x, bar_y, bar_width, 10))
        pygame.draw.rect(screen, (255, 40, 40),
            (bar_x, bar_y, hp_width, 10))
        
        # phase warning messages
        font = pygame.font.SysFont(None, 24)
        phase_text = font.render(
            f"PHASE {self.phase}",True,(255, 255, 255))
        screen.blit(phase_text,(screen_x,self.y - 45))

        if self.phase_message_remaining > 0:
            warning = font.render(self.phase_message, True, (255, 0, 0))
            screen.blit(warning, (screen_x - 60, self.y - 70))

    def perform_special_attack(self, player):
        direction = 1
        if player.x < self.x:
            direction = -1

        damage = self.attack_damage
        if self.phase == 2:
            damage *= 2
        elif self.phase == 3:
            damage *= 3

        self.pending_projectile = EnemyProjectile(
            self.x - 15,
            self.get_top() + 120,
            direction,
            self.speed * 2,
            damage,
            lane_reach=1,
            width=30,
            height=15,
            shape="ellipse",
        )

    def take_damage(self, damage, attacker_x):
        if self.state == self.DEAD:
            return

        died = self.health.take_damage(damage)

        should_flinch = damage >= self.flinch_damage_threshold
        if died:
            should_flinch = True

        if should_flinch:
            self.hit_stun_remaining = 8
            self.state = self.HIT

            # boss barely moves when hit
            if attacker_x < self.x:
                self.knockback_velocity = 3
            else:
                self.knockback_velocity = -3

        if died:
            self.state = self.DEAD

    def update_phase(self):
        hp_ratio = self.health.hp / self.health.max_hp
        old_phase = self.phase

        if hp_ratio <= 0.3:
            self.phase = 3
        elif hp_ratio <= 0.6:
            self.phase = 2
        else:
            self.phase = 1

        if self.phase != old_phase:
            if self.phase != old_phase:
                self.apply_phase_stats()
                
    def apply_phase_stats(self):
        self.phase_message_remaining = 120

        if self.phase == 1:
            self.phase_message = "BOSS PHASE 1"
            self.flinch_damage_threshold = FIST_DAMAGE + 4
            self.speed = self.base_speed
            self.attack_damage = self.base_attack_damage
            self.attack_range = self.base_attack_range
            self.attack_lane_range = self.base_attack_lane_range
            self.attack_cooldown_duration = self.base_attack_cooldown_duration
            self.special_attack_cooldown_duration = self.base_special_attack_cooldown_duration

        elif self.phase == 2:
            self.phase_message = "BOSS ENRAGED"
            self.flinch_damage_threshold = FIST_DAMAGE + 8
            self.speed = self.base_speed + 0.5
            self.attack_damage = self.base_attack_damage + 6
            self.attack_range = self.base_attack_range
            self.attack_lane_range = self.base_attack_lane_range
            self.attack_cooldown_duration = 45
            self.special_attack_cooldown_duration = self.base_special_attack_cooldown_duration

        elif self.phase == 3:
            self.phase_message = "FINAL PHASE"
            self.flinch_damage_threshold = FIST_DAMAGE * 2
            self.speed = self.base_speed + 1
            self.attack_damage = self.base_attack_damage + 10
            self.attack_range = self.base_attack_range + 50
            self.attack_lane_range = self.base_attack_lane_range + 50
            self.attack_cooldown_duration = 60
            self.special_attack_cooldown_duration = 120

        self.special_attack_cooldown = min(
            self.special_attack_cooldown,
            self.special_attack_cooldown_duration
        )
