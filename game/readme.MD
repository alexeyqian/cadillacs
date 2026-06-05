
# Camera Calculation
![alt text](image.png)

✓ Side scrolling world
✓ Camera
✓ Depth movement
✓ Multiple enemies
✓ Enemy AI
✓ Health system
✓ Player combos
✓ Enemy attacks
✓ Knockback
✓ Health bars
✓ Game Over

game/systems/
├── wave_system.py
├── combat_system.py
├── loot_system.py
├── inventory_system.py
└── projectile_system.py

Enemy flow
HP <= 0
↓
state = DEAD
↓
loot drops once
↓
corpse stays for 60 frames
↓
enemy removed

Add visual feedback for hitting enemy
Player hits enemy
↓
Small yellow/white hit spark appears
↓
Spark disappears after a few frames

Enemy kill score
Combo score
Boss bonus
Stage bonus
Total score

+100 normal enemy
+200 fast enemy
+300 heavy enemy
+2000 boss

Combo x2
Combo x3
Combo x4

TOP SCORE
SCORE
LIVES
STAGE

Enemy killed      -> score increases
Breakable object  -> score increases
Boss defeated     -> big bonus
HUD shows score

Combo Score Multiplier
Hit enemies quickly
↓
Combo increases
↓
Score multiplier increases
↓
Combo resets if player stops attacking
1st kill: +100
2-hit combo: +200
3-hit combo: +300
5-hit combo: +500

Milestone 32 — Grab & Throw System
goal:
Press L near enemy
↓
Grab enemy
↓
Press L again
↓
Throw enemy
↓
Thrown enemy damages other enemies