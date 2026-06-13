from dataclasses import dataclass
from typing import Optional

import pygame

@dataclass
class FrameData:
    image: pygame.Surface
    offset: tuple
    hurt_rect: Optional[tuple]
    attack_rect: Optional[tuple]
    
class FrameAnimation:
    def __init__(self, frames, frame_duration=8):
        self.frames = frames
        self.frame_duration = frame_duration
        self.current_frame = 0
        self.timer = 0