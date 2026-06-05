class ScoreManager:
    def __init__(self):
        self.score = 0
        self.high_score = 0
        
    def add_score(self, points):
        self.score += points
        
        if self.score > self.high_score:
            self.high_score = self.score
    
    def enemy_score(self, enemy):
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