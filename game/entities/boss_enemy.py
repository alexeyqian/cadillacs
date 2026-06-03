import pygame
from game.entities.enemy import Enemy
from game.settings import *

class BossEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x,y)
        
        self.max_hp = 500
        self.hp = 500
        self.width = 100
        self.height = 120
        self.speed = 1.5
        self.attack_damage = 20
        self.attack_range = BOSS_ENEMY_HITBOX_W
        # special attack
        self.special_attack_cooldown=300

    def update(self, player, enemies):
        super().update(player, enemies)

        if self.state == self.DEAD:
            return

        if self.special_attack_cooldown > 0:
            self.special_attack_cooldown -= 1
        else:
            self.perform_special_attack(player)
            self.special_attack_cooldown = 300

    def draw(self, screen, camera_x):
        screen_x = self.x - camera_x
        # shadow
        pygame.draw.ellipse(screen, (30,30,30),
            (screen_x, self.y+self.height-10,self.width,15))
        # boss body
        pygame.draw.rect(screen, (180,40,180),
            (screen_x, self.y, self.width, self.height))
        # hp bar
        pygame.draw.rect(screen, (120, 120,120),
            (screen_x, self.y-20,self.width,10))
        hp_width = int(100*self.hp/self.max_hp)
        pygame.draw.rect(screen, (255,0,0),
        (screen_x, self.y-20,hp_width,10))

    def perform_special_attack(self, player):
        player.take_damage(40)
    
    # add better boss knockback resistance
    def take_damage(self, damage, attacker_x):
        self.hp -= damage
        self.hit_timer = 8
        # boss barely moves when hit
        self.knockback_velocity *= 0.25
        if self.hp <= 0:
            self.hp = 0
            self.state = self.DEAD

