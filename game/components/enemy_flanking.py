from game.settings import (
    ENEMY_FLANK_DECISION_DURATION,
    ENEMY_FLANK_OFFSET_X,
    ENEMY_FLANK_OFFSET_Y,
)


class EnemyFlanking:
    def __init__(self):
        #  if an enemy is in range but cannot attack because another melee enemy owns the slot, 
        # it should reposition toward an open side instead of just pressing into the player. 
        # This makes groups look more intentional.
        self.target_side = None
        self.target_y_offset = 0
        self.offset_x = ENEMY_FLANK_OFFSET_X
        self.offset_y = ENEMY_FLANK_OFFSET_Y
        # avoid make enemies jitter between left/right if counts are close. 
        # give each flank decision a short commitment timer.
        self.decision_remaining = 0
        self.decision_duration = ENEMY_FLANK_DECISION_DURATION

    def has_target(self):
        return self.target_side is not None

    def advance_timers(self):
        if self.decision_remaining > 0:
            self.decision_remaining -= 1

    def set_target(self, owner, player, enemies):
        if self.decision_remaining > 0 and self.target_side:
            return

        left_count = 0
        right_count = 0

        for enemy in enemies:
            if enemy is owner:
                continue
            if enemy.state in [enemy.DEAD, enemy.GRABBED, enemy.THROWN, enemy.KNOCKDOWN]:
                continue

            if enemy.x < player.x:
                left_count += 1
            else:
                right_count += 1

        if left_count <= right_count:
            self.target_side = "left"
        else:
            self.target_side = "right"

        same_side_count = left_count if self.target_side == "left" else right_count
        if same_side_count % 2 == 0:
            self.target_y_offset = -self.offset_y
        else:
            self.target_y_offset = self.offset_y

        self.decision_remaining = self.decision_duration

    def clear_target(self):
        self.target_side = None
        self.target_y_offset = 0
        self.decision_remaining = 0

    def get_target_position(self, player):
        target_y = player.y + self.target_y_offset
        if self.target_side == "left":
            return player.x - self.offset_x, target_y

        return player.x + self.offset_x, target_y
