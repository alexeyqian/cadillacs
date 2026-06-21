class ComponentBase:
    def __init__(self, owner=None):
        self.owner = owner
        self.enabled = True

    def on_start(self):
        pass
    
    def on_destroyed(self):
        pass
    
    def update(self, dt: float) -> None:
        pass