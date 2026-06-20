import pygame
from game.colors import WHITE_COLOR
from game.settings import PLAYER_H, PLAYER_W

def make_frame(body_color, head_color, leg_offset):
    image = pygame.Surface((PLAYER_W, PLAYER_H), pygame.SRCALPHA)
    # head
    pygame.draw.circle(image, head_color, (25,12),10)
    # body
    pygame.draw.rect(image, body_color, (10,22,30,30))
    # legs
    pygame.draw.rect(image, body_color, (12,52,8,20+leg_offset))
    pygame.draw.rect(image, body_color, (30,52,8,20-leg_offset))

    return image

def create_idle_frames():
    return [make_frame((220,40,40),(255,220,180),0)]

def create_walk_frames():
    return [
        make_frame((220,40,40),(255,220,180),5),
        make_frame((220,40,40),(255,220,180),-5),
    ]

def create_run_frames():
    return create_walk_frames() # todo: later
    
def create_jump_frames():
    return create_walk_frames() # todo: later

def create_attack_frames():
    frame1 = make_frame((225,120,0),(255,220,180),0)
    pygame.draw.rect(frame1, (255,255,0),(40,30,10,5))
    
    frame2 = make_frame((225,180,0),(255,220,180),0)
    pygame.draw.rect(frame2, (255,255,0),(40,20,10,15))

    return [frame1, frame2]

def create_run_attack_frames():
    return create_attack_frames() # todo: later

def create_jump_attack_frames():
    return create_attack_frames() # todo: later

def create_grab_frames():
    return create_attack_frames() # todo: later

def create_throw_frames():
    return create_attack_frames() # todo: later

def create_hit_frames():
    return [make_frame(WHITE_COLOR,WHITE_COLOR,0)]

def create_dead_frames():
    image = pygame.Surface((PLAYER_H,PLAYER_W),pygame.SRCALPHA)
    pygame.draw.rect(image,(80,80,80),(0,20,60,20))
    return [image]
