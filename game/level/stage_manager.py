class StageManager:
    def __init__(self, stages):
        self.stages = stages
        self.current_stage_index = 0
        
    def get_current_stage(self):
        return self.stages[self.current_stage_index]
    
    def has_next_stage(self):
        return self.current_stage_index + 1 < len(self.stages)
    
    def advance_stage(self):
        if self.has_next_stage():
            self.current_stage_index += 1
            return self.get_current_stage()
        return None