from game.settings import FPS
from game.animation.frame_animation import FrameAnimation, load_frame_animation
from game.animation.animation_manager import AnimationManager


class EnemyAnimationController:
    def __init__(self, owner, animation_data, anim_fps):
        self.animation_data = animation_data
        self.anim_fps = anim_fps
        self.animation_manager = AnimationManager()
        self.init_frame_animations(owner)

    def get_current_frame_data(self):
        animation = self.animation_manager.current_animation
        if hasattr(animation, "get_frame_data"):
            return animation.get_frame_data()
        return None

    def get_image(self):
        return self.animation_manager.get_image()

    def play(self, animation_name):
        self.animation_manager.play(animation_name)

    def reset_current_animation(self):
        self.animation_manager.current_animation.reset()

    def get_current_animation(self):
        return self.animation_manager.current_animation

    def init_frame_animations(self, owner):
        for state, animation_name, loop in self.get_animation_specs(owner):
            frames = load_frame_animation(self.animation_data, animation_name)
            duration = self.frame_duration(animation_name)
            self.animation_manager.add_animation(
                state,
                FrameAnimation(frames, duration, loop=loop),
            )

    def get_animation_specs(self, owner):
        return [
            (owner.IDLE, "idle", True),
            (owner.WALK, "walk", True),
            (owner.ATTACK, "attack", False),
            (owner.HIT, "hit", True),
            (owner.DEAD, "dead", True),
        ]

    def frame_duration(self, animation_name):
        return max(1, int(FPS / self.anim_fps[animation_name]))

    def update(self, owner):
        self.animation_manager.play(self.get_animation_state(owner))
        self.animation_manager.update()

    def get_animation_state(self, owner):
        state_map = {
            owner.IDLE: owner.IDLE,
            owner.WALK: owner.WALK,
            owner.PATROL: owner.IDLE,
            owner.CHASE: owner.WALK,
            owner.ATTACK: owner.ATTACK,
            owner.HIT: owner.HIT,
            owner.RECOIL: owner.HIT,
            owner.GRABBED: owner.IDLE,
            owner.THROWN: owner.HIT,
            owner.KNOCKDOWN: owner.HIT,
            owner.GETUP: owner.IDLE,
            owner.DEAD: owner.DEAD,
        }
        return state_map.get(owner.state, owner.IDLE)
