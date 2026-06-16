# AGENTS.md

# Cadillacs and Dinosaurs (PyGame) Project

## Goal

Build easy-to-understand Cadillacs and Dinosaurs style beat'em up using:

- Python
- PyGame
- macOS compatible
- Make code easy to understand and modularized for easy to maintain
- Make code well organized
- Step-by-step milestone-driven development
- Enemy types should be easy to expand.
- Weapon types should be easy to expand.
- Should support choose different players
- Should support level editing in future
- Try not to remove code comments, these are added by myself for code understanding
- Try to make it more like production scale project, not educational any more.

The codebase should easy to understand and easy to maintain. 
You can do refactoring if needed, including: rename variables, rename functions, move functions into different files. Prefer to write code in the way easy to write test in future.


---

# Current Architecture

## Core Files

### main.py

Responsibilities:

- Main game loop
- Event handling
- Wave triggering
- Camera lock logic
- Collision handling
- Loot pickup
- Projectile processing
- Rendering orchestration

Key helper functions:

- update_player_weapon_interaction()
- main_draw()
- main_draw_world()
- main_draw_ui()

---

### player.py

Responsibilities:

- Movement
- Combo attacks
- Weapon handling
- Projectile firing
- Animation state machine
- Health system

States:

- IDLE
- WALK
- ATTACK_1
- ATTACK_2
- ATTACK_3
- HIT
- DEAD

Important fields:

- weapon
- pending_projectile
- combo_step
- combo_timer
- fire_pressed

---

### enemy.py

Responsibilities:

- Basic enemy AI
- Patrol/Chase/Attack foundation
- Knockback
- Damage handling
- Loot drops
- Animation

States:

- IDLE
- PATROL
- WALK
- CHASE
- ATTACK
- HIT
- DEAD

Important fields:

- attack_range
- detect_range
- knockback_velocity
- hit_timer
- loot_generated

---

### enemy_factory.py

Creates enemy variants:

- Enemy
- FastEnemy
- HeavyEnemy
- RangedEnemy

Factory method:

- create_enemy(enemy_type, x, y)

---

### fast_enemy.py

Characteristics:

- Fast movement
- Lower HP

---

### heavy_enemy.py

Characteristics:

- Slow movement
- High HP
- Large size

---

### ranged_enemy.py

Characteristics:

- Long attack range
- Enemy projectile support

---

### boss_enemy.py

Current boss implementation.

Future:
- El Gran Maja deep sea monster boss

---

### camera.py

Responsibilities:

- Follow player
- Clamp to world boundaries
- Arena lock support

Current:

Horizontal scrolling only.

---

### level.py

Responsibilities:

- Wave progression
- Arena lock state

Current waves:

1. Normal wave
2. Mixed wave
3. Heavy/Fast wave
4. BossWave
5. SpawnWave

---

### wave.py

Contains:

- Wave
- BossWave
- SpawnWave

---

### spawner.py

Contains:

- EnemySpawner

Supports:

- delayed spawning
- survival mode
- reinforcements

---

# Current Systems

Implemented:

- Side scrolling world
- Camera
- Arena lock
- Combo attacks
- Weapons
- Guns
- Projectiles
- Enemy projectiles
- Health bars
- Knockback
- Breakable objects
- Loot drops
- Wave progression
- Boss wave
- Spawn wave
- Animation framework
- Enemy variants

---

# Animation System

Files:

- animation.py
- animation_manager.py
- asset_loader.py
- animation_config.py

Current direction:

Each enemy type owns its own sprite sheet config.

Example:

- NORMAL_ENEMY_WALK
- FAST_ENEMY_WALK
- HEAVY_ENEMY_WALK
- BOSS_ENEMY_WALK

Avoid using one shared ENEMY_WALK config.

---

# Asset Decisions

Player:

- Sprite sheet driven
- Placeholder fallback supported

Enemies:

- Separate sprite sheets per enemy type

Boss:

Current generated assets:

- boss_enemy_walk.png
- boss_enemy_attack.png

Format:

- 128x256 frame size
- 6 frames

---

# Coding Guidelines

Prefer:

- Readability
- Small functions
- Explicit code
- Step-by-step milestones

Avoid:

- Premature optimization
- Complex ECS architecture
- Excessive abstractions

This project is educational first.

---

# Known TODOs

## Combat

- Attack buffering
- Better combo chaining
- Weapon throw system

## Enemy AI

- Finish PATROL state
- Smarter CHASE state
- Group tactics
- Flanking

## Boss

- El Gran Maja attack patterns
- Multi-phase boss
- Tentacle attacks
- Death animation

## Animation

- Attack sprites
- Hit sprites
- Death sprites
- Raptor sprites

## World

- Multiple stages
- Stage transitions
- Background art
- Parallax scrolling

## Camera

- Smooth camera
- Camera shake
- Boss arena camera

## UI

- Score
- Lives
- Continue screen
- Stage intro screen

---

# Next Recommended Milestones

Milestone 20
- Dinosaur / Raptor Enemy

Milestone 21
- Boss Phase System

Milestone 22
- Enemy Death Animations

Milestone 23
- Stage 2

Milestone 24
- Save/Load

---

# Important Baseline

Current baseline files to preserve during refactors:

- main.py
- player.py
- enemy.py
- camera.py
- level.py
- wave.py

New changes should be incremental and milestone-based.

Some notes:
The Rule of Thumb for Beat 'Em UpsStandard Punches/Kicks: Wrap the red hitbox around the striking point (the fist or the boot) + 10 to 15 pixels of the forearm/shin to ensure a clean visual overlap. Keep the shoulder and elbow as a vulnerable green hurtbox.Large Weapon Swings (Knives/Pipes): Wrap the hitbox around the entire length of the active blade or metal pipe, plus the fist holding it. The weapon itself is an object, so it should be completely dangerous from base to tip.Body Slams / Clotheslines: If the character throws their entire body weight forward (like a shoulder tackle), then you can expand a single massive hitbox across their entire chest and upper arm, because their whole mass is acting as the weapon.

A counter-hit check is a combat programming routine that detects when a character is struck while they are in the middle of executing their own attack animation.When Mustapha punches forward, his arm extends. If an enemy strikes his extended arm hurtbox before Mustapha's fist hitbox can touch the enemy, the engine registers a "Counter-Hit." This instantly interrupts Mustapha's punch, cancels his attack frame, and knocks him into a hit-stun state.

When two opposing attack hitboxes collide at the exact same frame before either one touches a vulnerable body hurtbox, it causes a phenomenon known as a Clash, Parry, or Trade.Depending on how competitive or realistic you want your beat 'em up to be, modern and classic 2D games handle this intersection using one of three design rules:

Method 1: The Weapon Deflection / Parry (The Arcade Standard)This is the most satisfying and professional approach. If a bare fist hits a steel knife or another fist directly, the weapons cancel each other out. Neither character takes damage to their health bars, but both are forced into a brief visual recoil animation.What happens: Both hitboxes bounce off each other. A unique metal-clinking spark or block effect flashes.The Gameplay Benefit: It rewards the player for precise timing. Instead of getting sliced by a knife, their punch acts as a shield, neutralizing the enemy's threat.
