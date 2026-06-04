#!/usr/bin/env python3
"""
Generate simple, original sprite sheets for the player (inspired by a yellow-pants hero)
and a box image for breakable objects.

This script creates the following files (matching animation_config paths):
- game/assets/player/player_idle.png  (4 frames, 80x100)
- game/assets/player/player_walk.png  (6 frames, 80x100)
- game/assets/player/player_attack.png (4 frames, 80x100)
- game/assets/objects/box.png          (50x50)

Run: pip install pillow && python tools/generate_sprites.py

The generated art is original, simple pixel-style artwork (not a copy of any existing commercial art).
"""

from PIL import Image, ImageDraw
import os

# match sizes used in animation_config
FRAME_W = 80
FRAME_H = 100

OUT_IDLE = "game/assets/player/player_idle.png"
OUT_WALK = "game/assets/player/player_walk.png"
OUT_ATTACK = "game/assets/player/player_attack.png"
OUT_BOX = "game/assets/objects/box.png"

IDLE_FRAMES = 4
WALK_FRAMES = 6
ATTACK_FRAMES = 4

def ensure_dir(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)

# simple function to draw a single stylized hero into an ImageDraw at given offsets
def draw_hero(draw, ox, oy, frame_idx, action):
    # anchor: ox, oy is top-left of frame
    # feet baseline
    feet_y = oy + FRAME_H - 10
    cx = ox + FRAME_W // 2

    # colors
    skin = (255, 200, 150)
    pants = (235, 200, 20)   # yellow pants
    shirt = (40, 90, 170)
    boot = (40, 30, 20)
    hair = (40, 25, 10)
    hat = (120, 30, 20)

    # head
    head_w, head_h = 18, 18
    head_x = cx - head_w // 2
    head_y = feet_y - 60
    draw.rectangle([head_x, head_y, head_x + head_w, head_y + head_h], fill=skin)
    # hair/hat simple
    if action == 'idle':
        # small hat
        draw.polygon([(head_x-2, head_y+2), (head_x+head_w+2, head_y+2), (cx, head_y-6)], fill=hat)
    else:
        draw.rectangle([head_x, head_y-2, head_x+head_w, head_y+2], fill=hair)

    # body
    body_w, body_h = 22, 28
    body_x = cx - body_w // 2
    body_y = head_y + head_h
    draw.rectangle([body_x, body_y, body_x + body_w, body_y + body_h], fill=shirt)

    # pants
    pants_h = 16
    pants_y = body_y + body_h
    draw.rectangle([body_x, pants_y, body_x + body_w, pants_y + pants_h], fill=pants)

    # boots
    boot_w, boot_h = 8, 10
    # walking/idle leg offsets
    if action == 'walk':
        phase = frame_idx % 2
        left_leg_dx = -4 if phase == 0 else 2
        right_leg_dx = 2 if phase == 0 else -4
    elif action == 'attack':
        left_leg_dx = -2
        right_leg_dx = 2
    else:
        left_leg_dx = -1
        right_leg_dx = 1

    left_boot_x = cx - 10 + left_leg_dx
    right_boot_x = cx + 2 + right_leg_dx
    boot_y = pants_y + pants_h - boot_h + 2
    draw.rectangle([left_boot_x, boot_y, left_boot_x + boot_w, boot_y + boot_h], fill=boot)
    draw.rectangle([right_boot_x, boot_y, right_boot_x + boot_w, boot_y + boot_h], fill=boot)

    # arms
    arm_w, arm_h = 6, 18
    if action == 'attack':
        # attack: right arm extended
        draw.rectangle([body_x - arm_w, body_y + 6, body_x - arm_w + arm_w, body_y + 6 + arm_h], fill=shirt)
        draw.rectangle([body_x + body_w, body_y + 2, body_x + body_w + 18, body_y + 2 + 8], fill=(160, 110, 70))
    else:
        # idle/walk: arms swinging
        arm_swing = -6 if (frame_idx % 2 == 0) else 6
        draw.rectangle([body_x - arm_w + arm_swing//4, body_y + 4, body_x - arm_w + arm_w + arm_swing//4, body_y + 4 + arm_h], fill=shirt)
        draw.rectangle([body_x + body_w + arm_swing//4, body_y + 4, body_x + body_w + arm_w + arm_swing//4, body_y + 4 + arm_h], fill=shirt)

    # simple shadow
    draw.ellipse([cx - 18, feet_y + 2, cx + 18, feet_y + 12], fill=(30,30,30))


def make_spritesheet(frames, out_path, action):
    ensure_dir(out_path)
    sheet = Image.new('RGBA', (FRAME_W * frames, FRAME_H), (0,0,0,0))
    draw_sheet = ImageDraw.Draw(sheet)
    for i in range(frames):
        # draw onto a temporary image for clarity
        frame = Image.new('RGBA', (FRAME_W, FRAME_H), (0,0,0,0))
        d = ImageDraw.Draw(frame)
        draw_hero(d, 0, 0, i, action)
        sheet.paste(frame, (i * FRAME_W, 0), frame)
    sheet.save(out_path)
    print(f"Wrote {out_path}")


def make_box(out_path):
    ensure_dir(out_path)
    w = 50
    h = 50
    img = Image.new('RGBA', (w,h), (0,0,0,0))
    d = ImageDraw.Draw(img)
    # base wood
    base = (160, 100, 40)
    d.rectangle([0,0,w,h], fill=base)
    # planks
    for y in range(5, h-5, 8):
        d.line([(5,y),(w-5,y)], fill=(120,70,20), width=3)
    # border
    d.rectangle([1,1,w-2,h-2], outline=(80,40,10), width=2)
    # slight top highlight
    d.rectangle([4,4,w-5,10], fill=(200,150,80))
    img.save(out_path)
    print(f"Wrote {out_path}")

if __name__ == '__main__':
    make_spritesheet(IDLE_FRAMES, OUT_IDLE, 'idle')
    make_spritesheet(WALK_FRAMES, OUT_WALK, 'walk')
    make_spritesheet(ATTACK_FRAMES, OUT_ATTACK, 'attack')
    make_box(OUT_BOX)
    print('Done. Please run the game to verify art alignment and tweak if needed.')
