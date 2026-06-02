from game.settings import *
class Camera:
    def __init__(self):
        self.x = 0

# Runs every frame to keep the camera centered on the player.
    def update(self, player):
        target_x = player.x - SCREEN_WIDTH // 2
        self.x = target_x
        self.x = max(0, self.x)
        self.x = min(self.x, WORLD_WIDTH - SCREEN_WIDTH)

