Core boxes:

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
