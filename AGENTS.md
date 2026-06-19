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


Combat should use hitboxes, hurtboxes, timing, and attack data rather than hardcoded distance checks.
Recommended flow:
Controller requests attack
Character enters attack state
Animation/attack timing advances
Attack active frames expose hitbox
Combat system checks hitbox vs hurtbox
Target receives damage/reaction
Attack remembers already-hit targets
Character enters recovery or next combo state