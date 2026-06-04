import pygame
import random

from game.entities.loot import Loot

BOX_IMAGE = None

class BreakableObject:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.hp = 30
        self.destroyed = False
        self.loot_generated = False
    
    def draw(self, screen, camera_x):
        if self.destroyed:
            return
        screen_x = self.x - camera_x
        # try to draw box image if available
        global BOX_IMAGE
        if BOX_IMAGE is None:
            try:
                BOX_IMAGE = pygame.image.load("game/assets/objects/box.png").convert_alpha()
                BOX_IMAGE = pygame.transform.smoothscale(BOX_IMAGE, (self.width, self.height))
            except Exception:
                BOX_IMAGE = None
        if BOX_IMAGE:
            screen.blit(BOX_IMAGE, (screen_x, self.y))
            return
        pygame.draw.rect(screen, (150,90,40),
                (screen_x, self.y, self.width, self.height))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
            self.destroyed = True

    def create_loot(self):
        roll = random.randint(1,100)
        if roll <= 50:
            return Loot(self.x, self.y, "health")
        elif roll <= 80:
            return Loot(self.x, self.y, "ammo")
        
        # return None
        return Loot(self.x, self.y, "health")

