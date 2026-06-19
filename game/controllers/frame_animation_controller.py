from game.settings import FPS
from game.animation.animation_manager import AnimationManager
from game.animation.frame_animation import FrameAnimation, load_frame_animation


class FrameAnimationController:
    def __init__(self, animation_data, anim_fps):
        self.animation_data = animation_data
        self.anim_fps = anim_fps
        self.animation_manager = AnimationManager()

    def get_current_frame(self):
        return self.animation_manager.current_animation.get_frame_data()

    def get_current_frame_index(self):
        return self.animation_manager.current_animation.get_frame_index()

    def get_image(self):
        return self.animation_manager.get_image()

    def play(self, animation_name):
        self.animation_manager.play(animation_name)

    def reset_current_animation(self):
        self.animation_manager.current_animation.reset()

    def get_current_animation(self):
        return self.animation_manager.current_animation

    def add_frame_animation(self, state, animation_name, loop=True):
        frames = load_frame_animation(self.animation_data, animation_name)
        duration = self.frame_duration(animation_name)
        self.animation_manager.add_animation(
            state,
            FrameAnimation(frames, duration, loop=loop),
        )
        return frames, duration

    def frame_duration(self, animation_name):
        return max(1, int(FPS / self.anim_fps[animation_name]))

    def update(self, owner):
        self.animation_manager.play(self.get_animation_state(owner))
        self.animation_manager.update()
