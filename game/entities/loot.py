import pygame
from game.colors import GREEN_COLOR, WHITE_COLOR, YELLOW_COLOR
from game.managers.asset_manager import AssetManager

LOOT_IMAGE_FILES = {
    "health": "game/assets/loot/health.png",
    "ammo": "game/assets/loot/ammo.png",
}

class Loot:
    def __init__(self, x, y, loot_type):
        self.x = x
        self.y = y
        self.width = 60
        self.height = 60
        self.loot_type = loot_type
        self.active = True
        self.image = None

    def load_image(self):
        filename = LOOT_IMAGE_FILES.get(self.loot_type)
        if filename is None:
            return None

        return AssetManager.load_image(filename, alpha=True)

    def draw(self, screen, camera_x):
        if not self.active:
            return
        screen_x = self.get_left() - camera_x
        screen_y = self.get_top()
        if self.image is None:
            self.image = self.load_image()

        if self.image:
            image = pygame.transform.scale(
                self.image,
                (self.width, self.height)
            )
            screen.blit(image, (screen_x, screen_y))
            return

        if self.loot_type == "health":
            color = GREEN_COLOR
        elif self.loot_type == "ammo":
            color = YELLOW_COLOR
        else:
            color = WHITE_COLOR

        # draw loot at screen coordinates
        pygame.draw.rect(screen, color, (screen_x, screen_y, self.width, self.height))

    def get_left(self):
        return self.x - self.width // 2
    
    def get_top(self):
        return self.y - self.height

    def get_rect(self):
        return pygame.Rect(self.get_left(), self.get_top(), self.width, self.height)
