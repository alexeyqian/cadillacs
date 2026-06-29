import random

from game.settings import SCREEN_WIDTH

# It captures the camera's current x at the exact moment the wave fires, 
# clamped so it doesn't scroll past the world boundary. 
# There is no direct arithmetic from trigger_x — the lock position is 
# wherever the camera happens to be when the player crosses the trigger.

# Camera locks on each update, if level.camera_locked is True, 
# the camera calls _move_to_lock(level.lock_x) which sets self.x = lock_x 
# and stops following the player.

# Arena bounds uses level.lock_x directly as arena_left, 
# and lock_x + SCREEN_WIDTH as arena_right.
class Camera:
    def __init__(self):
        self.x = 0
        self.shake_timer = 0
        self.shake_strength = 0

    def update(self, player, level):
        shake_active = self._advance_shake_timer()

        if level.camera_locked:
            self._move_to_lock(level.lock_x)
        else:
            self._follow_player(player)

        self._clamp_to_world(level.world_width)
        self._apply_shake_offset(shake_active)

    def shake(self, strength, duration):
        self.shake_strength = max(self.shake_strength, strength)
        self.shake_timer = max(self.shake_timer, duration)

    def _advance_shake_timer(self):
        shake_active = self.shake_timer > 0
        if shake_active:
            self.shake_timer -= 1
        return shake_active

    def _move_to_lock(self, lock_x):
        if lock_x is not None:
            self.x = lock_x

    def _follow_player(self, player):
        self.x = player.x - SCREEN_WIDTH // 2

    def _clamp_to_world(self, world_width):
        max_scroll = max(0, world_width - SCREEN_WIDTH)
        self.x = max(0, min(self.x, max_scroll))

    def _apply_shake_offset(self, shake_active):
        if shake_active:
            self.x += random.randint(-self.shake_strength, self.shake_strength)
