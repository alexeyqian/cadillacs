######## system and sizes ########

FPS=60
# external window width: for real monitor/display
EXTERNAL_WIDTH=1920
EXTERNAL_HEIGHT=1080
# internal window width: for entire game area
SCREEN_WIDTH=1920
SCREEN_HEIGHT=1080
# total stage width, should around 3 screens
WORLD_WIDTH=SCREEN_WIDTH*4
PLAYER_SCREEN_EDGE_MARGIN=80

# Classical Proportions (Artistic & Anatomical)
# Width-to-height ratio: 1:4 ratio
# Biacromial width: 46.25 cm
# Head height units: 2 full heads wide
# height: 185 cm, shoulder: 46.25cm
# height: 182 cm, shoulder: 45.5cm
# height: 180 cm, shoulder: 45cm
# PLAYER_NAKED_HEIGHT=185
# PLAYER_NAKED_WIDTH=47
# Since arcade is left/right facing,
# the width is wider than shoulder

# Important: feet alignment matters most.anchor by feet, not by image center.
# Across idle, walk, attack, hit, etc., 
# the player’s feet should land on the same baseline. 
PLAYER_W=128 # static left/right facing width
PLAYER_H=256
# collision box is centered on bottom
# COLLISION UNIT == UNIT_LENGTH == PIXEL_PER_GRID == player shoulder width
PLAYER_COLLISION_W = 128
PLAYER_COLLISION_H = 50
# default for most of times
# some special movement might need special hurtbox
PLAYER_HURTBOX_W = PLAYER_COLLISION_W
PLAYER_HURTBOX_H = int(PLAYER_H*0.9)
PLAYER_HURTBOX_OFFSET_X=int(-1 * PLAYER_HURTBOX_W//2)
PLAYER_HURTBOX_OFFSET_Y=int(-1*(PLAYER_HURTBOX_H + PLAYER_COLLISION_H*2))

PLAYER_HITBOX_W = int(PLAYER_W*1.3+30)
PLAYER_HITBOX_H = int(PLAYER_H*0.2)
PLAYER_HIT_BOX_OFFSET_X = int(PLAYER_W/2)
PLAYER_HIT_BOX_OFFSET_Y = int(-1*(PLAYER_HURTBOX_H + 50))

ENEMY_W=PLAYER_W
ENEMY_H=PLAYER_H
ENEMY_COLLISION_W = PLAYER_COLLISION_W
ENEMY_COLLISION_H = PLAYER_COLLISION_H
ENEMY_HURTBOX_W = PLAYER_HURTBOX_W
ENEMY_HURTBOX_H = PLAYER_HURTBOX_H
ENEMY_HURTBOX_OFFSET_X=int(-1 * ENEMY_HURTBOX_W//2)
ENEMY_HURTBOX_OFFSET_Y=int(-1*(ENEMY_HURTBOX_H + ENEMY_COLLISION_H*2))

ENEMY_HITBOX_W = int(ENEMY_W*1)
ENEMY_HITBOX_H = int(ENEMY_H*0.2)
ENEMY_HITBOX_OFFSET_X = int(ENEMY_W/2)
ENEMY_HITBOX_OFFSET_Y = int(-1*(ENEMY_HURTBOX_H + 70))

# fallback walkable area height
LANE_TOP=600-PLAYER_H
LANE_BOTTOM = SCREEN_HEIGHT-PLAYER_H-100

UI_FIRST_X=32
UI_FIRST_Y=32
UI_FONT_SIZE=36

######## debug ########
SHOW_COMBAT_BOXES=False
SHOW_EXIT_RECT=True
# Dev only.
# None means start from the first stage normally.
# Can be a stage id, for example: "episode_1_stage_4_ruined_arena"
START_STAGE=None
#"episode_1_stage_4_ruined_arena"

######## health and score ########
PLAYER_LIVES=1 #3
PLAYER_MAX_HP=100
PLAYER_EXTRA_LIFE_SCORE_BASE=30000
PLAYER_EXTRA_LIFE_SCORE_STEP=30000
ENEMY_MAX_HP=int(PLAYER_MAX_HP*1)
ENEMY_SCORE_POINTS = 100

######## speed ########
PLAYER_SPEED = 10
PLAYER_RUN_SPEED= PLAYER_SPEED * 2
ENEMY_SPEED=int(PLAYER_SPEED*0.5)
PROJECTILE_SPEED=PLAYER_SPEED*3

######## player attack ########
FIST_DAMAGE=10
# Attack lifecycle
# -> windup (prepare)
# -> active attack (hit player once, not every frame) 
# -> recovery (enemy cannot move)
# ->cooldown(frame cooldown before next attack)

ATTACK_1_DAMAGE=10
ATTACK_1_WINDUP_DURATION=3
ATTACK_1_ACTIVE_DURATION=3
ATTACK_1_RECOVERY_DURATION=5
ATTACK_1_COOLDOWN=2
ATTACK_1_HIT_STUN_DURATION=15
ATTACK_1_KNOCKBACK_VELOCITY=10

ATTACK_2_DAMAGE=12
ATTACK_2_HIT_STUN=10
ATTACK_2_WINDUP_DURATION=4
ATTACK_2_ACTIVE_DURATION=4
ATTACK_2_RECOVERY_DURATION=6
ATTACK_2_COOLDOWN=4
ATTACK_2_HIT_STUN_DURATION=20
ATTACK_2_KNOCKBACK_VELOCITY=10

ATTACK_3_DAMAGE=15
ATTACK_3_HIT_STUN=10
ATTACK_3_WINDUP_DURATION=5
ATTACK_3_ACTIVE_DURATION=4
ATTACK_3_RECOVERY_DURATION=8
ATTACK_3_COOLDOWN=6
ATTACK_3_HIT_STUN_DURATION=25
ATTACK_3_KNOCKBACK_VELOCITY=10

# todo: simplify it?
ATTACK_3_FORWARD_NUDGE_FRAMES=3
ATTACK_3_FORWARD_NUDGE_SPEED_SCALE=0.35

# todo: merge with PLAYER_COMBO_WINDOW
ATTACK_COMBO_WINDOW=30
# Combo windows are measured from attack start, not from attack finish.
# Because standing punches now have recovery frames, these values include
# attack duration plus the desired follow-up grace period.
PLAYER_COMBO_WINDOW = 29
# the window starts when the attack starts, not when it finishes. 
# That is why the settings comment says the value includes attack duration plus follow-up grace.
PLAYER_FIRST_TO_SECOND_COMBO_WINDOW = 29
PLAYER_SECOND_TO_THIRD_COMBO_WINDOW = 24
PLAYER_THIRD_HIT_RECOVERY = 24
PLAYER_CLASH_RECOVERY = 8

# RUN ATTACK
# it's 0.25 seconds, should we use game frames as timer counter here?
RUN_TAP_WINDOW=0.25
RUN_ATTACK_REQUIRED_DISTANCE=100

RUN_ATTACK_DAMAGE=28
RUN_ATTACK_WINDUP_DURATION=4
RUN_ATTACK_ACTIVE_DURATION=16
RUN_ATTACK_RECOVERY_DURATION=6
RUN_ATTACK_COOLDOWN=60
RUN_ATTACK_HIT_STUN_DURATION=25
RUN_ATTACK_KNOCKBACK_VELOCITY=10

# TODO: below design is too complicated, might remove?
RUN_ATTACK_FULL_POWER_DISTANCE=240
RUN_ATTACK_MOMENTUM_FRAMES=18
RUN_ATTACK_MOMENTUM_SPEED_SCALE=0.85
RUN_ATTACK_LANDING_RECOVERY=4

RUN_ATTACK_BASE_KNOCKBACK=18
RUN_ATTACK_FULL_POWER_KNOCKBACK_BONUS=6
RUN_ATTACK_BASE_ENEMY_HIT_STUN=40
RUN_ATTACK_FULL_POWER_ENEMY_HIT_STUN_BONUS=6

# todo: settings for jump attack
JUMP_ATTACK_DAMAGE=FIST_DAMAGE

# grab and throw
PLAYER_GRAB_RANGE=int(PLAYER_W * 0.4)
PLAYER_GRAB_KNEE_DURATION = 14
PLAYER_GRAB_KNEE_HIT_FRAME = 6
THROWN_DAMAGE=int(FIST_DAMAGE*1.5)
# weapons
KNIFE_DAMAGE=int(FIST_DAMAGE*1.5)
BAT_DAMAGE=int(FIST_DAMAGE*2)
PISTOL_DAMAGE=int(FIST_DAMAGE*3)

######## enemy attack timing ########
ENEMY_DETECT_RANGE=int(SCREEN_WIDTH*0.50)
ENEMY_ATTACK_RANGE=130
ENEMY_ATTACK_LANE_RANGE=50

# thinking and make decisions
ENEMY_ATTACK_DELAY=20
ENEMY_ATTACK_DAMAGE=int(ATTACK_1_DAMAGE*0.8)
ENEMY_ATTACK_WINDUP=int(ATTACK_1_WINDUP_DURATION*1.2)
ENEMY_ATTACK_ACTIVE=int(ATTACK_1_ACTIVE_DURATION*0.8)
ENEMY_ATTACK_RECOVERY=int(ATTACK_1_RECOVERY_DURATION*1.2)
ENEMY_ATTACK_COOLDOWN=30 # add player attack cooldown?
ENEMY_ATTACK_HIT_STUN_DURATION=5
ENEMY_ATTACK_KNOCKBACK_VELOCITY=10


# Only a small number of regular melee enemies 
# should enter ATTACK at the same time.
MAX_MELEE_ATTACKERS = 4
ENEMY_FLANK_OFFSET_X = 120
# avoid multiple enemies stack on the same lane. 
# give flankers a small Y offset based on crowding.
ENEMY_FLANK_OFFSET_Y = 36
ENEMY_FLANK_DECISION_DURATION = 20
ENEMY_FLANK_Y_TOLERANCE = 18

# per enemy settings
RANGED_ENEMY_ATTACK_DAMAGE=ENEMY_ATTACK_DAMAGE*0.5

BOSS_ENEMY_SPEED=ENEMY_SPEED*0.5
BOSS_SPECIAL_ATTACK_WARNING_DURATION=45
