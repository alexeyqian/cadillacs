class StageClearManager:
    def __init__(self):
        self.active = False
        self.life_bonus = 0
        self.score_bonus = 0
        self.total_bonus = 0
        self.timer = 0

    def activate(self, player):
        self.active = True
        # bonus are just points
        self.life_bonus = player.health.lives*1000
        self.score_bonus = 1500
        self.total_bonus = self.life_bonus + self.score_bonus
        self.timer = 100

    def update(self):
        if not self.active:
            return
        if self.timer > 0:
            self.timer -= 1
            
    
