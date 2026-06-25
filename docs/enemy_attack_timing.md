# Enemy Attack Timing Design

This document describes how to design enemy attack timing so combat feels fair,
readable, and balanced compared to the player's attacks.

The main goal is:

```text
Enemies may punish bad positioning, but should not punish correct reactions.
```

That means enemies should not instantly damage the player just because they are
nearby. The player should have a visible chance to react, move away, interrupt,
or punish the enemy after a missed attack.

---

## Core Principle

A fair enemy attack should follow this shape:

```text
Detect player -> move into range -> face player -> wind-up -> active hitbox -> recovery
```

Do not let enemies instantly damage the player the moment they enter attack
range.

The most important fairness rule:

```text
Enemy attacks should have visible startup and punishable recovery.
```

If the player sees the enemy starting an attack and reacts correctly, the player
should usually be able to avoid or interrupt it.

---

## Recommended Enemy Attack Phases

Enemy attacks should be split into clear phases:

```text
CHASE
  Enemy moves toward player.

ATTACK_WINDUP
  Enemy stops moving, faces player, and shows the beginning of the attack.
  No damage happens yet.

ATTACK_ACTIVE
  Attack hitbox becomes active for a short window.
  Damage can happen here.

ATTACK_RECOVERY
  Attack hitbox is disabled.
  Enemy cannot immediately attack again.
  Player can punish the missed or blocked attack.
```

At 60 FPS, good starting values are:

```text
WINDUP:   20-35 frames
ACTIVE:   6-12 frames
RECOVERY: 25-45 frames
COOLDOWN: 30-90 frames
```

These values should differ by enemy type:

```text
Normal enemy:
  Medium windup
  Medium damage
  Medium recovery

Fast enemy:
  Shorter windup
  Lower damage
  Shorter recovery

Heavy enemy:
  Long windup
  Higher damage
  Longer recovery

Ranged enemy:
  Longer decision delay
  Projectile startup
  Clear firing animation
```

---

## When Should An Enemy Start Attacking?

An enemy should only start an attack if all of these are true:

```text
1. Player is inside horizontal attack range.
2. Player is roughly aligned on the Y axis.
3. Enemy is facing the player.
4. Enemy is not in HIT, DEAD, ATTACK_ACTIVE, or ATTACK_RECOVERY.
5. Enemy attack cooldown is finished.
6. Enemy has waited briefly after entering range.
7. Optional: not too many enemies are already attacking.
```

The enemy should not attack immediately on the first frame that the player enters
range. A small decision delay makes the enemy feel intentional instead of
robotic.

Example check:

```python
def can_start_attack(enemy, player):
    horizontal_distance = abs(enemy.rect.centerx - player.rect.centerx)
    vertical_distance = abs(enemy.rect.centery - player.rect.centery)

    return (
        horizontal_distance <= enemy.attack_range
        and vertical_distance <= enemy.attack_y_tolerance
        and enemy.attack_cooldown <= 0
        and enemy.state not in ["HIT", "DEAD", "ATTACK"]
    )
```

Then add an attack decision timer:

```python
if can_start_attack(enemy, player):
    enemy.attack_decision_timer += 1

    if enemy.attack_decision_timer >= enemy.attack_delay:
        enemy.start_attack()
else:
    enemy.attack_decision_timer = 0
```

Recommended attack delay values:

```text
NormalEnemy: attack_delay = 20 frames
FastEnemy:   attack_delay = 12 frames
HeavyEnemy:  attack_delay = 35 frames
RangedEnemy: attack_delay = 30 frames
```

This gives the player a small but important reaction window.

---

## Comparison With Player Attacks

The player should generally have faster, more responsive attacks than enemies.

Player attacks should usually have:

```text
Faster startup
Shorter recovery
More control
Better combo potential
```

Enemy attacks should usually have:

```text
Clearer telegraphs
Longer commitment
More predictable timing
Cooldowns between attacks
```

Example timing comparison:

```text
Player punch:
  startup:  6-10 frames
  active:   6 frames
  recovery: 10-18 frames

Normal enemy punch:
  windup:   20-28 frames
  active:   6-10 frames
  recovery: 25-35 frames
```

This keeps combat fair because the player wins by reading enemy behavior, not by
guessing.

---

## Fairness Examples

Good enemy behavior:

```text
The player walks straight into attack range and keeps attacking late.
The enemy's windup finishes.
The enemy hits the player.
```

This is fair because the player made a risky choice.

Good player reward:

```text
The enemy starts windup.
The player backs away.
The enemy attack misses.
The enemy enters recovery.
The player moves in and punishes.
```

This is fair because the player read the attack correctly.

Good interrupt behavior:

```text
The enemy starts windup.
The player attacks before the enemy hitbox becomes active.
The enemy is interrupted and enters HIT state.
```

This rewards fast reactions and proactive play.

---

## Suggested Enemy State Flow

A simple state flow for the current project:

```text
CHASE
  If close enough and aligned:
    go to ATTACK_WINDUP

ATTACK_WINDUP
  Stop moving
  Face player
  Play startup animation
  No hitbox yet
  After windup frames:
    go to ATTACK_ACTIVE

ATTACK_ACTIVE
  Enable attack hitbox
  If hit player:
    apply damage once
  After active frames:
    go to ATTACK_RECOVERY

ATTACK_RECOVERY
  Disable attack hitbox
  Wait recovery frames
  Then go to CHASE or IDLE
  Start attack cooldown
```

