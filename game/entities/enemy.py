import random
import pygame

from game.settings import *
from game.colors import *
from game.tuning import scale_frames, scale_timing, scale_animation_fps_map
from game.animation.frame_animation import FrameAnimation, load_frame_animation
from game.animation.animation_manager import AnimationManager

from game.entities.enemy_config import get_enemy_config
from game.entities.enemy_state import EnemyState
from game.entities.enemy_boxes import EnemyBoxMixin
from game.entities.enemy_ai import EnemyAIMixin
from game.entities.enemy_combat import EnemyCombatMixin
from game.entities.enemy_lifecycle import EnemyLifecycleMixin
from game.entities.enemy_reactions import EnemyReactionMixin
from game.entities.loot import Loot

class Enemy(EnemyBoxMixin, EnemyAIMixin, EnemyCombatMixin,
            EnemyReactionMixin, EnemyLifecycleMixin):
    IDLE = EnemyState.IDLE
    WALK = EnemyState.WALK
    PATROL = EnemyState.PATROL
    CHASE = EnemyState.CHASE
    ATTACK = EnemyState.ATTACK
    HIT = EnemyState.HIT
    DEAD = EnemyState.DEAD
    GRABBED = EnemyState.GRABBED
    THROWN = EnemyState.THROWN
    KNOCKDOWN = EnemyState.KNOCKDOWN
    GETUP = EnemyState.GETUP

    def __init__(self, x, y, enemy_type, animation_data, anim_fps,
            sprite_scale=4, attack_timing=None):
        self.x = x
        self.y = y
        self.enemy_id = "normal"
        self.display_name = "Enemy"
        self.score_points = 100
        
        # TODO: use scaler-able settings to replace hardcode
        self.attack_range = 90 # should i attack, attack_rect = did i hit
        self.attack_lane_range = 45
        self.attack_cooldown_duration = 45

        ###### boxes ######
        # logical box
        self.width = ENEMY_W
        self.height = ENEMY_H
        #collision box
        self.collision_box_w = ENEMY_COLLISION_W
        self.collision_box_h = ENEMY_COLLISION_H
        # hurt box
        self.hurtbox_w = ENEMY_HURTBOX_W
        self.hurtbox_h = ENEMY_HURTBOX_H
        self.hurtbox_offset_x = ENEMY_HURTBOX_OFFSET_X
        self.hurtbox_offset_y = ENEMY_HURTBOX_OFFSET_Y

        self.speed = ENEMY_SPEED
        self.max_hp = ENEMY_MAX_HP
        self.hp = self.max_hp
        self.state = self.IDLE
        self.facing_right = False
        self.loot_generated = False
        self.death_timer = 30
        self.death_timer_started = False

        # within this range, enemy chases player
        # outside this range, enemy ignores player
        self.detect_range = ENEMY_DETECT_RANGE
        # enemy remembers where it spawned
        self.spawn_x = x
        self.patrol_distance = ENEMY_DETECT_RANGE
        self.patrol_direction = 1

        self.attack_damage = ENEMY_ATTACK_DAMAGE

        self.attack_has_hit = False
        self.attack_cooldown = 0

        # hit reaction
        self.knockback_velocity = 0
        # enemy gets briefly white when hit by player
        self.hit_timer = 0
        self.hit_stun_duration = 15
        
        # grab/throw
        self.thrown_velocity_x = 0
        self.thrown_timer = 0
        self.thrown_hit_targets = set()
        self.thrown_damage = THROWN_DAMAGE
        
        #knockdown/getup
        self.knockdown_timer = 0
        self.getup_timer = 0

        #lane boundaries
        self.lane_top = LANE_TOP
        self.lane_bottom = LANE_BOTTOM

        self.apply_enemy_config(get_enemy_config(enemy_type))
        self.animation_data = animation_data
        self.anim_fps = scale_animation_fps_map(anim_fps)
        self.sprite_scale = sprite_scale
        self.animation_manager = AnimationManager()
        self.init_frame_animations()

    def init_frame_animations(self):
        idle_frames = load_frame_animation(self.animation_data, "idle")
        walk_frames = load_frame_animation(self.animation_data, "walk")
        attack_frames = load_frame_animation(self.animation_data, "attack")
        hit_frames = load_frame_animation(self.animation_data, "hit")
        dead_frames = load_frame_animation(self.animation_data, "dead")
        # todo: game frame duration for single sprite frame? or idle sprite frames
        # Answer: for single sprite frame
        idle_dur = max(1, int(FPS/self.anim_fps["idle"]))
        walk_dur = max(1, int(FPS/self.anim_fps["walk"]))
        attack_dur = max(1, int(FPS/self.anim_fps["attack"]))
        hit_dur = max(1, int(FPS/self.anim_fps["hit"]))
        dead_dur = max(1, int(FPS/self.anim_fps["dead"]))
    
        self.animation_manager.add_animation(self.IDLE,
                FrameAnimation(idle_frames, idle_dur))
        self.animation_manager.add_animation(self.WALK,
                FrameAnimation(walk_frames, walk_dur))
        self.animation_manager.add_animation(self.ATTACK,
                FrameAnimation(attack_frames, attack_dur))
        self.animation_manager.add_animation(self.HIT,
                FrameAnimation(hit_frames, hit_dur))
        self.animation_manager.add_animation(self.DEAD,
                FrameAnimation(dead_frames, dead_dur))

        # return value is object include multiple frames/surfaces

    def get_current_frame_data(self):
        animation = self.animation_manager.current_animation
        if hasattr(animation, "get_frame_data"):
            return animation.get_frame_data()
        return None

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

    def apply_enemy_config(self, config):
        self.enemy_id = config.enemy_id
        self.display_name = config.display_name
        self.score_points = config.score_points
        self.width = int(config.width)
        self.height = int(config.height)
        self.max_hp = config.max_hp
        self.hp = self.max_hp
        self.speed = config.speed
        self.attack_damage = config.attack_damage
        self.detect_range = config.detect_range
        #self.attack_cooldown_duration = scale_frames(config.attack_cooldown)
        self.hit_stun_duration = scale_frames(config.hit_stun_duration)

        self.collision_box_w = int(self.width * 0.5)
        self.collision_box_h = int(self.height * 0.2)
        self.hurtbox_w = int(self.width * 0.6)
        self.hurtbox_h = int(self.height * 0.6)
        self.hurtbox_offset_x = int(self.width * 0.2)
        self.hurtbox_offset_y = int(self.height * 0.1)

    def update(self, player, enemies):
        if self.update_special_states():
            return
        self.update_timers()
        if self.update_hit_state():
            return
        self.apply_knockback()
        dx, dy, distance_x, distance_y = self.get_player_distance(player)
        if distance_x <= self.detect_range:
            self.face_player(player)
        self.choose_state(distance_x, distance_y)
        self.execute_state(player, enemies, dx, dy)
        #self.apply_world_bounds()
        self.update_animation()

    def create_loot(self):
        roll = random.randint(1, 100)
        if roll <= 30:
            return Loot(self.x, self.y, "health")
        elif roll <= 50:
            return Loot(self.x, self.y, "ammo")

        return None

    def draw(self, screen, camera_x):
        frame = self.get_current_frame_data()

        if not frame:
            raise ValueError(f"Missing frame data for enemy state: {self.state}")

        # get the surface object of current animation's current frame
        image = self.animation_manager.get_image()

        scale = self.sprite_scale
        image = pygame.transform.scale(
            image,
            (
                image.get_width() * scale,
                image.get_height() * scale
            )
        )

        if not self.facing_right:
            image = pygame.transform.flip(image, True, False)

        frame_rect = self.get_frame_rect()
        screen.blit(image, (frame_rect.x - camera_x, frame_rect.y))

        if SHOW_ENEMY_RECT:
            body_rect = self.get_logical_rect()
            hurt_rect = self.get_hurt_rect()
            collision_rect = self.get_collision_rect()
            attack_rect = self.get_attack_rect()

            pygame.draw.rect(screen, (80, 180, 255), (
                collision_rect.x - camera_x,
                collision_rect.y,
                collision_rect.width,
                collision_rect.height
            ), 1)

            pygame.draw.rect(screen, GREEN_COLOR, (
                body_rect.x - camera_x,
                body_rect.y,
                body_rect.width,
                body_rect.height
            ), 1)

            if hurt_rect:
                pygame.draw.rect(screen, (255, 80, 80), (
                    hurt_rect.x - camera_x,
                    hurt_rect.y,
                    hurt_rect.width,
                    hurt_rect.height
                ), 1)

            if attack_rect:
                pygame.draw.rect(screen, YELLOW_COLOR, (
                    attack_rect.x - camera_x,
                    attack_rect.y,
                    attack_rect.width,
                    attack_rect.height
                ), 1)

        bar_width = 50
        bar_x = int(self.x - camera_x - bar_width / 2)
        hp_width = int(bar_width * (self.hp / self.max_hp))
        hp_height = 12
        pygame.draw.rect(
            screen,
            (120, 120, 120),
            (bar_x, frame_rect.y - hp_height, bar_width, 6)
        )
        pygame.draw.rect(
            screen,
            (255, 0, 0),
            (bar_x, frame_rect.y - hp_height, hp_width, 6)
        )