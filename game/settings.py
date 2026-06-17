FPS=60
# external window width: for real monitor/display
EXTERNAL_WIDTH=1920
EXTERNAL_HEIGHT=1080
# internal window width: for entire game area
SCREEN_WIDTH=1920
SCREEN_HEIGHT=1080

# Classical Proportions (Artistic & Anatomical)
# Width-to-height ratio: 1:4 ratio
# Biacromial width: 46.25 cm
# Head height units: 2 full heads wide
# height: 185 cm, shoulder: 46.25cm
# height: 182 cm, shoulder: 45.5cm
# height: 180 cm, shoulder: 45cm

# PLAYER_NAKED_HEIGHT=185
# PLAYER_NAKED_WIDTH=47

# PLAYER_IDLE_FRAME_H=185
# PLAYER_IDLE_FRAME_W=47
# 

# Important: feet alignment matters most.anchor by feet, not by image center.
# Across idle, walk, attack, hit, etc., 
# the player’s feet should land on the same baseline. 
# For example:
# PLAYER_SPRITE_BASELINE_Y = 232
# frame baseline y = 232 inside the 256 px frame
# the player feet should land on center of collision box
# player logical box, mostly for anchoring
# visible idle body should be smaller, 
# leave margin between visible body and logical player box
# COLLISION UNIT is the fundamental unit in game
PLAYER_W=int(128) # equals player shoulder width = COLLISION UNIT
PLAYER_H=int(256)
# walkable area height
# todo: rename to GROUD_TOP and GROUND_BOTTOM
LANE_TOP=600-PLAYER_H
LANE_BOTTOM = 1040-PLAYER_H
#GROUND_HEIGHT=GROUND_BOTTOM - GROUND_TOP

# total stage width, should around 3 screens
WORLD_WIDTH=SCREEN_WIDTH*4
PLAYER_SCREEN_EDGE_MARGIN=80

UI_FIRST_X=32
UI_FIRST_Y=32
UI_FONT_SIZE=36

# Design note for the overlay colors:
# blue  = collision/footprint box
# green = hurtbox
# red   = attack hitbox
# orange = counter-hurtbox / extended limb vulnerability
# yellow = active enemy attack timing indicator
# module import is the right choice for mutable runtime flags.
SHOW_COMBAT_BOXES=False
SHOW_EXIT_RECT=True

PLAYER_LIVES=3

######## sizes ########
ENEMY_W=PLAYER_W
ENEMY_H=PLAYER_H

######## collision, hurt and hit/attack boxes ########
# collision box is centered on bottom
PLAYER_COLLISION_W = PLAYER_W
PLAYER_COLLISION_H = int(PLAYER_H * 0.2)

ENEMY_COLLISION_W = int(ENEMY_W)
ENEMY_COLLISION_H = int(ENEMY_H * 0.2)

######## hp max ########
PLAYER_MAX_HP=100
ENEMY_MAX_HP=int(PLAYER_MAX_HP*0.6)
# enemy projectile
RANGED_ENEMY_MAX_HP=int(ENEMY_MAX_HP*1.2)
RAPTOR_ENEMY_MAX_HP=int(ENEMY_MAX_HP*1.2)
BOSS_ENEMY_MAX_HP=int(ENEMY_MAX_HP*10)

ENEMY_SCORE_POINTS = 100

######## speed ########
PLAYER_SPEED=7
PLAYER_RUN_SPEED=PLAYER_SPEED*2
RUN_DOUBLE_TAP_TIME=0.25
ATTACK_3_FORWARD_NUDGE_FRAMES=3
ATTACK_3_FORWARD_NUDGE_SPEED_SCALE=0.35
RUN_ATTACK_REQUIRED_DISTANCE=100
RUN_ATTACK_FULL_POWER_DISTANCE=240
RUN_ATTACK_MOMENTUM_FRAMES=18
RUN_ATTACK_MOMENTUM_SPEED_SCALE=0.85
RUN_ATTACK_LANDING_RECOVERY=4
RUN_ATTACK_BASE_KNOCKBACK=18
RUN_ATTACK_FULL_POWER_KNOCKBACK_BONUS=6
RUN_ATTACK_BASE_ENEMY_HIT_STUN=40
RUN_ATTACK_FULL_POWER_ENEMY_HIT_STUN_BONUS=6

ENEMY_SPEED=PLAYER_SPEED*0.5
RAPTOR_ENEMY_SPEED=ENEMY_SPEED*1.3
BOSS_ENEMY_SPEED=ENEMY_SPEED*0.5
PROJECTILE_SPEED=ENEMY_SPEED*4
BOSS_SPECIAL_ATTACK_WARNING_DURATION=45

######## ranges ########
PLAYER_GRAB_RANGE = int(PLAYER_W * 0.4)
ENEMY_DETECT_RANGE=SCREEN_WIDTH*0.50

######## enemy attack timing ########
# windup:prepare -> active attack (hit player once) 
# -> recovery (enemy cannot move)->cooldown(frame cooldown before next attack)
ENEMY_ATTACK_DELAY=20
ENEMY_ATTACK_WINDUP=20 
ENEMY_ATTACK_ACTIVE=8
ENEMY_ATTACK_RECOVERY=25
ENEMY_ATTACK_COOLDOWN=45
ENEMY_ATTACK_CLASH_RECOVERY_DURATION=12
ENEMY_ATTACK_CLASH_COOLDOWN_DURATION=20
# Only a small number of regular melee enemies should enter ATTACK at the same time.
MAX_MELEE_ATTACKERS = 2
ENEMY_FLANK_OFFSET_X = 120
# avoid multiple enemies stack on the same lane. 
# give flankers a small Y offset based on crowding.
ENEMY_FLANK_OFFSET_Y = 36
ENEMY_FLANK_DECISION_DURATION = 45
ENEMY_FLANK_Y_TOLERANCE = 18

######## damages ########
# player attack damage
# melee weapons
FIST_DAMAGE=10
KNIFE_DAMAGE=int(FIST_DAMAGE*1.5)
BAT_DAMAGE=int(FIST_DAMAGE*2)
THROWN_DAMAGE=int(FIST_DAMAGE*1.5)
######## grab combo ########
PLAYER_GRAB_KNEE_DURATION = 14
PLAYER_GRAB_KNEE_HIT_FRAME = 6
# range weapons
PISTOL_DAMAGE=int(FIST_DAMAGE*3)

# enemies attack damage
ENEMY_ATTACK_DAMAGE=FIST_DAMAGE
RANGED_ENEMY_ATTACK_DAMAGE=ENEMY_ATTACK_DAMAGE*0.5
RAPTOR_ENEMY_ATTACK_DAMAGE=ENEMY_ATTACK_DAMAGE*1.2

# WAVES

######## player visual frame sizes ########
