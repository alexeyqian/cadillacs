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

class Enemy:
    IDLE = "IDLE"
    WALK = "WALK"
    PATROL = "PATROL" # ai decisions
    CHASE = "CHASE"
    ATTACK = "ATTACK"
    HIT = "HIT"
    DEAD = "DEAD"
    GRABBED = "GRABBED"
    THROWN = "THROWN"
    KNOCKDOWN = 'KNOCKDOWN' # heavy hit or thrown cause enemy falls down briefly
    GETUP = "GETUP" # gets up after knockdown

    def __init__(self, x, y, idle_config=None, walk_config=None,
                attack_config=None, hit_config=None, dead_config=None,
                fallback_frame_factory=None, enemy_config=None):
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
        self.attack_cooldown_duration = ENEMY_ATTACK_COOLDOWN
        self.attack_windup = ENEMY_ATTACK_WINDUP
        self.attack_active = ENEMY_ATTACK_ACTIVE
        self.attack_recovery = ENEMY_ATTACK_RECOVERY
        self.attack_total_duration = (self.attack_windup + self.attack_active + self.attack_recovery)

        # hit reaction
        self.knockback_velocity = 0
        # enemy gets briefly white when hit by player
        self.hit_timer = 0
        
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
        self.init_animations(idle_config=idle_config,
                            walk_config=walk_config,
                            attack_config=attack_config,
                            hit_config=hit_config,
                            dead_config=dead_config,
                            fallback_frame_factory=fallback_frame_factory)

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
        self.attack_cooldown_duration = config.attack_cooldown

        self.collision_box_w = int(self.width * 0.5)
        self.collision_box_h = int(self.height * 0.2)
        self.hurtbox_w = int(self.width * 0.6)
        self.hurtbox_h = int(self.height * 0.6)
        self.hurtbox_offset_x = int(self.width * 0.2)
        self.hurtbox_offset_y = int(self.height * 0.1)
        self.attack_hitbox_w = int(ENEMY_HITBOX_W * config.attack_range_multiplier)
        self.attack_hitbox_h = int(self.height * 0.5)
        self.attack_hitbox_offset_y = int(self.height * 0.2)

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
            hit_config = NORMAL_ENEMY_IDLE
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
        #self.animation_manager.add_animation(
        #    self.HIT, Animation(hit_frames(), hit_dur))
        self.animation_manager.add_animation(
            self.DEAD, Animation(dead_frames, dead_dur))

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
        if self.hit_timer == 0:
            self.state = self.IDLE

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

    def get_player_distance(self, player):
        dx = player.x - self.x
        dy = player.y - self.y

        distance_x = abs(dx)
        distance_y = abs(dy)

        return dx, dy, distance_x, distance_y

    def face_player(self, player):
        self.facing_right = player.x > self.x
    
    def choose_state(self, distance_x, distance_y):
        if self.state == self.ATTACK:
            return

        # state selection, attack if close enough
        if (self.attack_cooldown <= 0
            and distance_x <= self.attack_hitbox_w
            and distance_y <= self.attack_hitbox_h):
            self.state = self.ATTACK
        elif distance_x <= self.detect_range:
            self.state = self.CHASE
        else:
            self.state = self.PATROL

    def execute_state(self, player, enemies, dx, dy):
        # execute state
        if self.state == self.PATROL:
            self.update_patrol()
        elif self.state == self.CHASE:
            self.update_walking(dx, dy)
            self.separate_from_other_enemies(enemies)
        elif self.state == self.ATTACK:
            self.update_attack(player)

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

    def apply_world_bounds(self, world_width=None, lane_top=None, lane_bottom=None):
        # todo: remove these lines of temp code
        if world_width is None:
            world_width = WORLD_WIDTH
        if lane_top is None:
            lane_top = self.lane_top
        if lane_bottom is None:
            lane_bottom = self.lane_bottom

        # world boundaries
        half_w = self.width // 2
        self.x = max(half_w, self.x) # cannot go left of window
        self.x = min(self.x, world_width - half_w) # cannot go right window
        # beat'em up lane limits creates the illusion of depth
        # player walks on a horizontal strip, not full screen
        self.y = max(lane_top, self.y) # cannot go above lane_top
        self.y = min(lane_bottom, self.y) # cannot go below lane_bottom

    def get_left(self):
        return int(self.x - self.width / 2)

    def get_top(self):
        return self.y - self.height

    def get_right(self):
        return int(self.x + self.width / 2)

    def get_bottom(self):
        return self.y

    # body rect
    def get_logical_rect(self):
        return pygame.Rect(
            int(self.get_left()),
            int(self.get_top()),
            int(self.width),
            int(self.height)
        )

    def get_hurt_rect(self):
        return pygame.Rect(
            int(self.get_left() + self.hurtbox_offset_x),
            int(self.get_top() + self.hurtbox_offset_y),
            int(self.hurtbox_w),
            int(self.hurtbox_h))

    # on bottom center
    def get_collision_rect(self):
        return pygame.Rect(
            int(self.x - self.collision_box_w/2),
            int(self.y - self.collision_box_h),
            int(self.collision_box_w),
            int(self.collision_box_h)
        )

    # hit box
    def get_attack_rect(self):
        body_left = self.get_left()
        body_top = self.get_top()

        # Use symmetric hitbox size and offsets so left/right behave identically
        hit_w = self.attack_hitbox_w
        # giving running attack a longer hitbox
        #if self.state == self.RUN_ATTACK:
        #    hit_w = self.attack_hitbox_w * 1.5
        hit_h = self.attack_hitbox_h
        #if self.weapon and not self.weapon.is_ranged:
        #    hit_w += self.weapon.hitbox_w_bonus
        #    hit_h += self.weapon.hitbox_h_bonus

        hit_y = body_top + self.attack_hitbox_offset_y
        if self.facing_right:
            hit_x = int(self.x + self.width/2)
        else:
            hit_x = int(self.x - self.width/2 - hit_w)

        return pygame.Rect(hit_x, hit_y, hit_w, hit_h)

    def update_walking(self, dx, dy):
        # horizontal movement
        if dx > 0:
            self.x += self.speed
            self.facing_right = True
        elif dx < 0:
            self.x -= self.speed
            self.facing_right = False
        # vertical movement
        if abs(dy) > 10: # allow some vertical leniency
            if dy > 0:
                self.y += self.speed
            else:
                self.y -= self.speed

        # Keep enemy inside lane, already done in apply_world_bound
        #self.y = max(self.lane_top, self.y)
        #self.y = min(self.lane_bottom - self.height, self.y)

    # enemy patrol back and forth
    def update_patrol(self):
        self.x += self.patrol_direction
        if self.patrol_direction > 0:
            self.facing_right = True
        elif self.patrol_direction < 0:
            self.facing_right = False
        if self.x > self.spawn_x + self.patrol_distance:
            self.patrol_direction = -1
        if self.x < self.spawn_x - self.patrol_distance:
            self.patrol_direction = 1

    def separate_from_other_enemies(self, enemies):
        for other in enemies:
            if other is self:
                continue
            if other.state == self.DEAD:
                continue
            dx = other.x - self.x
            if abs(dx) < 40:
                if dx > 0:
                    self.x -= 1
                else:
                    self.x += 1

    def start_attack(self):
        self.state = self.ATTACK
        self.attack_timer = 0
        self.attack_has_hit = False

    def update_attack(self, player):
        self.facing_right = player.x > self.x
        self.attack_timer += 1
        
        active_start = self.attack_windup
        active_end = self.attack_windup + self.attack_active
        is_active_frame = active_start <= self.attack_timer < active_end
        if is_active_frame and not self.attack_has_hit:
            attack_rect = self.get_attack_rect()
            player_hurt_rect = player.get_hurt_rect()
            if attack_rect and player_hurt_rect and attack_rect.colliderect(player_hurt_rect):
                player.take_damage(self.attack_damage)
                self.attack_has_hit = True
        
        if self.attack_timer >= self.attack_total_duration:
            self.state = self.IDLE
            self.attack_timer = 0
            self.attack_has_hit = False
            self.attack_cooldown = self.attack_cooldown_duration
        
    def update_attack_old(self, player):
        if self.attack_cooldown > 0:
            return
        self.facing_right = player.x > self.x
        player.take_damage(self.attack_damage)
        self.attack_cooldown = 60

    def take_damage(self, damage, attacker_x):
        if self.state == self.DEAD:
            return

        self.hp -= damage
        self.hit_timer = 15
        self.state = self.HIT

        # knockback direction based on attacker's position
        if attacker_x < self.x:
            self.knockback_velocity = 10
        else:
            self.knockback_velocity = -10
            
        if self.hp > 0 and self.should_knockdown_from_damage(damage):
            self.knockdown()
            return

        if self.hp <= 0:
            self.hp = 0
            self.state = self.DEAD
            self.death_timer = 30
            self.death_timer_started = False

    def apply_knockback(self):
        if self.knockback_velocity == 0:
            return
        self.x += self.knockback_velocity
        # friction slows down knockback over time
        self.knockback_velocity *= 0.8
        if abs(self.knockback_velocity) < 0.5:
            self.knockback_velocity = 0
            
    def knockdown(self):
        if self.state == self.DEAD:
            return
        self.state = self.KNOCKDOWN
        self.knockdown_timer = 60
        self.knockback_velocity = 0
        
    def should_knockdown_from_damage(self, damage):
        return damage >= 40

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

    def is_ready_to_remove(self):
        return self.state == self.DEAD and self.death_timer <= 0

    def grabbed_by_player(self):
        if self.state == self.DEAD:
            return
        self.state = self.GRABBED
        self.knockback_velocity = 0
        self.hit_timer = 0
        
    def thrown_by_player(self, direction):
        if self.state == self.DEAD:
            return
        
        self.state = self.THROWN
        self.facing_right = direction > 0
        self.thrown_velocity_x = 14 * direction
        self.thrown_timer = 30
        self.thrown_hit_targets.clear()
        self.take_thrown_damage(self.thrown_damage)

    # this prevents knee attacks from accidentally knocking the enemy out of grab state
    def take_grab_knee_damage(self, damage):
        if self.state == self.DEAD:
            return
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
            self.state = self.DEAD
            self.death_timer = 30
            self.death_timer_started = False # todo: not True?
            return
        
        self.state = self.GRABBED

    def take_thrown_damage(self, damage):
        if self.state == self.DEAD:
            return

        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
            self.state = self.DEAD
            self.death_timer = 30
            self.death_timer_started = False

    def create_loot(self):
        roll = random.randint(1, 100)
        if roll <= 30:
            return Loot(self.x, self.y, "health")
        elif roll <= 50:
            return Loot(self.x, self.y, "ammo")

        return None
