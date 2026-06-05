import pygame
from game.entities.enemy import Enemy
from game.entities.boss_projectile import BossProjectile
from game.settings import *
from game.animation.animation_config import *

# boss phase system
# make boss behavior change as HP decreases
# Phase 1: normal boss
# Phase 2: faster attacks below 60% HP
# Phase 3: dangerous final phase below 30% HP
class BossEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x,y,
                        walk_config=BOSS_ENEMY_WALK,
                        attack_config=BOSS_ENEMY_ATTACK)
        
        self.max_hp = BOSS_ENEMY_MAX_HP
        self.hp = self.max_hp
        self.width = BOSS_ENEMY_W
        self.height = BOSS_ENEMY_H
        self.speed = BOSS_ENEMY_SPEED
        self.attack_damage = BOSS_ENEMY_ATTACK_DAMAGE
        self.attack_range = BOSS_ENEMY_HITBOX_W
        # special attack
        self.attack_cooldown_duration = 60
        self.special_attack_cooldown_duration = 300
        self.special_attack_cooldown = self.special_attack_cooldown_duration
        self.phase = 1
        self.phase_message_timer = 0
        self.pending_projectile = None

    def update(self, player, enemies):
        super().update(player, enemies)

        if self.state == self.DEAD:
            return

        self.update_phase()
        if self.phase_message_timer > 0:
            self.phase_message_timer -= 1

        if self.state == self.HIT:
            return

        if self.special_attack_cooldown > 0:
            self.special_attack_cooldown -= 1
        else:
            self.perform_special_attack(player)
            self.special_attack_cooldown = self.special_attack_cooldown_duration

    def draw(self, screen, camera_x):
        super().draw(screen, camera_x)

        screen_x = self.x - camera_x
        bar_y = self.y - 24
        hp_width = int(self.width * (self.hp / self.max_hp))
        pygame.draw.rect(screen, (60, 20, 60),
            (screen_x, bar_y, self.width, 10))
        pygame.draw.rect(screen, (255, 40, 40),
            (screen_x, bar_y, hp_width, 10))
        
        # phase warning messages
        font = pygame.font.SysFont(None, 24)
        phase_text = font.render(
            f"PHASE {self.phase}",True,(255, 255, 255))
        screen.blit(phase_text,(screen_x,self.y - 45))

        if self.phase_message_timer > 0:
            warning = font.render(
                f"BOSS PHASE {self.phase}!",True,(255, 0, 0))
            screen.blit(warning,(screen_x - 20,self.y - 70))

    def perform_special_attack(self, player):
        direction = 1
        if player.x < self.x:
            direction = -1

        damage = 30
        if self.phase == 2:
            damage = 45
        elif self.phase == 3:
            damage = 60

        self.pending_projectile = BossProjectile(
            self.x + self.width // 2,
            self.y + 40,
            direction,
            damage
        )

    def update_attack(self, player):
        if self.attack_cooldown > 0:
            return

        player.take_damage(self.attack_damage)
        self.attack_cooldown = self.attack_cooldown_duration
    
    # add better boss knockback resistance
    def take_damage(self, damage, attacker_x):
        if self.state == self.DEAD:
            return

        self.hp -= damage
        self.hit_timer = 8
        self.state = self.HIT

        # boss barely moves when hit
        if attacker_x < self.x:
            self.knockback_velocity = 3
        else:
            self.knockback_velocity = -3

        if self.hp <= 0:
            self.hp = 0
            self.state = self.DEAD

    def update_phase(self):
        hp_ratio = self.hp / self.max_hp
        old_phase = self.phase

        if hp_ratio <= 0.3:
            self.phase = 3
        elif hp_ratio <= 0.6:
            self.phase = 2
        else:
            self.phase = 1

        if self.phase != old_phase:
            self.phase_message_timer = 120

            if self.phase == 2:
                self.speed += 0.5
                self.attack_damage += 10
                self.attack_cooldown_duration = 45

            elif self.phase == 3:
                self.speed += 1
                self.attack_damage += 15
                self.attack_range += 40
                self.attack_cooldown_duration = 35
                self.special_attack_cooldown_duration = 120
                self.special_attack_cooldown = min(
                    self.special_attack_cooldown,
                    self.special_attack_cooldown_duration
                )
