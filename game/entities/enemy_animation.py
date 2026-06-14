from game.settings import *
from game.assets.placeholder.enemy_frames import create_enemy_frames
from game.assets.asset_manager import AssetManager
from game.animation.animation import Animation
from game.animation.animation_config import *

class EnemyAnimationMixin:
    def init_animations(self, idle_config=None, walk_config=None, attack_config=None,
                    hit_config=None, dead_config=None, fallback_frame_factory=None):
        use_normal_dead_animation = (
            idle_config is None and
            walk_config is None and
            attack_config is None and
            hit_config is None and
            dead_config is None
        )

        if idle_config is None:
            idle_config = NORMAL_ENEMY_IDLE
        if walk_config is None:
            walk_config = NORMAL_ENEMY_WALK
        if attack_config is None:
            attack_config = NORMAL_ENEMY_ATTACK
        if hit_config is None:
            hit_config = NORMAL_ENEMY_HIT
        if use_normal_dead_animation:
            dead_config = NORMAL_ENEMY_DEAD
        if fallback_frame_factory is None:
            fallback_frame_factory = create_enemy_frames

        # assets loader
        idle_frames = AssetManager.load_animation(idle_config, fallback_frame_factory)
        walk_frames = AssetManager.load_animation(walk_config, fallback_frame_factory)
        # todo: chase frames
        attack_frames = AssetManager.load_animation(attack_config, fallback_frame_factory)
        hit_frames = AssetManager.load_animation(hit_config, fallback_frame_factory)
        dead_frames = AssetManager.load_animation(dead_config, fallback_frame_factory)
        
        # compute frame durations to match game FPS
        idle_dur = max(1, int(FPS / ANIM_FPS_IDLE_ENEMY))
        walk_dur = max(1, int(FPS / ANIM_FPS_WALK_ENEMY))
        attack_dur = max(1, int(FPS / ANIM_FPS_ATTACK_ENEMY))
        hit_dur = max(1, int(FPS / ANIM_FPS_HIT_ENEMY))
        dead_dur = max(1, int(self.death_timer / len(dead_frames)))

        self.animation_manager.add_animation(
            self.IDLE, Animation(idle_frames, idle_dur))
        self.animation_manager.add_animation(
            self.WALK, Animation(walk_frames, walk_dur))
        # add chase
        self.animation_manager.add_animation(
            self.ATTACK, Animation(attack_frames, attack_dur))
        self.animation_manager.add_animation(
            self.HIT, Animation(hit_frames(), hit_dur))
        self.animation_manager.add_animation(
            self.DEAD, Animation(dead_frames, dead_dur))

    def update_animation(self):
        if self.state == self.IDLE:
            self.animation_manager.play(self.IDLE)
        elif self.state == self.WALK:
            self.animation_manager.play(self.WALK)
        elif self.state == self.PATROL:
            self.animation_manager.play(self.IDLE)
        elif self.state == self.CHASE:
            self.animation_manager.play(self.WALK)
        elif self.state == self.ATTACK:
            self.animation_manager.play(self.ATTACK)
        # by player
        elif self.state == self.HIT:
            self.animation_manager.play(self.HIT)
        elif self.state == self.GRABBED:
            self.animation_manager.play(self.IDLE)
        elif self.state == self.THROWN:
            self.animation_manager.play(self.THROWN)
        elif self.state == self.KNOCKDOWN:
            self.animation_manager.play(self.KNOCKDOWN)

        elif self.state == self.GETUP:
            self.animation_manager.play(self.IDLE)
        elif self.state == self.DEAD:
            self.animation_manager.play(self.DEAD)

        self.animation_manager.update()