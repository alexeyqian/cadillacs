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
                fallback_frame_factory=None):
        self.x = x
        self.y = y
        self.width = ENEMY_W
        self.height = ENEMY_H
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

        # attack players / combat
        # attack hitbox settings (kept symmetric for left/right)
        self.attack_hitbox_w = ENEMY_HITBOX_W
        self.attack_hitbox_h = ENEMY_HITBOX_H
        self.attack_hitbox_offset_y = ENEMY_HITBOX_OFFSET_Y
        self.attack_damage = ENEMY_ATTACK_DAMAGE

        self.attack_timer = 0 # ?
        self.attack_has_hit = False
        self.attack_cooldown = 0
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

        self.animation_manager = AnimationManager()
        self.init_animations(idle_config=idle_config,
                            walk_config=walk_config,
                            attack_config=attack_config,
                            hit_config=hit_config,
                            dead_config=dead_config,
                            fallback_frame_factory=fallback_frame_factory)

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
        enemy_center_x = self.x + self.width / 2
        enemy_center_y = self.y + self.height / 2

        player_center_x = player.x + player.width / 2
        player_center_y = player.y + player.height / 2

        dx = player_center_x - enemy_center_x
        dy = player_center_y - enemy_center_y

        distance_x = abs(dx)
        distance_y = abs(dy)

        return dx, dy, distance_x, distance_y
    
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
        self.choose_state(distance_x, distance_y)
        self.execute_state(player, enemies, dx, dy)
        self.apply_world_bounds()
        self.update_animation()

    def draw(self, screen, camera_x):
        screen_x = self.x - camera_x
        # shadow
        pygame.draw.ellipse(
            screen, (50, 50, 50),
            (screen_x,self.y + self.height - 10,self.width,12))

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
        blit_x = screen_x + (self.width - img_w) // 2
        blit_y = self.y + (self.height - img_h) // 2
        screen.blit(image, (blit_x, blit_y))

        # debug: draw enemy bounding box (world -> screen)
        if SHOW_ENEMY_RECT:
            pygame.draw.rect(screen, RED_COLOR, (screen_x, self.y, self.width, self.height), 2)

        # attack hitbox for debug
        if SHOW_ENEMY_HITBOX:
            attack_rect = self.get_attack_rect()
            if attack_rect:
                pygame.draw.rect(screen, YELLOW_COLOR,
                    (attack_rect.x - camera_x, attack_rect.y,
                    attack_rect.width, attack_rect.height), 1)

        # health bar background
        pygame.draw.rect(
            screen, (120, 120, 120),
            (screen_x, self.y - 12, 50, 6))
        # health bar
        hp_width = int(50 * (self.hp / self.max_hp))
        pygame.draw.rect(
            screen, (255, 0, 0),
            (screen_x, self.y - 12, hp_width, 6))

        # debug: draw enemy attack hitbox when attacking
        if self.state == self.ATTACK:
            attack_rect = self.get_attack_rect()
            pygame.draw.rect(screen, YELLOW_COLOR,
                    (attack_rect.x - camera_x, attack_rect.y,
                    attack_rect.width, attack_rect.height), 1)

    def apply_world_bounds(self):
        # world boundaries
        self.x = max(0, self.x) # cannot go left of window
        self.x = min(self.x, WORLD_WIDTH-self.width) # cannot go right window
        # beat'em up lane limits creates the illusion of depth
        # player walks on a horizontal strip, not full screen
        self.y = max(self.lane_top, self.y) # cannot go above lane_top
        self.y = min(self.lane_bottom, self.y) # cannot go below lane_bottom

    # hit box
    def get_attack_rect(self):
        # Use symmetric hitbox size and offsets so left/right behave identically
        hit_w = self.attack_hitbox_w
        # giving running attack a longer hitbox
        #if self.state == self.RUN_ATTACK:
        #    hit_w = self.attack_hitbox_w * 1.5
        hit_h = self.attack_hitbox_h
        #if self.weapon and not self.weapon.is_ranged:
        #    hit_w += self.weapon.attack_range_bonus
        #    hit_h += self.weapon.attack_height_bonus

        hit_y = int(self.y + self.attack_hitbox_offset_y)
        # do we need attack hitbox_offset_x ? no need probably
        if self.facing_right:
            hit_x = int(self.x + self.width)
        else:
            hit_x = int(self.x - hit_w)
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
            player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
            if attack_rect.colliderect(player_rect):
                player.take_damage(self.attack_damage)
                self.attack_has_hit = True
        
        if self.attack_timer >= self.attack_total_duration:
            self.state = self.IDLE
            self.attack_timer = 0
            self.attack_has_hit = False
            self.attack_cooldown = ENEMY_ATTACK_COOLDOWN
        
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
            self.animation_manager.play(self.HIT)
        elif self.state == self.KNOCKDOWN:
            self.animation_manager.play(self.HIT)

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
