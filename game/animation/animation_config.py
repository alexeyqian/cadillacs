PLAYER_IDLE = {
    "file":"game/assets/player/player_idle.png",
    "frame_width":128,
    "frame_height":256,
    "frame_count":6
}

PLAYER_WALK = {
    "file":"game/assets/player/player_walk.png",
    "frame_width":128,
    "frame_height":256,
    "frame_count":6
}

PLAYER_RUN = {
    "file":"game/assets/player/player_run.png",
    "frame_width":128,
    "frame_height":256,
    "frame_count":6
}

PLAYER_ATTACK = {
    "file":"game/assets/player/player_attack.png",
    "frame_width":192,
    "frame_height":256,
    "frame_count":2
}

PLAYER_RUN_ATTACK = {
    "file":"game/assets/player/player_run_attack.png",
    "frame_width":256,
    "frame_height":256,
    "frame_count":2
}

PLAYER_JUMP = {
    "file":"game/assets/player/player_jump.png",
    "frame_width":128,
    "frame_height":256,
    "frame_count":6
}

PLAYER_JUMP_ATTACK = {
    "file":"game/assets/player/player_jump_attack.png",
    "frame_width":224,
    "frame_height":256,
    "frame_count":6
}

PLAYER_GRAB = {
    "file":"game/assets/player/player_grab.png",
    "frame_width":176,
    "frame_height":256,
    "frame_count":6
}

PLAYER_THROW = {
    "file":"game/assets/player/player_throw.png",
    "frame_width":224,
    "frame_height":256,
    "frame_count":6
}

PLAYER_HIT = {
    "file":"game/assets/player/player_hit.png",
    "frame_width":144,
    "frame_height":256,
    "frame_count":6
}

PLAYER_DEAD = {
    "file":"game/assets/player/player_dead.png",
    "frame_width":256,
    "frame_height":128,
    "frame_count":6
}

# ==========================================
# Normal Enemy
# ==========================================

NORMAL_ENEMY_IDLE = {
    "file":"game/assets/enemy/normal_enemy_idle.png",
    "frame_width":64,
    "frame_height":64,
    "frame_count":4
}

NORMAL_ENEMY_WALK = {
    "file":"game/assets/enemy/normal_enemy_walk.png",
    "frame_width":64,
    "frame_height":64,
    "frame_count":6
}

NORMAL_ENEMY_ATTACK = {
    "file":"game/assets/enemy/normal_enemy_attack.png",
    "frame_width":64,
    "frame_height":64,
    "frame_count":6
}

NORMAL_ENEMY_HIT = {
    "file":"game/assets/enemy/normal_enemy_idle.png",
    "frame_width":64,
    "frame_height":64,
    "frame_count":4
}

NORMAL_ENEMY_DEAD = {
    "file":"game/assets/enemy/normal_enemy_dead.png",
    "frame_width":64,
    "frame_height":64,
    "frame_count":6
}

# ==========================================
# Fast Enemy
# ==========================================

FAST_ENEMY_IDLE = {
    "file":"game/assets/enemy/fast_enemy_idle.png",
    "frame_width":64,
    "frame_height":64,
    "frame_count":4
}

FAST_ENEMY_WALK = {
    "file":"game/assets/enemy/fast_enemy_walk.png",
    "frame_width":64,
    "frame_height":64,
    "frame_count":6
}

FAST_ENEMY_ATTACK = {
    "file":"game/assets/enemy/fast_enemy_attack.png",
    "frame_width":64,
    "frame_height":64,
    "frame_count":6
}

# ==========================================
# Heavy Enemy
# ==========================================

HEAVY_ENEMY_IDLE = {
    "file":"game/assets/enemy/heavy_enemy_idle.png",
    "frame_width":64,
    "frame_height":64,
    "frame_count":4
}

HEAVY_ENEMY_WALK = {
    "file":"game/assets/enemy/heavy_enemy_walk.png",
    "frame_width":64,
    "frame_height":64,
    "frame_count":6
}

HEAVY_ENEMY_ATTACK = {
    "file":"game/assets/enemy/heavy_enemy_attack.png",
    "frame_width":64,
    "frame_height":64,
    "frame_count":6
}

# ==========================================
# Raptor Enemy
# ==========================================

RAPTOR_ENEMY_SPRITESHEET = "game/assets/enemy/raptor_enemy_spritesheet.png"

RAPTOR_ENEMY_IDLE = {
    "file": RAPTOR_ENEMY_SPRITESHEET,
    "frame_width":80,
    "frame_height":160,
    "frame_count":4,
    "start_frame":0
}

RAPTOR_ENEMY_PATROL = {
    "file": RAPTOR_ENEMY_SPRITESHEET,
    "frame_width":80,
    "frame_height":160,
    "frame_count":4,
    "start_frame":4
}

RAPTOR_ENEMY_WALK = {
    "file": RAPTOR_ENEMY_SPRITESHEET,
    "frame_width":80,
    "frame_height":160,
    "frame_count":4,
    "start_frame":8
}

RAPTOR_ENEMY_CHASE = {
    "file": RAPTOR_ENEMY_SPRITESHEET,
    "frame_width":80,
    "frame_height":160,
    "frame_count":4,
    "start_frame":8
}

RAPTOR_ENEMY_JUMP = {
    "file": RAPTOR_ENEMY_SPRITESHEET,
    "frame_width":80,
    "frame_height":160,
    "frame_count":4,
    "start_frame":12
}

RAPTOR_ENEMY_ATTACK = {
    "file": RAPTOR_ENEMY_SPRITESHEET,
    "frame_width":80,
    "frame_height":160,
    "frame_count":4,
    "start_frame":16
}

RAPTOR_ENEMY_JUMP_ATTACK = {
    "file": RAPTOR_ENEMY_SPRITESHEET,
    "frame_width":80,
    "frame_height":160,
    "frame_count":4,
    "start_frame":20
}

# ==========================================
# Boss Enemy
# ==========================================

BOSS_ENEMY_WALK = {
    "file":"game/assets/enemy/boss_enemy_walk.png",
    "frame_width":96,
    "frame_height":96,
    "frame_count":8
}

BOSS_ENEMY_ATTACK = {
    "file":"game/assets/enemy/boss_enemy_attack.png",
    "frame_width":96,
    "frame_height":96,
    "frame_count":8
}

BOSS_ATTACK_TIMING = {
    "windup": 20,
    "active": 8,
    "recovery": 25,
}

# Animation target FPS (how many animation frames per real second)
# Tune these to control perceived animation speed; values are in frames-per-second
# for player

# TODO: use ai to re-set these values
ANIM_FPS_IDLE = 6
ANIM_FPS_WALK = 6
ANIM_FPS_RUN = 6
ANIM_FPS_JUMP = 6
ANIM_FPS_ATTACK = 12
ANIM_FPS_RUN_ATTACK=6
ANIM_FPS_JUMP_ATTACK=6
ANIM_FPS_GRAB=6
ANIM_FPS_THROW=6
ANIM_FPS_HIT = 6
ANIM_FPS_DEAD = 999
# for enemy
ANIM_FPS_IDLE_ENEMY = 6
ANIM_FPS_WALK_ENEMY = 6
ANIM_FPS_ATTACK_ENEMY = 6
ANIM_FPS_HIT_ENEMY = 6
