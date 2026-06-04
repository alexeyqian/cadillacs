import random
import pygame
from game.animation.animation import Animation
from game.animation.animation_manager import AnimationManager
from game.animation.asset_loader import AssetLoader
from game.animation.animation_config import *
from game.animation.file_utils import *
from game.assets.placeholder.enemy_frames import *
from game.assets.placeholder.player_frames import create_hit_frames
from game.settings import *
from game.entities.loot import Loot

class Enemy:
    IDLE = "IDLE"
    PATROL = "PATROL"
    WALK = "WALK" # will remove in future
    CHASE = "CHASE"
    ATTACK = "ATTACK"
    HIT = "HIT"
    DEAD = "DEAD"

    def __init__(self, x, y, walk_config=None, attack_config=None,
                fallback_frame_factory=None):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 80
        self.speed = 2
        self.max_hp = 100
        self.hp = self.max_hp
        self.state = self.WALK
        self.loot_generated = False

        # within this range, enemy chases player
        # outside this range, enemy ignores player
        self.detect_range = 250
        # enemy remembers where it spawned
        self.spawn_x = x
        self.patrol_distance = 80
        self.patrol_direction = 1

        # attack players / combat
        self.attack_timer = 0 # ?
        self.attack_cooldown = 0
        self.attack_damage = 10
        self.attack_range = ENEMY_HITBOX_W

        # hit reaction
        self.knockback_velocity = 0
        # enemy gets briefly white when hit by player
        self.hit_timer = 0
        
        #lane boundaries
        self.lane_top = LANE_TOP
        self.lane_bottom = LANE_BOTTOM
        
        if walk_config is None:
            walk_config = NORMAL_ENEMY_WALK
        if attack_config is None:
            attack_config = NORMAL_ENEMY_ATTACK
        if fallback_frame_factory is None:
            fallback_frame_factory = create_enemy_frames

        # assets loader
        if file_exists(walk_config["file"]):
            walk_frames = AssetLoader.load_animation(
                    walk_config["file"],
                    walk_config["frame_width"],
                    walk_config["frame_height"],
                    walk_config["frame_count"]
                )
        else:
            walk_frames = fallback_frame_factory()

        if file_exists(attack_config["file"]):
            attack_frames = AssetLoader.load_animation(
                    attack_config["file"],
                    attack_config["frame_width"],
                    attack_config["frame_height"],
                    attack_config["frame_count"]
                )
        else:
            attack_frames = fallback_frame_factory()

        # animation manager
        self.animation_manager = AnimationManager()
        # compute frame durations to match game FPS
        walk_dur = max(1, int(FPS / ANIM_FPS_WALK_ENEMY))
        attack_dur = max(1, int(FPS / ANIM_FPS_ATTACK_ENEMY))
        hit_dur = max(1, int(FPS / ANIM_FPS_HIT_ENEMY))
        self.animation_manager.add_animation(
            self.WALK, Animation(walk_frames, walk_dur))
        self.animation_manager.add_animation(
            self.ATTACK, Animation(attack_frames, attack_dur))
        self.animation_manager.add_animation(
            self.HIT, Animation(fallback_frame_factory(), hit_dur))
        self.animation_manager.add_animation(
            self.DEAD, Animation(fallback_frame_factory(), 999))

    def update(self, player, enemies):
        if self.state == self.DEAD:
            return

        # attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # hit state
        # enemy pauses briefly when hit by player, but can still be knocked back
        if self.hit_timer > 0:
            self.hit_timer -= 1
            self.apply_knockback()
            if self.hit_timer == 0:
                self.state = self.WALK
            return
        # apply any remaining knockback
        self.apply_knockback()

        # distance to player
        dx = player.x - self.x
        dy = player.y - self.y
        distance_x = abs(dx)
        distance_y = abs(dy)

        # state selection
        # attack if close enough
        if distance_x <= self.attack_range and distance_y <= self.attack_range:
            self.state = self.ATTACK
        elif distance_x <= self.detect_range:
            self.state = self.CHASE
        else:
            self.state = self.PATROL

        # execute state
        if self.state == self.PATROL:
            self.update_patrol()
        elif self.state == self.CHASE:
            self.update_walking(dx, dy)
            self.separate_from_other_enemies(enemies)
        elif self.state == self.ATTACK:
            self.update_attack(player)

        self.update_animation()

    def draw(self, screen, camera_x):
        screen_x = self.x - camera_x
        # shadow
        pygame.draw.ellipse(
            screen, (50, 50, 50),
            (
                screen_x,
                self.y + self.height - 10,
                self.width,
                12
            )
        )

        image = self.animation_manager.get_image()
        image = pygame.transform.scale(image, (self.width, self.height))
        # Center the scaled image inside the enemy bounding box so it visually aligns
        img_w, img_h = image.get_size()
        blit_x = screen_x + (self.width - img_w) // 2
        blit_y = self.y + (self.height - img_h) // 2
        screen.blit(image, (blit_x, blit_y))

        # debug: draw enemy bounding box (world -> screen)
        pygame.draw.rect(screen, (255, 0, 255), (screen_x, self.y, self.width, self.height), 2)

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
            # represent attack area using attack_range centered in front of enemy
            hit_w = int(self.attack_range)
            hit_h = max(20, int(self.height / 2))
            hit_y = int(self.y + 10)
            # center attack box on enemy horizontally
            hit_x = int(self.x + (self.width / 2) - (hit_w / 2))
            pygame.draw.rect(screen, (255, 165, 0), (hit_x - camera_x, hit_y, hit_w, hit_h), 2)

    def update_walking(self, dx, dy):
        #if dx <= 60:
        #    return # stop near player

        # horizontal movement
        if dx > 0:
            self.x += self.speed
        elif dx < 0:
            self.x -= self.speed
        # vertical movement
        if abs(dy) > 10: # allow some vertical leniency
            if dy > 0:
                self.y += self.speed
            else:
                self.y -= self.speed

        # Keep enemy inside lane
        self.y = max(self.lane_top, self.y)
        self.y = min(self.lane_bottom, self.y)

    # enemy patrol back and forth
    def update_patrol(self):
        self.x += self.patrol_direction
        if self.x > self.spawn_x + self.patrol_distance:
            self.patrol_direction -= 1
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

    def update_attack(self, player):
        if self.attack_cooldown > 0:
            return
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

        if self.hp <= 0:
            self.hp = 0
            self.state = self.DEAD

    def apply_knockback(self):
        if self.knockback_velocity == 0:
            return
        self.x += self.knockback_velocity
        # friction slows down knockback over time
        self.knockback_velocity *= 0.8
        if abs(self.knockback_velocity) < 0.5:
            self.knockback_velocity = 0

    def update_animation(self):
        if self.state == self.DEAD:
            self.animation_manager.play(self.DEAD)
        elif self.state == self.HIT:
            self.animation_manager.play(self.HIT)
        elif self.state == self.ATTACK:
            self.animation_manager.play(self.ATTACK)
        elif self.state == self.WALK:
            self.animation_manager.play(self.WALK)
        elif self.state == self.PATROL:
            self.animation_manager.play(self.WALK)
        elif self.state == self.CHASE:
            self.animation_manager.play(self.WALK)

        self.animation_manager.update()
        
    def create_loot(self):
        roll = random.randint(1, 100)
        if roll <= 30:
            return Loot(self.x, self.y, "health")
        elif roll <= 50:
            return Loot(self.x, self.y, "ammo")

        return None
        
