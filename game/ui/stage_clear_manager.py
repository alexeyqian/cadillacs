class StageClearManager:
    def __init__(self):
        self.active = False
        self.life_bonus = 0
        self.score_bonus = 0
        self.total_bonus = 0
        self.timer = 0
        self.bonus_applied = False

    def activate(self, player):
        self.active = True
        # bonus are just points
        self.life_bonus = player.lives*1000
        self.score_bonus = 1500
        self.total_bonus = self.life_bonus + self.score_bonus
        self.timer = 100
        self.bonus_applied = False

    def apply_bonus(self, score_manager):
        if self.bonus_applied:
            return
        score_manager.add_score(self.total_bonus)
        self.bonus_applied = True

    def update(self):
        if not self.active:
            return
        if self.timer > 0:
            self.timer -= 1
            
    