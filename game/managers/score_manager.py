from game.settings import PLAYER_EXTRA_LIFE_SCORE_BASE
from game.settings import PLAYER_EXTRA_LIFE_SCORE_STEP
class ScoreManager:
    def __init__(self):
        self.score = 0
        self.high_score = 0
        # Combo Score Multiplier
        self.combo_count = 0
        self.combo_timer = 0
        self.combo_timeout = 60
        self.max_combo_count = 3
        
        self.next_extra_life_score = PLAYER_EXTRA_LIFE_SCORE_BASE
        self.extra_life_step = PLAYER_EXTRA_LIFE_SCORE_STEP
        
    def register_hit(self):
        self.combo_count = min(self.combo_count + 1, self.max_combo_count)
        self.combo_timer = self.combo_timeout
    
    def update(self):
        if self.combo_timer > 0:
            self.combo_timer -= 1
        else:
            self.combo_count = 0

    def get_multiplier(self):
        if self.combo_count >= 3:
            return 3
        if self.combo_count >= 2:
            return 2
        return 1
    
    def get_combo_score(self, base_points):
        multiplier = self.get_multiplier()
        points = base_points * multiplier
        return points

    def add_score(self, points):
        self.score += points
        
        if self.score > self.high_score:
            self.high_score = self.score
    
    def enemy_score(self, enemy):
        return enemy.score_points

    def object_score(self, obj):
        return 50
        
    def should_award_extra_life(self):
        return self.score >= self.next_extra_life_score
    
    def advance_extra_life_threshold(self):
        self.next_extra_life_score += self.extra_life_step
