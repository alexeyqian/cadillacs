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
        idle_frames = load_frame_animation(self.animation_data, "idle")
        walk_frames = load_frame_animation(self.animation_data, "walk")
        run_frames = load_frame_animation(self.animation_data, "run")
        jump_frames = load_frame_animation(self.animation_data, "jump")
        attack_frames = load_frame_animation(self.animation_data, "attack")
        attack_1_frames = load_frame_animation(self.animation_data, "attack_1")
        attack_2_frames = load_frame_animation(self.animation_data, "attack_2")
        attack_3_frames = load_frame_animation(self.animation_data, "attack_3")
        run_attack_frames = load_frame_animation(self.animation_data, "run_attack")
        jump_attack_frames = load_frame_animation(self.animation_data, "jump_attack")
        grab_frames = load_frame_animation(self.animation_data, "grab")
        throw_frames = load_frame_animation(self.animation_data, "throw")
        grab_knee_frames = load_frame_animation(self.animation_data, "grab_knee")
        hit_frames = load_frame_animation(self.animation_data, "hit")
        dead_frames = load_frame_animation(self.animation_data, "dead")

        idle_dur = self.frame_duration("idle")
        walk_dur = self.frame_duration("walk")
        run_dur = self.frame_duration("run")
        jump_dur = self.frame_duration("jump")
        attack_dur = self.frame_duration("attack")
        attack_1_dur = self.frame_duration("attack_1")
        attack_2_dur = self.frame_duration("attack_2")
        attack_3_dur = self.frame_duration("attack_3")
        run_attack_dur = self.frame_duration("run_attack")
        jump_attack_dur = self.frame_duration("jump_attack")
        grab_dur = self.frame_duration("grab")
        throw_dur = self.frame_duration("throw")
        grab_knee_dur = self.frame_duration("grab_knee")
        hit_dur = self.frame_duration("hit")
        dead_dur = self.frame_duration("dead")

        owner.grab.throw_duration = len(throw_frames) * throw_dur
        owner.grab.grab_knee_duration = len(grab_knee_frames) * grab_knee_dur

        self.animation_manager.add_animation(owner.IDLE, FrameAnimation(idle_frames, idle_dur))
        self.animation_manager.add_animation(owner.WALK, FrameAnimation(walk_frames, walk_dur))
        self.animation_manager.add_animation(owner.RUN, FrameAnimation(run_frames, run_dur))
        self.animation_manager.add_animation(owner.JUMP, FrameAnimation(jump_frames, jump_dur))
        self.animation_manager.add_animation(owner.ATTACK, FrameAnimation(attack_frames, attack_dur))
        self.animation_manager.add_animation(owner.ATTACK_1, FrameAnimation(attack_1_frames, attack_1_dur))
        self.animation_manager.add_animation(owner.ATTACK_2, FrameAnimation(attack_2_frames, attack_2_dur))
        self.animation_manager.add_animation(owner.ATTACK_3, FrameAnimation(attack_3_frames, attack_3_dur))
        self.animation_manager.add_animation(owner.RUN_ATTACK, FrameAnimation(run_attack_frames, run_attack_dur))
        self.animation_manager.add_animation(owner.JUMP_ATTACK, FrameAnimation(jump_attack_frames, jump_attack_dur))
        self.animation_manager.add_animation(owner.GRAB, FrameAnimation(grab_frames, grab_dur))
        self.animation_manager.add_animation(owner.THROW, FrameAnimation(throw_frames, throw_dur))
        self.animation_manager.add_animation(owner.GRAB_KNEE, FrameAnimation(grab_knee_frames, grab_knee_dur))
        self.animation_manager.add_animation(owner.HIT, FrameAnimation(hit_frames, hit_dur))
        # todo: add recoil animation
        self.animation_manager.add_animation(owner.DEAD, FrameAnimation(dead_frames, dead_dur))

    def frame_duration(self, animation_name):
        return max(1, int(FPS / self.anim_fps[animation_name]))

    def update(self, owner):
        if owner.state == owner.IDLE:
            self.animation_manager.play(owner.IDLE)
        elif owner.state == owner.WALK:
            self.animation_manager.play(owner.WALK)
        elif owner.state == owner.RUN:
            self.animation_manager.play(owner.RUN)
        elif owner.state == owner.JUMP:
            self.animation_manager.play(owner.JUMP)
        elif owner.state == owner.ATTACK_1:
            self.animation_manager.play(owner.ATTACK_1)
        elif owner.state == owner.ATTACK_2:
            self.animation_manager.play(owner.ATTACK_2)
        elif owner.state == owner.ATTACK_3:
            self.animation_manager.play(owner.ATTACK_3)
        elif owner.state == owner.RUN_ATTACK:
            self.animation_manager.play(owner.RUN_ATTACK)
        elif owner.state == owner.JUMP_ATTACK:
            self.animation_manager.play(owner.JUMP_ATTACK)
        elif owner.state == owner.GRAB:
            self.animation_manager.play(owner.GRAB)
        elif owner.state == owner.GRAB_KNEE:
            self.animation_manager.play(owner.GRAB_KNEE)
        elif owner.state == owner.THROW:
            self.animation_manager.play(owner.THROW)
        elif owner.state == owner.HIT:
            self.animation_manager.play(owner.HIT)
        elif owner.state == owner.RECOIL: # TODO: add recoil animation
            self.animation_manager.play(owner.HIT)
        elif owner.state == owner.DEAD:
            self.animation_manager.play(owner.DEAD)
        else:
            self.animation_manager.play(owner.IDLE)

        self.animation_manager.update()
