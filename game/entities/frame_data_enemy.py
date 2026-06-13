import pygame

from game.entities.enemy import Enemy
from game.animation.frame_animation import *
from game.settings import *
from game.colors import *
from game.entities.enemy_config import get_enemy_config


class FrameDataEnemy(Enemy):
    def __init__(self, x, y, enemy_type, animation_data, anim_fps, sprite_scale=4):
        super().__init__(x, y, enemy_type,
            enemy_config=get_enemy_config(enemy_type),
            load_legacy_animations=False)
        self.animation_data = animation_data
        self.anim_fps = anim_fps
        self.sprite_scale = sprite_scale
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
    
    def get_frame_rect(self):
        frame = self.get_current_frame_data()
        if not frame:
            raise ValueError(f"Missing frame data for enemy state: {self.state}")
        scale = self.sprite_scale
        offset_x, offset_y = frame.offset
        frame_w = frame.image.get_width()*scale
        frame_h = frame.image.get_height()*scale
        offset_x *= scale
        offset_y *= scale
        if self.facing_right:
            world_x = self.x + offset_x
        else: 
            world_x = self.x - frame_w - offset_x
            
        world_y = self.y + offset_y
        return pygame.Rect(int(world_x), int(world_y), int(frame_w), int(frame_h))
    
    def get_logical_rect(self):
        return self.get_frame_rect()
    
    def get_hurt_rect(self):
        frame = self.get_current_frame_data()
        if not frame or not frame.hurt_rect:
            return pygame.Rect(int(self.x), int(self.y), 0, 0)
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
            world_x = self.x + offset_x + local_x
        else:
            mirrored_x = frame_w - local_x - w
            world_x = self.x - frame_w - offset_x + mirrored_x
            
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
                world_x = self.x + offset_x + local_x
            else:
                mirrored_x = frame_w - local_x - w
                world_x = self.x - frame_w - offset_x + mirrored_x

            world_y = self.y + offset_y + local_y

            return pygame.Rect(
                int(world_x),
                int(world_y),
                int(w),
                int(h)
            )

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
