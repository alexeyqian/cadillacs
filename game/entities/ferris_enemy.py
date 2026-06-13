import pygame

from game.animation.ferris_data import *
from game.animation.frame_animation import FrameAnimation, load_frame_animation
from game.entities.basic_melee_enemy import BasicMeleeEnemy
from game.settings import *
from game.colors import *

class FerrisEnemy(BasicMeleeEnemy):
    def __init__(self, x, y):
        super().__init__(x, y, "ferris")
        self.sprite_scale = 4
        self.init_ferris_frame_animations()
        
    def init_ferris_frame_animations(self):
        idle_frames = load_frame_animation(FERRIS_ANIMATIONS, "idle")
        walk_frames = load_frame_animation(FERRIS_ANIMATIONS, "walk")
        attack_frames = load_frame_animation(FERRIS_ANIMATIONS, "attack")
        hit_frames = load_frame_animation(FERRIS_ANIMATIONS, "hit")
        dead_frames = load_frame_animation(FERRIS_ANIMATIONS, "dead")
        # todo: game frame duration for single sprite frame? or idle sprite frames
        # Answer: for single sprite frame
        idle_dur = max(1, int(FPS/ANIM_FPS_IDLE_ENEMY_FERRIS))
        walk_dur = max(1, int(FPS/ANIM_FPS_WALK_ENEMY_FERRIS))
        attack_dur = max(1, int(FPS/ANIM_FPS_ATTACK_ENEMY_FERRIS))
        hit_dur = max(1, int(FPS/ANIM_FPS_HIT_ENEMY_FERRIS))
        dead_dur = max(1, int(FPS/ANIM_FPS_DEAD_ENEMY_FERRIS))
    
        self.animation_manager.add_animation(self.IDLE,
                FrameAnimation(idle_frames, idle_dur))
        self.animation_manager.add_animation(self.WALK,
                FrameAnimation(walk_frames, walk_dur))
        self.animation_manager.add_animation(self.IDLE,
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
    
    def get_frame_rect(self):
        frame = self.get_current_frame_data()
        if not frame: # for old logic compatibility
            return super().get_logical_rect()
        scale = self.sprite_scale
        offset_x, offset_y = frame.offset
        frame_w = frame.image.get_width()*scale
        frame_h = frame.image.get_height()*scale
        offset_x *= scale
        offset_y *= scale
        # Enemy art currently follows Enemy.draw() convention:
        # source art faces left, and is flipped when facing_right is True.
        if self.facing_right:
            world_x = self.x - frame_w - offset_x
        else: 
            world_x = self.x + offset_x
            
        world_y = self.y + offset_y
        return pygame.Rect(int(world_x), int(world_y), int(frame_w), int(frame_h))
    
    def get_logical_rect(self):
        return self.get_frame_rect()
    
    def get_hurt_rect(self):
        frame = self.get_current_frame_data()
        if not frame: # for old logic compatibility
            return super().get_hurt_rect()
        scale = self.sprite_scale
        local_x, local_y, w, h = frame.hurt_rect
        offset_x, offset_y = frame.offset
        frame_w = frame.image.get_width()
        
        local_x *= scale
        local_y *= scale
        w *= scale
        h *= scale
        offset_x *= scale
        offset_y *= scale
        frame_w *= scale
        
        if self.facing_right:
            mirrored_x = self.x - frame_w - offset_x
            world_x = self.x - frame_w - offset_x + mirrored_x
        else:
            world_x = self.x + offset_x + local_x
            
        world_y = self.y + offset_y + local_y
        return pygame.Rect(int(world_x), int(world_y), int(w), int(h))
    
    def get_attack_rect(self):
        frame = self.get_current_frame_data()

        if frame:
            if not frame.attack_rect:
                return None

            scale = self.sprite_scale

            local_x, local_y, w, h = frame.attack_rect
            offset_x, offset_y = frame.offset
            frame_w = frame.image.get_width()

            local_x *= scale
            local_y *= scale
            w *= scale
            h *= scale
            offset_x *= scale
            offset_y *= scale
            frame_w *= scale

            if self.facing_right:
                mirrored_x = frame_w - local_x - w
                world_x = self.x - frame_w - offset_x + mirrored_x
            else:
                world_x = self.x + offset_x + local_x

            world_y = self.y + offset_y + local_y

            return pygame.Rect(
                int(world_x),
                int(world_y),
                int(w),
                int(h)
            )

        return super().get_attack_rect()

    def draw(self, screen, camera_x):
        frame = self.get_current_frame_data()

        if not frame:
            super().draw(screen, camera_x)
            return

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

        if self.facing_right:
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

        hp_width = int(50 * (self.hp / self.max_hp))
        hp_height = 12
        pygame.draw.rect(
            screen,
            (120, 120, 120),
            (frame_rect.x - camera_x, frame_rect.y - hp_height, 50, 6)
        )
        pygame.draw.rect(
            screen,
            (255, 0, 0),
            (frame_rect.x - camera_x, frame_rect.y - hp_height, hp_width, 6)
        )