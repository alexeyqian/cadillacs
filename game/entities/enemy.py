import random
import pygame

from game.settings import *
from game.colors import *
from game.entities.loot import Loot

from game.assets.placeholder.enemy_frames import *
from game.assets.asset_manager import AssetManager

from game.animation.animation import Animation
from game.animation.animation_manager import AnimationManager
from game.animation.animation_config import *
from game.tuning import scale_frames, scale_timing
from game.entities.enemy_state import EnemyState
from game.entities.enemy_boxes import EnemyBoxMixin
from game.entities.enemy_ai import EnemyAIMixin
from game.entities.enemy_combat import EnemyCombatMixin
from game.entities.enemy_animation import EnemyAnimationMixin

class Enemy(EnemyBoxMixin, EnemyAIMixin, EnemyCombatMixin, EnemyAnimationMixin):
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

    def __init__(self, x, y, idle_config=None, walk_config=None,
                attack_config=None, hit_config=None, dead_config=None,
                fallback_frame_factory=None, enemy_config=None,
                load_legacy_animations=True):
        self.x = x
        self.y = y
        self.enemy_id = "normal"
        self.display_name = "Enemy"
        self.score_points = 100
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
        # attack box
        self.attack_hitbox_w = ENEMY_HITBOX_W
        self.attack_hitbox_h = ENEMY_HITBOX_H
        self.attack_hitbox_offset_y = ENEMY_HITBOX_OFFSET_Y

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

        self.attack_timer = 0 # ?
        self.attack_has_hit = False
        self.attack_cooldown = 0
        self.attack_cooldown_duration = scale_frames(ENEMY_ATTACK_COOLDOWN)
        self.apply_attack_timing({
            "windup": ENEMY_ATTACK_WINDUP,
            "active": ENEMY_ATTACK_ACTIVE,
            "recovery": ENEMY_ATTACK_RECOVERY,
        })

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

        if enemy_config is not None:
            self.apply_enemy_config(enemy_config)
            idle_config = enemy_config.idle_config
            walk_config = enemy_config.walk_config
            attack_config = enemy_config.attack_config

        self.animation_manager = AnimationManager()
        if load_legacy_animations:
            self.init_animations(idle_config=idle_config,
                                walk_config=walk_config,
                                attack_config=attack_config,
                                hit_config=hit_config,
                                dead_config=dead_config,
                                fallback_frame_factory=fallback_frame_factory)

    def apply_attack_timing(self, attack_timing):
        timing = scale_timing(
            windup=attack_timing["windup"],
            active=attack_timing["active"],
            recovery=attack_timing["recovery"],
        )
        self.attack_windup = timing["windup"]
        self.attack_active = timing["active"]
        self.attack_recovery = timing["recovery"]
        self.attack_total_duration = timing["total"]

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
        self.attack_cooldown_duration = scale_frames(config.attack_cooldown)
        self.apply_attack_timing(config.attack_timing)
        self.hit_stun_duration = scale_frames(config.hit_stun_duration)

        self.collision_box_w = int(self.width * 0.5)
        self.collision_box_h = int(self.height * 0.2)
        self.hurtbox_w = int(self.width * 0.6)
        self.hurtbox_h = int(self.height * 0.6)
        self.hurtbox_offset_x = int(self.width * 0.2)
        self.hurtbox_offset_y = int(self.height * 0.1)
        self.attack_hitbox_w = int(ENEMY_HITBOX_W * config.attack_range_multiplier)
        self.attack_hitbox_h = int(self.height * 0.5)
        self.attack_hitbox_offset_y = int(self.height * 0.2)

    def update_special_states(self):
        if self.state == self.GRABBED:
            self.update_animation()
            return True
        if self.state == self.THROWN:
            self.update_thrown_state()
            return True
        if self.state == self.KNOCKDOWN:
            self.update_knockdown_state()
            return True
        if self.state == self.GETUP:
            self.update_getup_state()
            return True
        if self.state == self.DEAD:
            self.update_dead_state()
            return True

        return False

    def update_thrown_state(self):
        if self.thrown_velocity_x > 0:
                self.facing_right = True
        elif self.thrown_velocity_x < 0:
            self.facing_right = False

        self.x += self.thrown_velocity_x
        self.thrown_velocity_x *= 0.9
        self.thrown_timer -= 1
        
        if self.thrown_timer <= 0 or abs(self.thrown_velocity_x) < 1:
            self.state = self.KNOCKDOWN
            self.knockdown_timer = 60
            self.thrown_velocity_x = 0

        self.update_animation()

    def update_knockdown_state(self):
        self.knockdown_timer -= 1
        if self.knockdown_timer <= 0:
            self.state = self.GETUP
            self.getup_timer = 20
        self.update_animation()

    def update_getup_state(self):
        self.getup_timer -= 1
        if self.getup_timer <= 0:
            self.state = self.IDLE
        self.update_animation()

    def update_hit_state(self):
        if self.hit_timer <= 0:
            return False

        # enemy pauses briefly when hit by player, but can still be knocked back
        self.hit_timer -= 1
        self.apply_knockback()
        if self.hit_timer <= 0:
            self.state = self.IDLE
        else:
            self.state = self.HIT
        self.update_animation()

        return True

    def update_dead_state(self):
        if not self.death_timer_started:
            self.death_timer_started = True
        if self.death_timer > 0:
            self.death_timer -= 1
        self.update_animation()

    def update_timers(self):
        # attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

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

    def draw(self, screen, camera_x):
        screen_x = self.x - camera_x
        screen_left = self.get_left() - camera_x

        image = self.animation_manager.get_image()
        if self.facing_right:
            image = pygame.transform.flip(image, True, False)
        if self.state == self.DEAD:
            image = self.animation_manager.get_image().copy()
            image.set_alpha(120) # draw dead enemy darker
        if self.state == self.KNOCKDOWN: # knockdown show enemy sideways
            image = pygame.transform.rotate(image, 90)
            image = pygame.transform.scale(image, (self.height, self.width))
        else:
            image = pygame.transform.scale(image, (self.width, self.height))

        # Center the scaled image inside the enemy bounding box so it visually aligns
        img_w, img_h = image.get_size()
        blit_x = screen_left + (self.width - img_w) // 2
        blit_y = self.y - img_h
        screen.blit(image, (blit_x, blit_y))

        if SHOW_ENEMY_RECT:
            body_rect = self.get_logical_rect()
            hurt_rect = self.get_hurt_rect()
            collision_rect = self.get_collision_rect()

            pygame.draw.rect(screen,GREEN_COLOR,
                (body_rect.x - camera_x, body_rect.y,
                body_rect.width, body_rect.height), 1)
            pygame.draw.rect(screen,(255, 80, 80),
                (hurt_rect.x - camera_x, hurt_rect.y,
                hurt_rect.width, hurt_rect.height), 1)
            pygame.draw.rect(screen, (80, 180, 255),
                (collision_rect.x - camera_x, collision_rect.y,
                collision_rect.width, collision_rect.height), 1)

            attack_rect = self.get_attack_rect()
            if attack_rect:
                pygame.draw.rect(screen, YELLOW_COLOR,
                    (attack_rect.x - camera_x, attack_rect.y,
                    attack_rect.width, attack_rect.height), 1)

        # health bar background
        bar_width = 50
        bar_x = int(self.x - camera_x - bar_width / 2)
        hp_width = int(bar_width * (self.hp / self.max_hp))
        hp_height = 12
        # todo: fix hardcode 50 and 6 here
        pygame.draw.rect(
            screen, (120, 120, 120),
            (bar_x, self.get_top() - hp_height, bar_width, 6))
        # health bar
        
        pygame.draw.rect(
            screen, (255, 0, 0),
            (bar_x, self.get_top() - hp_height, hp_width, 6))

    def is_ready_to_remove(self):
        return self.state == self.DEAD and self.death_timer <= 0

    def create_loot(self):
        roll = random.randint(1, 100)
        if roll <= 30:
            return Loot(self.x, self.y, "health")
        elif roll <= 50:
            return Loot(self.x, self.y, "ammo")

        return None
