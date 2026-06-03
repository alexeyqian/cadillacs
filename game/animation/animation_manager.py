class AnimationManager:
    def __init__(self):
        self.animations = {}
        self.current_name = None
        self.current_animation = None

    def add_animation(self, name, animation):
        self.animations[name] = animation
        if self.current_animation is None:
            self.current_name = name
            self.current_animation = animation
    
    def play(self, name):
        if name == self.current_name:
            return
        self.current_name = name
        self.current_animation = self.animations[name]
        self.current_animation.reset()

    def update(self):
        if self.current_animation:
            self.current_animation.update()

    def get_image(self):
        return self.current_animation.get_image()

