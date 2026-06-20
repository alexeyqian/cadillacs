import random

from game.settings import PLAYER_SCREEN_EDGE_MARGIN, SCREEN_WIDTH


class Camera:
    def __init__(self):
        self.x = 0
        self.shake_timer = 0
        self.shake_strength = 0

    def clamp_to_world(self, world_width):
        max_scroll = max(0, world_width - SCREEN_WIDTH)
        self.x = max(0, min(self.x, max_scroll))

    # Runs every frame to keep the player inside the camera follow area.
    def update(self, player, world_width, lock_x = None):
        # for arena lock support
        if lock_x is not None:
            self.x = lock_x
            self.clamp_to_world(world_width)
            return

        # Use a dead zone instead of re-centering every frame. This keeps
        # camera.x stable when an arena lock is released after a wave clears.
        half_w = player.width // 2
        left_limit = self.x + half_w + PLAYER_SCREEN_EDGE_MARGIN
        right_limit = self.x + SCREEN_WIDTH - half_w - PLAYER_SCREEN_EDGE_MARGIN

        if player.x < left_limit:
            self.x = player.x - half_w - PLAYER_SCREEN_EDGE_MARGIN
        elif player.x > right_limit:
            self.x = player.x - SCREEN_WIDTH + half_w + PLAYER_SCREEN_EDGE_MARGIN

        self.clamp_to_world(world_width)

        if self.shake_timer > 0:
            self.shake_timer -= 1
            self.x += random.randint(-self.shake_strength, self.shake_strength)
        
    def shake(self, strength, duration):
        self.shake_strength = max(self.shake_strength, strength)
        self.shake_timer = max(self.shake_timer, duration)
