# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

A Cadillacs and Dinosaurs-style beat-em-up built with Python and PyGame, targeting macOS.

## Commands

```bash
# Run the game
python main.py

# Run all tests
python -m pytest tests/

# Run a single test file
python -m pytest tests/test_combat_geometry.py

# Run tests matching a name
python -m pytest tests/ -k "test_attack"
```

## Architecture

**Entry point:** `main.py` — initializes pygame, builds `GameState`, runs the main loop (events → input → gameplay → draw).

**`game/game_state.py`** — plain data bag passed everywhere. All mutable game state lives here (player, enemies, weapons, camera, score, etc.). Systems read and write it rather than owning state themselves.

**`game/systems/`** — pure functions that operate on `GameState`. `gameplay_system.py` is the top-level coordinator that calls all other systems each frame in order. Systems are decoupled: arena boundaries, collision, combat, wave spawning, camera, cleanup, etc. each live in their own file.

**`game/entities/`** — `GameObject` → `Character` → `Player`/`Enemy` hierarchy. Characters are shells; behavior comes from **components** stored as attributes (`health`, `movement`, `geometry`, `animation_controller`, `renderer`, `combat_controller`, `lifecycle_controller`). Individual enemy types (e.g. `ferris_enemy.py`, `mustapha_player.py`) subclass `Enemy`/`Player` and wire up their specific components.

**`game/components/`** — reusable behavior objects attached to characters. Examples: `PlayerMovement`, `EnemyMovement`, `CharacterGeometry`, `Health`, `EnemyLifeCycle`. Components receive the owning character as a parameter when called — they don't store a back-reference.

**`game/combat/`** — combat primitives: `AttackData` (hitbox/hurtbox/timing/damage), `AttackManager` (tracks active attacks and already-hit targets), `DamageRequest`, `CombatGeometry`. The intended flow is: controller requests attack → character enters attack state → animation advances frames → active frames expose hitbox → `combat_system` checks hitbox vs hurtbox → target receives damage/reaction.

**`game/core/events.py`** — simple event queue used for decoupled communication between systems.

**`game/factories/`** — `PlayerFactory`, `EnemyFactory` — centralized construction so entity wiring is in one place.

**`game/level/`** — `Level`, `StageManager`, `StageConfig`. Stages are data dicts (`EPISODE_1_STAGES`) describing background, player start, wave spawns, weapons, and objects.

**`game/animation/`** — animation controllers and data; frame-based, driven by character state.

**`game/settings.py`** — global constants (screen size, FPS, etc.). `game/tuning.py` — gameplay tuning values (speeds, damage, etc.).

**`main_draw.py`** — all rendering logic separated from update logic.

## Key Conventions

- Systems must not embed arena-lock, camera, or boundary logic inside `Player` or `Enemy` — those belong in dedicated system files.
- Attack collision uses hitbox/hurtbox geometry, not distance checks.
- `AttackManager` on each character tracks which targets were already hit in the current attack to prevent multi-hits.
- Enemy types are added by subclassing `Enemy` and registering in `EnemyFactory` — no changes needed elsewhere.
- Preserve existing code comments; they are intentional documentation.
- `settings.SHOW_COMBAT_BOXES` (toggle with F1 in-game) enables hitbox debug rendering.
