from game.settings import (
    ENEMY_FLANK_DECISION_DURATION,
    ENEMY_FLANK_OFFSET_X,
    ENEMY_FLANK_OFFSET_Y,
)


class EnemyFlankState:
    def __init__(self):
        self.target_side = None          # "left" or "right"; None when not flanking
        self._target_y_offset = 0
        self._offset_x = ENEMY_FLANK_OFFSET_X
        self._offset_y = ENEMY_FLANK_OFFSET_Y
        self._decision_remaining = 0
        self._decision_duration = ENEMY_FLANK_DECISION_DURATION

    def has_target(self):
        return self.target_side is not None

    def advance_timer(self):
        if self._decision_remaining > 0:
            self._decision_remaining -= 1

    def update(self, owner, player, enemies):
        if self._decision_remaining > 0 and self.target_side:
            return

        left_count = sum(
            1 for e in enemies
            if e is not owner
            and e.state not in [e.DEAD, e.GRABBED, e.THROWN, e.KNOCKDOWN]
            and e.x < player.x
        )
        right_count = sum(
            1 for e in enemies
            if e is not owner
            and e.state not in [e.DEAD, e.GRABBED, e.THROWN, e.KNOCKDOWN]
            and e.x >= player.x
        )

        self.target_side = "left" if left_count <= right_count else "right"
        same_side_count = left_count if self.target_side == "left" else right_count
        self._target_y_offset = -self._offset_y if same_side_count % 2 == 0 else self._offset_y
        self._decision_remaining = self._decision_duration

    def get_position(self, player):
        target_y = player.y + self._target_y_offset
        if self.target_side == "left":
            return player.x - self._offset_x, target_y
        return player.x + self._offset_x, target_y

    def clear(self):
        self.target_side = None
        self._target_y_offset = 0
        self._decision_remaining = 0
