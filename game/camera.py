from game.settings import *
import random

class Camera:
    def __init__(self):
        self.x = 0
        self.shake_timer = 0
        self.shake_strength = 0

    # Runs every frame to keep the camera centered on the player.
    def update(self, player, world_width, lock_x = None):
        # for arena lock support
        if lock_x is not None:
            self.x = lock_x
            return

        # camera follows player, tries to keep player near center of screen
        target_x = player.x - SCREEN_WIDTH // 2
        self.x = target_x
        self.x = max(0, self.x)
        
        #self.x = min(self.x, world_width - SCREEN_WIDTH)
        # This matters because Stage 3 is only 652 wide, smaller than SCREEN_WIDTH
        max_scroll = max(0, world_width - SCREEN_WIDTH)
        self.x = min(self.x, max_scroll)

        if self.shake_timer > 0:
            self.shake_timer -= 1
            self.x += random.randint(-self.shake_strength, self.shake_strength)
        
    def shake(self, strength, duration):
        self.shake_strength = max(self.shake_strength, strength)
        self.shake_timer = max(self.shake_timer, duration)

