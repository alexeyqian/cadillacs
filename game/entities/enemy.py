import pygame
from game.animation.animation import Animation
from game.animation.animation_manager import AnimationManager
from game.animation.asset_loader import AssetLoader
from game.animation.animation_config import *
from game.animation.file_utils import *
from game.assets.placeholder.enemy_frames import *
from game.assets.placeholder.player_frames import create_hit_frames

class Enemy:
    IDLE = "IDLE"
    WALK = "WALK"
    ATTACK = "ATTACK"
    HIT = "HIT"
    DEAD = "DEAD"

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 80
        self.speed = 2
        self.hp = 100
        self.state = self.WALK

        # attack players / combat
        self.attack_timer = 0 # ?
        self.attack_cooldown = 0
        self.attack_damage = 10
        self.attack_range = 70

        # hit reaction
        self.knockback_velocity = 0
        # enemy gets briefly white when hit by player
        self.hit_timer = 0

        # assets loader
        if file_exists(ENEMY_WALK["file"]):
            walk_frames = AssetLoader.load_animation(
                    ENEMY_WALK["file"],
                    ENEMY_WALK["frame_width"],
                    ENEMY_WALK["frame_height"],
                    ENEMY_WALK["frame_count"]
                )
        else:
            walk_frames = create_enemy_frames()

        if file_exists(ENEMY_ATTACK["file"]):
            attack_frames = AssetLoader.load_animation(
                    ENEMY_ATTACK["file"],
                    ENEMY_ATTACK["frame_width"],
                    ENEMY_ATTACK["frame_height"],
                    ENEMY_ATTACK["frame_count"]
                )
        else:
            attack_frames = create_enemy_frames()

        # animation manager
        self.animation_manager = AnimationManager()
        self.animation_manager.add_animation(
            self.WALK, Animation(walk_frames,12))
        self.animation_manager.add_animation(
            self.ATTACK,Animation(attack_frames,5))
        self.animation_manager.add_animation(
            self.HIT,Animation(create_enemy_frames(),3))

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

        # state selection
        # attack if close enough
        if distance_x <= self.attack_range:
            self.state = self.ATTACK
        else:
            self.state = self.WALK

        # execute state
        if self.state == self.WALK:
            #self.current_animation = self.animations[self.WALK]
            self.update_walking(dx, dy)
            self.separate_from_other_enemies(enemies)
        elif self.state == self.ATTACK:
            #self.current_animation = self.animations[self.ATTACK]
            self.update_attack(player)

        # 1 attack per second at 60 FPS
        if self.state == self.ATTACK:
            if self.attack_cooldown == 0:
                player.take_damage(20)
                self.attack_cooldown = 60

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
        # Real sprites are often larger than gameplay hitboxes.
        image = pygame.transform.scale(image,(self.width, self.height))
        screen.blit(image, (screen_x, self.y))

        # debug: draw enemy bounding box (world -> screen)
        pygame.draw.rect(screen, (255, 0, 255), (screen_x, self.y, self.width, self.height), 2)

        # health bar background
        pygame.draw.rect(
            screen, (120, 120, 120),
            (screen_x, self.y - 12, 50, 6))
        # health bar
        hp_width = int(50 * (self.hp / 100))
        pygame.draw.rect(
            screen, (255, 0, 0),
            (screen_x, self.y - 12, hp_width, 6))

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
        self.y = max(250, self.y)
        self.y = min(450, self.y)

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

        self.animation_manager.update()
