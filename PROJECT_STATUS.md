# Cadillacs & Dinosaurs Pygame Project
## Current Project Status

Last Updated: 2026-06-08

---

# Project Vision

Create a modern educational recreation inspired by the classic arcade beat-em-up:

Cadillacs & Dinosaurs

Goals:

- Easy to understand code
- Easy to maintain and extend architecture
- Modular systems
- Maintainable codebase
- Flexible to add new movement/action/state to player.
- Flexible to add new movement/action/state to enemy.
- Flexible to add all kinds of weapons into system.
- Flexible to add all kinds of vehicles into system.
- Player and enemy's action and timer can be modularized
- Multiple stage design
- Future multiplayer support
- Future content editor support

Target Platform:

- Python 3.x
- Pygame
- Windows
- macOS
- Linux

---

# Completed Milestones

## Milestone 1
Project Setup

Status: COMPLETE

Implemented:

- Game loop
- Window creation
- Settings module
- Basic project structure

---

## Milestone 2
Player Movement

Status: COMPLETE

Implemented:

- 8-direction movement
- Lane movement
- Screen clamping
- Basic animation support

---

## Milestone 3
Camera System

Status: COMPLETE

Implemented:

- Side scrolling camera
- World coordinates
- Screen coordinates
- Camera follow player

---

## Milestone 4
Enemy Foundation

Status: COMPLETE

Implemented:

- Enemy spawning
- Enemy movement
- Enemy state machine
- Chase behavior

Recent fixes:

- Enemy leaving arena bug fixed
- Enemy chase direction bug fixed

---

## Milestone 5
Wave System

Status: COMPLETE

Implemented:

- Wave definitions
- Enemy spawn control
- Wave completion detection
- Camera lock zones

---

# Current Development Stage

Current Milestone:

Asset Pipeline & Animation Framework

Status:

IN PROGRESS

Goals:

- Sprite sheet loader
- Animation definitions
- Animation player
- Asset organization
- Asset naming conventions

---

# Existing Systems

## Core

- Game Loop
- Settings
- State Management

## World

- Camera
- World Bounds
- Arena Lock

## Player

- Movement
- Collision
- State Machine

## Enemy

- Chase AI
- State Machine
- Wave Integration

## Combat

Partial Implementation

Planned Expansion:

- Attack system
- Hit detection
- Combo system
- Grab system
- Knockdown system

---

# Known Issues

Minor:

- Enemy crowding behavior needs improvement
- Enemy spacing needs tuning

Future:

- Combat balance tuning
- Animation timing tuning

---

# Next Immediate Goal

Implement:

Animation Framework

Required Features:

- SpriteSheet class
- Animation class
- AnimationSet class
- Animation state switching
- Frame timing support

---

# Long-Term Goals

- Full arcade combat
- Boss battles
- Weapons
- Pickups
- Save system
- Character select
- Online multiplayer