
# WINDOW SIZE 960X540
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 540

GROUND_TOP = 300
GROUND_BOTTOM = 520
GROUND_HEIGHT = GROUND_BOTTOM - GROUND_TOP  # 220

LANE_COUNT = 5
LANE_HEIGHT = GROUND_HEIGHT / LANE_COUNT  # 44 px
lanes = [
    322,
    366,
    410,
    454,
    498,
]
lane_y = GROUND_TOP + LANE_HEIGHT * lane_index + LANE_HEIGHT / 2

y = 0
+--------------------------------+
| background / buildings / sky   |
|                                |
|                                |
|                                |
y = 300  <- GROUND_TOP
+--------------------------------+
| walkable beat'em up area       |
|                                |
| player feet move here          |
|                                |
y = 520  <- GROUND_BOTTOM
+--------------------------------+
| small UI / screen edge margin  |
y = 540

# WINDOW SIZE 1920X1080
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

PLAYER_WIDTH = 128
PLAYER_HEIGHT = 256

GROUND_TOP = 600
GROUND_BOTTOM = 1040
GROUND_HEIGHT = 440

LANE_COUNT = 5
LANE_HEIGHT = 88

lanes = [
    644,
    732,
    820,
    908,
    996,
]
lane_y = GROUND_TOP + LANE_HEIGHT * lane_index + LANE_HEIGHT / 2

y = 0
+--------------------------------+
| background / buildings / sky   |
|                                |
|                                |
|                                |
y = 600  <- GROUND_TOP
+--------------------------------+
| walkable combat area           |
|                                |
| player feet move here          |
|                                |
y = 1040 <- GROUND_BOTTOM
+--------------------------------+
| 40 px bottom margin            |
y = 1080

# Player Core boxes:

body_rect: movement, standing position, pushing, world collision
hurtbox: where the player can be damaged
attack_hitbox: temporary damage area during attacks
Useful future boxes:

pickup_rect: slightly larger area around the player for collecting weapons, food, ammo, etc.
interaction_rect: area for opening doors, breaking crates, talking, pressing switches
throw_box or grab_box: short-range area in front of the player for grabs/throws
feet_rect or ground_rect: tiny box near the feet for sorting depth, checking stage bounds, or deciding “same lane”
sprite_rect: visual drawing rectangle only, often bigger than the collision body because the sprite includes arms, hair, weapon swing frames, etc.

sprite_rect      = what gets drawn
body_rect        = where player physically exists
hurtbox          = where player can be damaged
attack_hitbox    = where player deals damage
pickup_rect      = forgiving loot collection area


Think of the player as having 3 different rectangles:
 1. Body / collision box (where feet/body block movement)
   Where the player stands and collides.
 2. Hurtbox
   Where the player can receive damage.
 3. Attack hitbox
   Temporary area where fist/kick can hit enemy.

 For this kind of beat’em up, I’d design the 
 player hurtbox as a slightly smaller rectangle centered inside the body/collision box most of the time.
 Sprite art: virtual box, extend depends on action
 wide, includes arms, hair, jacket, animation smear

 The body sprite frame can still be larger than 80×160 during attack.
Idle frame:
[ 80 wide body ]
Punch frame:
[ 80 body ][ arm + fist extends 40 px ]
 So the actual animation frame could be:
 PLAYER_ATTACK_FRAME_W = 120
 PLAYER_ATTACK_FRAME_H = 160
 But the logical body size remains:
 Do not make PLAYER_W bigger just because the fist extends.

The most important distinction: do not let the sprite size become the gameplay size. In beat’em ups, sprites are often visually big and expressive, but collision should stay smaller and predictable.


Logic Box vs Sprite Frame
Do not make the logic box equal to the whole visible sprite canvas unless your game is very simple.

Better separation:
sprite frame: 128x256
logical body box: movement/position anchor
collision box: feet/lane collision
hurt box: damageable body area
attack box: active punch/kick area