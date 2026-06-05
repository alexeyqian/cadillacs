
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