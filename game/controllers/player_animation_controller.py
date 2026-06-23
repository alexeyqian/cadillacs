from game.controllers.frame_animation_controller import FrameAnimationController
from game.tuning import scale_animation_fps_map


class PlayerAnimationController(FrameAnimationController):
    def __init__(self, owner, animation_data, anim_fps):
        super().__init__(animation_data, scale_animation_fps_map(anim_fps))
        self.init_animations(owner)

    def init_animations(self, owner):
        for state, animation_name in self.get_animation_specs(owner):
            frames, duration = self.add_frame_animation(state, animation_name)
            total_duration = self.animation_total_duration(len(frames), duration)

            if state == owner.THROW:
                owner.grab_controller.throw_duration = total_duration
            elif state == owner.GRAB_KNEE:
                owner.grab_controller.grab_knee_duration = total_duration

    def get_animation_specs(self, owner):
        return [
            (owner.IDLE, "idle"),
            (owner.WALK, "walk"),
            (owner.RUN, "run"),
            (owner.JUMP, "jump"),
            (owner.ATTACK, "attack"),
            (owner.ATTACK2, "attack2"),
            (owner.ATTACK3, "attack3"),
            (owner.RUN_ATTACK, "run_attack"),
            (owner.JUMP_ATTACK, "jump_attack"),
            (owner.GRAB, "grab"),
            (owner.THROW, "throw"),
            (owner.GRAB_KNEE, "grab_knee"),
            (owner.HIT, "hit"),
            (owner.DEAD, "dead"),
        ]

    def get_animation_state(self, owner):
        state_map = {
            owner.IDLE: owner.IDLE,
            owner.WALK: owner.WALK,
            owner.RUN: owner.RUN,
            owner.JUMP: owner.JUMP,
            owner.ATTACK: owner.ATTACK,
            owner.ATTACK2: owner.ATTACK2,
            owner.ATTACK3: owner.ATTACK3,
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