This fits the current `enemy.py` architecture and can be added incrementally.

---

## Group Balance

One enemy can feel fair, but several enemies attacking at the same time can feel
cheap. Beat'em ups often solve this with an attack slot system.

Recommended rule:

```text
Only 1-2 enemies may actively attack the player at the same time.
Other enemies should circle, reposition, wait, or approach slowly.
```

Simple example:

```python
MAX_ATTACKERS = 2

if level.active_enemy_attackers < MAX_ATTACKERS:
    enemy.start_attack()
```

This keeps group fights dramatic without overwhelming the player unfairly.

Suggested values:

```text
Easy / early waves: 1 active attacker
Normal waves:       1-2 active attackers
Boss support waves: 1 active attacker plus boss
Survival mode:      2 active attackers, maybe 3 later
```

---

## Hitbox Timing Notes

For melee attacks, avoid making the enemy's entire body dangerous unless the move
visually uses the whole body.

Rule of thumb:

```text
Standard punches and kicks:
  Hitbox should cover the fist or boot plus 10-15 pixels of forearm or shin.
  Shoulder, elbow, torso, and head should remain vulnerable hurtboxes.

Large weapon swings:
  Hitbox should cover the full blade, pipe, or weapon length plus the hand
  holding it.

Body slams and shoulder tackles:
  Hitbox may cover the chest, shoulder, and upper arm because the whole body
  mass is the weapon.
```

This helps the player understand why they were hit.

---

## Counter-Hit Design

A counter-hit happens when a character is struck while performing their own
attack animation.

Example:

```text
The player starts a punch.
The player's arm extends.
An enemy hits the player's extended hurtbox before the player's fist hitbox
connects.
The player's attack is interrupted.
The player enters HIT state.
```

This can make combat deeper, but it should be introduced after the basic attack
timing feels good.

Recommended starting rule:

```text
During attack windup and recovery, characters are vulnerable.
During active frames, attacks can hit, clash, or trade depending on the design.
```

---

## Clash / Parry / Trade Design

When two opposing attack hitboxes collide on the same frame before either one
touches a vulnerable hurtbox, the game needs a clear rule.

There are several possible designs, but the recommended arcade-style approach is
weapon deflection or parry.

### Method 1: Weapon Deflection / Parry

If a fist hits another fist, or a bare attack hits a weapon attack directly, the
attacks cancel each other out.

Result:

```text
Neither character takes health damage.
Both characters are pushed into brief recoil.
A spark, block, or clink effect appears.
```

Gameplay benefit:

```text
Precise timing can neutralize an enemy attack.
The player feels rewarded for reading the enemy.
The enemy attack still feels dangerous but not unfair.
```

This is a good long-term direction for a professional arcade feel.

For the first implementation, this can be simplified:

```text
If player hitbox and enemy hitbox overlap during active frames:
  cancel both attacks
  play clash effect
  apply short recoil to both
```

---

## Recommended Milestone Plan

Implement this system step by step.

### Milestone A: Basic Enemy Attack Phases

Add:

```text
ATTACK_WINDUP
ATTACK_ACTIVE
ATTACK_RECOVERY
```

Keep behavior simple:

```text
Enemy stops during windup
Hitbox only exists during active frames
Enemy cannot move or attack during recovery
```

### Milestone B: Enemy Type Timing

Give each enemy type its own timing values:

```text
attack_delay
attack_windup_duration
attack_active_duration
attack_recovery_duration
attack_cooldown_duration
attack_y_tolerance
```

### Milestone C: Group Attack Slots

Limit the number of enemies that can attack at once:

```text
Only 1-2 enemies can be in ATTACK_WINDUP or ATTACK_ACTIVE.
```

### Milestone D: Counter-Hits

Add counter-hit rules after basic enemy attacks feel fair.

Start simple:

```text
Attack startup and recovery are vulnerable.
Getting hit during startup cancels the attack.
```

### Milestone E: Clash / Parry

Add attack-vs-attack collision:

```text
Active player attack hitbox touches active enemy attack hitbox.
Both attacks cancel.
Both characters briefly recoil.
```

---

## Practical Starting Values

Use these as initial tuning values:

```text
NormalEnemy
  attack_range: 55
  attack_y_tolerance: 24
  attack_delay: 20
  windup: 24
  active: 8
  recovery: 30
  cooldown: 45

FastEnemy
  attack_range: 48
  attack_y_tolerance: 22
  attack_delay: 12
  windup: 16
  active: 6
  recovery: 22
  cooldown: 40

HeavyEnemy
  attack_range: 70
  attack_y_tolerance: 28
  attack_delay: 35
  windup: 36
  active: 10
  recovery: 45
  cooldown: 65

RangedEnemy
  attack_range: 220
  attack_y_tolerance: 36
  attack_delay: 30
  windup: 32
  active: 4
  recovery: 40
  cooldown: 90
```

These are not final balance values. They are good first-pass numbers that should
be tuned by playtesting.

---

## Summary

The best enemy attack system for this project is not complicated. It should be
clear, readable, and predictable:

```text
Enemy enters range.
Enemy waits briefly.
Enemy visibly winds up.
Enemy hitbox becomes active for a short time.
Enemy recovers.
Player can punish.
```

This keeps the game fair while still letting enemies feel dangerous.
