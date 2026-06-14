from game.entities.enemy import Enemy
from game.animation.animation import Animation
from game.animation.animation_config import *
from game.assets.placeholder.enemy_frames import create_raptor_frames
from game.assets.asset_manager import AssetManager
from game.settings import *


class RaptorEnemy(Enemy):
    JUMP = "JUMP"
    JUMP_ATTACK = "JUMP_ATTACK"

    def __init__(self, x, y):
        super().__init__(x, y, fallback_frame_factory=create_raptor_frames)
        self.width = RAPTOR_ENEMY_W
        self.height = RAPTOR_ENEMY_H
        self.max_hp = RAPTOR_ENEMY_MAX_HP
        self.hp = self.max_hp
        self.speed = RAPTOR_ENEMY_SPEED
        self.attack_damage = RAPTOR_ENEMY_ATTACK_DAMAGE

        # properties special to current raptor enemy
        self.leap_cooldown = 0
        self.leap_speed = 12

    def init_animations(self, idle_config=None, walk_config=None, attack_config=None,
                    hit_config=None, dead_config=None, fallback_frame_factory=None):
        if fallback_frame_factory is None:
            fallback_frame_factory = create_raptor_frames

        idle_frames = AssetManager.load_animation(
            RAPTOR_ENEMY_IDLE, fallback_frame_factory)
        patrol_frames = AssetManager.load_animation(
            RAPTOR_ENEMY_PATROL, fallback_frame_factory)
        chase_frames = AssetManager.load_animation(
            RAPTOR_ENEMY_CHASE, fallback_frame_factory)
        jump_frames = AssetManager.load_animation(
            RAPTOR_ENEMY_JUMP, fallback_frame_factory)
        attack_frames = AssetManager.load_animation(
            RAPTOR_ENEMY_ATTACK, fallback_frame_factory)
        jump_attack_frames = AssetManager.load_animation(
            RAPTOR_ENEMY_JUMP_ATTACK, fallback_frame_factory)

        idle_dur = max(1, int(FPS / ANIM_FPS_IDLE_ENEMY))
        walk_dur = max(1, int(FPS / ANIM_FPS_WALK_ENEMY))
        attack_dur = max(1, int(FPS / ANIM_FPS_ATTACK_ENEMY))
        hit_dur = max(1, int(FPS / ANIM_FPS_HIT_ENEMY))

        self.animation_manager.add_animation(
            self.IDLE, Animation(idle_frames, idle_dur))
        self.animation_manager.add_animation(
            self.PATROL, Animation(patrol_frames, walk_dur))
        self.animation_manager.add_animation(
            self.CHASE, Animation(chase_frames, walk_dur))
        self.animation_manager.add_animation(
            self.WALK, Animation(chase_frames, walk_dur))
        self.animation_manager.add_animation(
            self.JUMP, Animation(jump_frames, attack_dur))
        self.animation_manager.add_animation(
            self.ATTACK, Animation(attack_frames, attack_dur))
        self.animation_manager.add_animation(
            self.JUMP_ATTACK, Animation(jump_attack_frames, attack_dur))
        self.animation_manager.add_animation(
            self.HIT, Animation(attack_frames, hit_dur))
        self.animation_manager.add_animation(
            self.DEAD, Animation(idle_frames, 999))

    def update(self, player, enemies):
        if self.leap_cooldown > 0:
            self.leap_cooldown -= 1
        # todo: why not call super() first
        super().update(player, enemies)

    def choose_state(self, distance_x, distance_y):
        if self.state in [self.ATTACK, self.JUMP_ATTACK]:
            return

        can_attack = (
            self.attack_cooldown <= 0
            and distance_x <= self.attack_range
            and distance_y <= self.attack_lane_range
        )
        if can_attack:
            if self.leap_cooldown <= 0:
                self.state = self.JUMP_ATTACK
                self.leap_cooldown = 120
            else:
                self.state = self.ATTACK
        elif distance_x <= self.detect_range:
            self.state = self.CHASE
        else:
            self.state = self.PATROL

    def execute_state(self, player, enemies, dx, dy):
        if self.state == self.JUMP_ATTACK:
            self.update_attack(player)
        else:
            super().execute_state(player, enemies, dx, dy)

    def update_attack(self, player):
        if self.state == self.JUMP_ATTACK and self.attack_timer == 0:
            self.leap_toward_player(player)

        super().update_attack(player)

    def leap_toward_player(self, player):
        if player.x > self.x:
            self.facing_right = True
            self.x += self.leap_speed
        else:
            self.facing_right = False
            self.x -= self.leap_speed

    def update_animation(self):
        if self.state == self.IDLE:
            self.animation_manager.play(self.IDLE)
        elif self.state == self.PATROL:
            self.animation_manager.play(self.PATROL)
        elif self.state in [self.WALK, self.CHASE]:
            self.animation_manager.play(self.CHASE)
        elif self.state == self.JUMP:
            self.animation_manager.play(self.JUMP)
        elif self.state == self.ATTACK:
            self.animation_manager.play(self.ATTACK)
        elif self.state == self.JUMP_ATTACK:
            self.animation_manager.play(self.JUMP_ATTACK)
        elif self.state == self.HIT:
            self.animation_manager.play(self.HIT)
        elif self.state == self.GRABBED:
            self.animation_manager.play(self.IDLE)
        elif self.state == self.THROWN:
            self.animation_manager.play(self.HIT)
        elif self.state == self.KNOCKDOWN:
            self.animation_manager.play(self.HIT)
        elif self.state == self.GETUP:
            self.animation_manager.play(self.IDLE)
        elif self.state == self.DEAD:
            self.animation_manager.play(self.DEAD)

        self.animation_manager.update()
