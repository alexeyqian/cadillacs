class StageManager:
    def __init__(self, stages, start_stage_id=None):
        self.stages = stages
        self.current_stage_index = self.find_stage_index(start_stage_id)

    def find_stage_index(self, stage_id):
        if stage_id is None:
            return 0

        for index, stage in enumerate(self.stages):
            if stage["id"] == stage_id:
                return index

        raise ValueError(f"Unknown start stage id: {stage_id}")
        
    def get_current_stage(self):
        return self.stages[self.current_stage_index]
    
    def has_next_stage(self):
        return self.current_stage_index + 1 < len(self.stages)
    
    def advance_stage(self):
        if self.has_next_stage():
            self.current_stage_index += 1
            return self.get_current_stage()
        return None
