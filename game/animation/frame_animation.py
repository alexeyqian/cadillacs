from dataclasses import dataclass
from typing import Optional

import pygame

@dataclass
class FrameData:
    image: pygame.Surface
    offset: tuple
    hurt_rect: Optional[tuple]
    # This is the foundation for real counter-hit. 
    # The idea is: during an attack, 
    # the player’s extended arm can be vulnerable without making the whole attack box count as body damage.
    counter_hurt_rect: Optional[tuple] = None

class FrameAnimation:
    def __init__(self, frames, frame_duration=8, loop=True):
        self.frames = frames
        self.frame_duration = frame_duration
        self.current_frame = 0
        self.timer = 0
        # add one-shot animation support, then use it for enemy attacks.
        self.loop = loop
    
    # Enemy attack animation plays once
    # Enemy holds final attack/follow through frame during remaining recovery
    # Animation no longer loops while attack_timer is still running
    def update(self):
        self.timer += 1
        if self.timer < self.frame_duration:
            return

        self.timer = 0
        self.current_frame += 1

        if self.current_frame < len(self.frames):
            return

        if self.loop:
            self.current_frame = 0
        else:
            self.current_frame = len(self.frames) - 1

    def get_image(self):
        return self.frames[self.current_frame].image
    
    def get_frame_data(self):
        return self.frames[self.current_frame]
    
    def get_frame_index(self):
        return self.current_frame
    
    def reset(self):
        self.current_frame = 0
        self.timer = 0
        
def load_frame_animation(animation_data, animation_key):
    config = animation_data.get(animation_key)
    if not config:
        raise ValueError(f"Missing frame animation data: {animation_key}")
    
    sheet = pygame.image.load(config["file"]).convert_alpha()
    frames = []
    for frame_config in config["frames"]:
        
        frame_x, frame_y, frame_w, frame_h = frame_config["frame_rect"]
        image = pygame.Surface((frame_w, frame_h), pygame.SRCALPHA)
        image.blit(sheet, (0,0),(frame_x, frame_y, frame_w, frame_h))

        frames.append(FrameData(
            image=image,
            offset=frame_config["offset"],
            hurt_rect = frame_config.get("hurt_rect"),
            counter_hurt_rect=frame_config.get("counter_hurt_rect")))
    if not frames:
        raise ValueError(f"No frames loaded for animation: {animation_key}")
    
    return frames
