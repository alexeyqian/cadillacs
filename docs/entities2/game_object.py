
class GameObject:
    def __init__(self, entity_id, name):
        self.id = entity_id
        self.name = name
        self.tags = set()
        self.x = 0
        self.y = 0
        self.z_index = 0
        self.scale = 1
        self.width = 0
        self.height = 0
        self.active = True
        self.visible = True
        self.destroyed = False
        self._components = []

    def update(self):
        return None

    def draw(self):
        return None
    
    def add_tag(self, tag):
        pass
    
    def remove_tab(self, tag):
        pass
    
    def has_tab(self, tag):
        pass
    
    def add_component(self, component):
        pass
    def remove_component(self, component):
        pass
    def has_component(self, component):
        pass
    
    # lifecycle
    def on_spawn(self):
        pass
    def on_destroy(self):
        pass
    
    def __repr__(self) -> str:
        return f"{type(self).__name__}(id={self.id}, name={self.name})"
