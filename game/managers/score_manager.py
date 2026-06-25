from game.settings import PLAYER_EXTRA_LIFE_SCORE_BASE, PLAYER_EXTRA_LIFE_SCORE_STEP


class ScoreManager:
    _COMBO_TIMEOUT = 60
    _MAX_COMBO = 3

    def __init__(self):
        self.score = 0
        self.high_score = 0

        self._combo_count = 0
        self._combo_timer = 0

        self.next_extra_life_score = PLAYER_EXTRA_LIFE_SCORE_BASE
        self._extra_life_step = PLAYER_EXTRA_LIFE_SCORE_STEP

    # --- Public API ---

    def register_hit(self):
        self._combo_count = min(self._combo_count + 1, self._MAX_COMBO)
        self._combo_timer = self._COMBO_TIMEOUT

    def get_combo_score(self, base_points):
        return base_points * self._multiplier()

    def add_score(self, points):
        self.score += points
        if self.score > self.high_score:
            self.high_score = self.score

    def should_award_extra_life(self):
        return self.score >= self.next_extra_life_score

    def advance_extra_life_threshold(self):
        self.next_extra_life_score += self._extra_life_step

    def update(self):
        if self._combo_timer > 0:
            self._combo_timer -= 1
        else:
            self._combo_count = 0

    # --- Private ---

    def _multiplier(self):
        if self._combo_count >= 3:
            return 3
        if self._combo_count >= 2:
            return 2
        return 1
