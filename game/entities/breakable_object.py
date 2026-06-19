import random
import pygame
from game.managers.asset_manager import AssetManager
from game.entities.loot import Loot

class BreakableObject:
    def __init__(self, x, y, loot_type=None):
        self.x = x
        self.y = y
        self.width = 150
        self.height = 150
        self.hp = 10
        self.destroyed = False
        self.loot_generated = False
        self.box_image_file = "game/assets/objects/box.png"
        self.loot_type = loot_type
    
    def draw(self, screen, camera_x):
        if self.destroyed:
            return
        screen_x = self.get_left() - camera_x
        screen_y = self.get_top()
        box_image = AssetManager.load_scaled_image(self.box_image_file,
                        (self.width, self.height), alpha=True, smooth=True)

        if box_image:
            screen.blit(box_image, (screen_x, screen_y))
            return

        pygame.draw.rect(screen, (150,90,40),
                (screen_x, screen_y, self.width, self.height))

    def get_left(self):
        return self.x - self.width / 2

    def get_top(self):
        return self.y - self.height

    def get_rect(self):
        return pygame.Rect(self.get_left(), self.get_top(), self.width, self.height)

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
            self.destroyed = True

    def create_loot(self):
        if self.loot_type:
            return Loot(self.x, self.y, self.loot_type)

        roll = random.randint(1,100)
        if roll <= 50:
            return Loot(self.x, self.y, "health")
        elif roll <= 80:
            return Loot(self.x, self.y, "ammo")

        return Loot(self.x, self.y, "health")

