class ScoreManager:
    def __init__(self):
        self.score = 0
        self.high_score = 0
        # Combo Score Multiplier
        self.combo_count = 0
        self.combo_timer = 0
        self.combo_timeout = 120
        
        self.next_extra_life_score = 5000
        self.extra_life_step = 10000
        
    def register_hit(self):
        self.combo_count += 1
        self.combo_timer = self.combo_timeout
    
    def update(self):
        if self.combo_timer > 0:
            self.combo_timer -= 1
        else:
            self.combo_count = 0

    def get_multiplier(self):
        if self.combo_count >= 8:
            return 4
        if self.combo_count >= 5:
            return 3
        if self.combo_count >= 3:
            return 2
        return 1
    
    def get_combo_score(self, base_points):
        multiplier = self.get_multiplier()
        points = base_points * multiplier
        return points
    
    # deprecated
    def add_combo_score(self, base_points):
        points = self.get_combo_score(base_points)
        self.add_score(points)
        return points

    def add_score(self, points):
        self.score += points
        
        if self.score > self.high_score:
            self.high_score = self.score
    
    def enemy_score(self, enemy):
        if hasattr(enemy, "score_points"):
            return enemy.score_points

        name = enemy.__class__.__name__
        if name == "FastEnemy":
            return 200

        if name == "HeavyEnemy":
            return 300

        if name == "RangedEnemy":
            return 250

        if name == "BossEnemy":
            return 2000

        if name == "RaptorEnemy":
            return 400

        return 100
    
    def add_enemy_kill_score(self, enemy):
        self.add_score(
            self.enemy_score(enemy)
        )

    def object_score(self, obj):
        return 50

    def add_breakable_score(self, obj):
        points = self.object_score(obj)
        self.add_score(points)
        
    def should_award_extra_life(self):
        return self.score >= self.next_extra_life_score
    
    def advance_extra_life_threshold(self):
        self.next_extra_life_score += self.extra_life_step
