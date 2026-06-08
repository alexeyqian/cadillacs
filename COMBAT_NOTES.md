# Combat Notes

Reference:
Cadillacs & Dinosaurs Arcade

---

# Combat Philosophy

Enemies should feel:

- Dangerous
- Readable
- Fair

Player should:

- React to enemy tells
- Avoid damage through skill
- Control crowds

---

# Enemy Attack Structure

Every attack contains:

1. Windup
2. Active
3. Recovery

Example:

Windup = 20 frames
Active = 10 frames
Recovery = 25 frames

Total = 55 frames

At 60 FPS:

55 / 60 = 0.92 seconds

---

# State Machine

IDLE

↓

CHASE

↓

ATTACK_WINDUP

↓

ATTACK_ACTIVE

↓

ATTACK_RECOVERY

↓

CHASE

---

# Recommended Enemy Timings

Normal Enemy

Windup:
20-30 frames

Active:
8-12 frames

Recovery:
20-30 frames

---

Fast Enemy

Windup:
10-15 frames

Active:
6-8 frames

Recovery:
15-20 frames

---

Heavy Enemy

Windup:
35-45 frames

Active:
15-20 frames

Recovery:
35-45 frames

---

# Fairness Rules

Enemy should never:

- Instantly attack
- Attack without warning
- Attack during recovery
- Attack through walls

Enemy should:

- Telegraph attacks
- Commit to attack animation
- Be punishable after missing

---

# Group Combat Rules

Maximum attackers:

2

Others:

- Circle player
- Wait
- Reposition

Avoid:

"Zombie swarm"

---

# Player Combo Targets

Future Implementation

Combo A:

Punch
Punch
Punch

Combo B:

Punch
Punch
Kick

Combo C:

Run Attack

---

# Hit Stun

Light Hit:

12 frames

Medium Hit:

18 frames

Heavy Hit:

24 frames

---

# Knockdown

Knockdown Duration:

60 frames

Invulnerable while down:

Yes

Wakeup:

Automatic

---

# Future Combat Systems

- Grab
- Throw
- Air attacks
- Weapon attacks
- Boss armor
- Counter attacks
- Rage mode

---

# Balance Targets

Player Health:
100

Normal Enemy:
30

Fast Enemy:
20

Heavy Enemy:
60

Boss:
300+

These values are placeholders and should be tuned through playtesting.