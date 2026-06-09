# PROJECT_STATUS.md

## Project

Cadillacs & Dinosaurs Inspired Beat-em-up

Engine: Python + Pygame

Current Development Stage:
Core Gameplay Vertical Slice

Last Updated:
2026-06-09

---

# Overall Progress

Estimated Completion: 35%

The project has moved beyond prototype stage and now contains a playable combat loop with:

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
* Modular gameplay architecture

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

Current architecture is stable and suitable for future expansion.

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

Recently Designed

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

Planned

* Asset manager integration
* Larger attack animation frames
* Attack frame offsets
* Weapon-specific animations
* Hit sparks
* Camera shake

---

# World Systems

Completed

* Stage scrolling
* Camera follow
* Arena lock
* Multi-wave progression
* Boss wave
* Props

Planned

* Stage hazards
* Multiple stages
* Branching paths

---

# Save / Progression

Not Started

Planned

* Save game
* Continue system
* Stage unlocks
* High score system

---

# Networking

Future

* Local co-op first
* Networking only after core gameplay is complete

---

# Current Priority

1. Player animation sizing refactor
2. Hurtbox / hitbox refactor
3. Enemy attack timing improvements
4. Weapon throw
5. Enemy animation loading refactor
6. Scene system

---

# Current Stable Baseline

Milestone 45 Complete

Implemented:

* Asset Manager
* Grab Combo
* Knee Attack

Milestone 46 (Escape Move)

Status: Deferred

Will revisit after combat refactor.
