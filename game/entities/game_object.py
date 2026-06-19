class GameObject:
    def __init__(self, x=0, y=0, width=0, height=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.active = True
        self.visible = True

    def update(self, *args, **kwargs):
        pass

    def draw(self, *args, **kwargs):
        pass
