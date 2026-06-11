# PROJECT_STATUS.md

## Project

Cadillacs & Dinosaurs Inspired Beat-em-up

Engine: Python + Pygame

Current Development Stage:
Core Gameplay Vertical Slice + Stage Progression Foundation

Last Updated:
2026-06-11

---

# Overall Progress

Estimated Completion: 42%

The project now has a playable beat-em-up loop and the foundation for multiple stages within an episode.

Implemented gameplay includes:

* Camera system
* Arena lock system
* Wave progression
* Multiple enemy types
* Boss battle
* Weapon system
* Grab system
* Throw system
* Running attacks
* Jump attacks
* Projectile weapons
* Loot and breakable objects
* Continue/lives foundation
* Stage clear flow
* Multi-stage episode foundation

---

# Architecture Status

Completed

* GameState architecture
* Main loop refactor
* Rendering system extraction
* Gameplay system extraction
* Arena system
* Combat system
* Wave system
* Cleanup system
* Loot system
* Projectile system
* StageManager foundation
* Data-driven stage configuration
* Stage-specific background, waves, weapons, objects, exits, and walkable areas

Current architecture is stable for incremental expansion.

Important current direction:

* `Level` represents the currently loaded stage.
* `StageManager` controls which stage is active.
* `stage_config.py` defines stage data.
* `main.py` owns runtime stage loading/reset through `load_stage()`.
* Future episode support should build on top of the current stage manager instead of replacing it.

---

# Episode / Stage System

Recently Added

* Episode 1 stage list in `stage_config.py`
* StageManager with current-stage tracking and stage advancement
* Stage loading/reset helper
* Stage-specific world width and height
* Stage-specific player start position
* Stage-specific wave configuration
* Stage-specific weapons and breakable objects
* Stage-specific exit rectangles
* Stage-specific walkable polygons
* Dynamic camera world-width clamp
* Stage clear -> press Enter -> next stage flow

Episode 1 Current Stages

* Stage 1: Rooftop Approach
* Stage 2: Mansion Hallway
* Stage 3: Ruined Building transition
* Stage 4: Ruined Arena

Background Decision

* Stage backgrounds should be at least `SCREEN_WIDTH` wide.
* Avoid narrow playable backgrounds.
* If source art is narrow, expand/regenerate it to full-screen width or wider.
* This keeps rendering simple: one camera, one world coordinate system, no special centering branch.

Planned

* EpisodeManager above StageManager
* Episode clear flow
* Stage intro title card
* Optional stage transition scenes

---

# Player Systems

Completed

* Walking
* Running
* Double-tap run detection
* Jumping
* Air movement
* Jump attack
* 3-hit combo
* Grab enemy
* Throw enemy
* Grab knee attack
* Weapon pickup
* Auto weapon pickup
* Pistol firing
* Lives
* Death
* Respawn
* Stage-aware world/lane bounds
* Walkable polygon boundary check

Planned

* Escape move
* Recovery roll
* Weapon throw
* Advanced grab combos
* Special attacks

---

# Enemy Systems

Completed

* Patrol
* Chase
* Attack
* Hit reaction
* Knockback
* Grabbed state
* Thrown state
* Knockdown
* Get-up
* Death
* Separation behavior
* Stage-aware world/lane bounds
* Walkable polygon boundary check

Enemy Types

* Normal Enemy
* Fast Enemy
* Heavy Enemy
* Ranged Enemy
* Raptor Enemy
* Boss Enemy

Planned

* Improved group AI
* Flanking behavior
* Attack coordination
* Better boss phases

---

# Weapons

Completed

* Knife
* Bat
* Pistol
* Stage-configured weapon placement

Planned

* Weapon throw
* Weapon durability
* Additional weapon types

---

# Combat Status

Completed

* Combo attacks
* Running attacks
* Jump attacks
* Grab system
* Throw system
* Grab knee attack
* Separate body box
* Separate hurtbox
* Separate collision box
* Separate attack hitboxes

Planned

* Attack windup frames
* Active attack frames
* Recovery frames
* Better enemy timing
* Animation-driven hit frames

---

# Visual Systems

Completed

* Animation manager
* Sprite sheet support
* Asset loading framework
* Generated Episode 1 background art
* Stage-specific single-image backgrounds
* Debug exit rectangle drawing
* Debug walkable polygon drawing

Planned

* More stage background cleanup
* Props/foreground layering per stage
* Larger attack animation frames
* Attack frame offsets
* Weapon-specific animations
* Hit sparks polish
* Camera shake polish

---

# World Systems

Completed

* Stage scrolling
* Camera follow
* Arena lock
* Multi-wave progression
* Boss wave
* Props foundation
* Multiple stages
* Stage exits via `exit_rect`
* Walkable areas via polygon data
* Stage-specific content config

Planned

* Stage hazards
* Episode system
* Branching paths
* Stage intro and episode clear screens

---

# Save / Progression

Partially Started

* Continue/lives foundation exists.
* Score and high score manager exist.
* Stage progression foundation exists.

Planned

* Save game
* Stage unlocks
* Episode unlocks
* Persistent high score

---

# Networking

Future

* Local co-op first
* Networking only after core gameplay is complete

---

# Current Priority

1. Finish Episode 1 stage flow testing
2. Regenerate/expand Stage 3 to full-screen width or wider
3. Tune walkable polygons and exit rectangles
4. Move/tune per-stage enemy waves and pickups
5. Add EpisodeManager
6. Add stage intro / episode clear presentation
7. Continue combat expansion: weapon throw, recovery roll, boss phases

---

# Current Stable Baseline

Latest Baseline:
Multi-stage Episode 1 foundation

Implemented:

* StageManager
* Data-driven `stage_config.py`
* Runtime `load_stage()` flow
* Stage-specific waves, pickups, objects, exits, and walkable areas
* Generated Episode 1 background assets

Milestone 46 Escape Move:
Deferred

Reason:
Player state machine and stage progression work have higher priority before adding another action state.
