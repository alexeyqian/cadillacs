import pygame

class Loot:
    def __init__(self, x, y, loot_type):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.loot_type = loot_type
        self.active = True

    def draw(self, screen, camera_x):
        if not self.active:
            return
        screen_x = self.x - camera_x
        if self.loot_type == "health":
            color = (0,255,0)
        elif self.loot_type == "ammo":
            color = (255,255,0)
        else:
            color = (255,255,255)

        # draw loot at screen coordinates
        pygame.draw.rect(screen, color, (screen_x, self.y, self.width, self.height))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

