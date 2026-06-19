from game.settings import FPS
from game.animation.animation_manager import AnimationManager
from game.animation.frame_animation import FrameAnimation, load_frame_animation
from game.tuning import scale_animation_fps_map


class PlayerAnimationController:
    def __init__(self, owner, animation_data, anim_fps):
        self.animation_data = animation_data
        self.anim_fps = scale_animation_fps_map(anim_fps)
        self.animation_manager = AnimationManager()
        self.init_animations(owner)

    def get_current_frame(self):
        animation = self.animation_manager.current_animation
        if hasattr(animation, "get_frame_data"):
            return animation.get_frame_data()
        return None

    def get_current_frame_index(self):
        animation = self.animation_manager.current_animation
        if hasattr(animation, "get_frame_index"):
            return animation.get_frame_index()
        return 0

    def get_image(self):
        return self.animation_manager.get_image()

    def init_animations(self, owner):
        for state, animation_name in self.get_animation_specs(owner):
            frames = load_frame_animation(self.animation_data, animation_name)
            duration = self.frame_duration(animation_name)
            self.animation_manager.add_animation(state, FrameAnimation(frames, duration))

            if state == owner.THROW:
                owner.grab_controller.throw_duration = len(frames) * duration
            elif state == owner.GRAB_KNEE:
                owner.grab_controller.grab_knee_duration = len(frames) * duration

    def get_animation_specs(self, owner):
        return [
            (owner.IDLE, "idle"),
            (owner.WALK, "walk"),
            (owner.RUN, "run"),
            (owner.JUMP, "jump"),
            (owner.ATTACK, "attack"),
            (owner.ATTACK_1, "attack_1"),
            (owner.ATTACK_2, "attack_2"),
            (owner.ATTACK_3, "attack_3"),
            (owner.RUN_ATTACK, "run_attack"),
            (owner.JUMP_ATTACK, "jump_attack"),
            (owner.GRAB, "grab"),
            (owner.THROW, "throw"),
            (owner.GRAB_KNEE, "grab_knee"),
            (owner.HIT, "hit"),
            (owner.DEAD, "dead"),
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
            owner.RUN: owner.RUN,
            owner.JUMP: owner.JUMP,
            owner.ATTACK_1: owner.ATTACK_1,
            owner.ATTACK_2: owner.ATTACK_2,
            owner.ATTACK_3: owner.ATTACK_3,
            owner.RUN_ATTACK: owner.RUN_ATTACK,
            owner.JUMP_ATTACK: owner.JUMP_ATTACK,
            owner.GRAB: owner.GRAB,
            owner.GRAB_KNEE: owner.GRAB_KNEE,
            owner.THROW: owner.THROW,
            owner.HIT: owner.HIT,
            owner.RECOIL: owner.HIT,
            owner.DEAD: owner.DEAD,
        }
        return state_map.get(owner.state, owner.IDLE)
