import random

from game.settings import PLAYER_SCREEN_EDGE_MARGIN, SCREEN_WIDTH


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

        if not level.camera_locked:
            self._keep_player_inside_view(player)

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
        left_limit, right_limit = self._get_player_view_limits(player)
        half_width = player.width // 2

        if player.x < left_limit:
            self.x = player.x - half_width - PLAYER_SCREEN_EDGE_MARGIN
        elif player.x > right_limit:
            self.x = player.x - SCREEN_WIDTH + half_width + PLAYER_SCREEN_EDGE_MARGIN

    def _keep_player_inside_view(self, player):
        left_limit, right_limit = self._get_player_view_limits(player)

        if player.x < left_limit:
            player.x = left_limit
        if player.x > right_limit:
            player.x = right_limit

    def _get_player_view_limits(self, player):
        half_width = player.width // 2
        left_limit = self.x + half_width + PLAYER_SCREEN_EDGE_MARGIN
        right_limit = self.x + SCREEN_WIDTH - half_width - PLAYER_SCREEN_EDGE_MARGIN
        return left_limit, right_limit

    def _clamp_to_world(self, world_width):
        max_scroll = max(0, world_width - SCREEN_WIDTH)
        self.x = max(0, min(self.x, max_scroll))

    def _apply_shake_offset(self, shake_active):
        if shake_active:
            self.x += random.randint(-self.shake_strength, self.shake_strength)
