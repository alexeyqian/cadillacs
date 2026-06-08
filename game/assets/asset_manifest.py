from game.animation.animation_config import *

IMAGE_ASSETS = {
    "objects.box": "game/assets/objects/box.png",
    "weapon.knife": "game/assets/weapon/knife.png",
    "loot.health": "game/assets/loot/health.png",
    "loot.ammo": "game/assets/loot/ammo.png",
}

PLAYER_ANIMATIONS = {
    "player.idle": PLAYER_IDLE,
    "player.walk": PLAYER_WALK,
    "player.run": PLAYER_RUN,
    "player.attack": PLAYER_ATTACK,
    "player.run_attack": PLAYER_RUN_ATTACK,
    "player.jump": PLAYER_JUMP,
    "player.jump_attack": PLAYER_JUMP_ATTACK,
    "player.grab": PLAYER_GRAB,
    "player.throw": PLAYER_THROW,
    "player.hit": PLAYER_HIT,
    "player.dead": PLAYER_DEAD,
}

ENEMY_ANIMATIONS = {
    "enemy.normal_idle": NORMAL_ENEMY_IDLE,
    "enemy.normal_walk": NORMAL_ENEMY_WALK,
    "enemy.normal_attack": NORMAL_ENEMY_ATTACK,
    "enemy.normal_hit": NORMAL_ENEMY_HIT,
    "enemy.normal_dead": NORMAL_ENEMY_DEAD,
    "enemy.fast_idle": FAST_ENEMY_IDLE,
    "enemy.fast_walk": FAST_ENEMY_WALK,
    "enemy.fast_attack": FAST_ENEMY_ATTACK,
    "enemy.heavy_idle": HEAVY_ENEMY_IDLE,
    "enemy.heavy_walk": HEAVY_ENEMY_WALK,
    "enemy.heavy_attack": HEAVY_ENEMY_ATTACK,
    "enemy.boss_walk": BOSS_ENEMY_WALK,
    "enemy.boss_attack": BOSS_ENEMY_ATTACK,
}

ANIMATION_ASSETS = {
    **PLAYER_ANIMATIONS,
    **ENEMY_ANIMATIONS,
}