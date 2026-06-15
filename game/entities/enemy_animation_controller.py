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
        idle_frames = load_frame_animation(self.animation_data, "idle")
        walk_frames = load_frame_animation(self.animation_data, "walk")
        attack_frames = load_frame_animation(self.animation_data, "attack")
        hit_frames = load_frame_animation(self.animation_data, "hit")
        dead_frames = load_frame_animation(self.animation_data, "dead")

        idle_dur = self.frame_duration("idle")
        walk_dur = self.frame_duration("walk")
        attack_dur = self.frame_duration("attack")
        hit_dur = self.frame_duration("hit")
        dead_dur = self.frame_duration("dead")

        self.animation_manager.add_animation(owner.IDLE, FrameAnimation(idle_frames, idle_dur))
        self.animation_manager.add_animation(owner.WALK, FrameAnimation(walk_frames, walk_dur))
        self.animation_manager.add_animation(owner.ATTACK, FrameAnimation(attack_frames, attack_dur, loop=False))
        self.animation_manager.add_animation(owner.HIT, FrameAnimation(hit_frames, hit_dur))
        self.animation_manager.add_animation(owner.DEAD, FrameAnimation(dead_frames, dead_dur))

    def frame_duration(self, animation_name):
        return max(1, int(FPS / self.anim_fps[animation_name]))

    def update(self, owner):
        if owner.state == owner.IDLE:
            self.animation_manager.play(owner.IDLE)
        elif owner.state == owner.WALK:
            self.animation_manager.play(owner.WALK)
        elif owner.state == owner.PATROL:
            self.animation_manager.play(owner.IDLE)
        elif owner.state == owner.CHASE:
            self.animation_manager.play(owner.WALK)
        elif owner.state == owner.ATTACK:
            self.animation_manager.play(owner.ATTACK)
        elif owner.state == owner.HIT:
            self.animation_manager.play(owner.HIT)
        elif owner.state == owner.GRABBED:
            self.animation_manager.play(owner.IDLE)
        elif owner.state == owner.THROWN: # TODO
            self.animation_manager.play(owner.HIT)
        elif owner.state == owner.KNOCKDOWN: # TODO
            self.animation_manager.play(owner.HIT)
        elif owner.state == owner.GETUP:
            self.animation_manager.play(owner.IDLE)
        elif owner.state == owner.DEAD:
            self.animation_manager.play(owner.DEAD)

        self.animation_manager.update()
