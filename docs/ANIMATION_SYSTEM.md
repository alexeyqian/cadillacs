# ANIMATION_REFACTOR.md

## Purpose

This document defines the current animation, visual frame, collision box, hurtbox, and hitbox design for the Cadillacs & Dinosaurs inspired Pygame beat-em-up.

This document is based on the latest `settings.py`.

---

# Current Resolution Baseline

The game now uses a full HD internal game area.

```python
EXTERNAL_WIDTH = 1920
EXTERNAL_HEIGHT = 1080

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
```

The internal game area and external display size currently match.

---

# Core Size Principle

`PLAYER_W` and `PLAYER_H` are the logical player body size.

```python
PLAYER_W = 128
PLAYER_H = 256
```

This means:

```text
Player logical body box = 128 x 256
```

Important:

```text
PLAYER_W and PLAYER_H are not always the visible sprite size.
They are the logical body anchor size.
```

Attack animations, weapon animations, and extended arm/weapon frames may be wider than the logical body box.

---

# Feet Alignment Rule

Feet alignment is the most important animation rule.

All animation frames should keep the player’s feet on the same baseline.

This applies to:

* Idle
* Walk
* Run
* Attack
* Hit
* Grab
* Throw
* Jump landing frames
* Weapon animations

The player should be anchored by feet, not by image center.

The logical player box is used for anchoring, while the visible body may leave margin inside the logical box.

---

# Lane / Ground Area

Current lane setup:

```python
LANE_TOP = 600 - PLAYER_H
LANE_BOTTOM = 1040 - PLAYER_H
```

With:

```python
PLAYER_H = 256
```

This gives:

```text
LANE_TOP = 344
LANE_BOTTOM = 784
```

The player’s `y` position represents the top of the logical body box.

So the actual visible feet position is approximately:

```text
player.y + PLAYER_H
```

---

# Player Box Types

The player should use separate boxes:

1. Logical Body Box
2. Collision Box
3. Hurtbox
4. Attack Hitbox
5. Visual Frame

These boxes should not be treated as the same thing.

---

# Logical Body Box

Purpose:

```text
Base coordinate system.
Anchoring reference.
Default body size.
```

Current size:

```python
PLAYER_W = 128
PLAYER_H = 256
```

Result:

```text
128 x 256
```

Debug color recommendation:

```text
Green
```

---

# Collision Box

Purpose:

```text
Feet/body blocking.
Arena movement.
Enemy separation.
```

Current settings:

```python
PLAYER_COLLISION_W = PLAYER_W * 0.5
PLAYER_COLLISION_H = PLAYER_H * 0.2
```

Result:

```text
64 x 51
```

Collision box should be centered at the bottom of the logical body box.

Recommended function:

```python
def get_collision_rect(self):
    return pygame.Rect(
        int(self.x + (self.width - PLAYER_COLLISION_W) / 2),
        int(self.y + self.height - PLAYER_COLLISION_H),
        int(PLAYER_COLLISION_W),
        int(PLAYER_COLLISION_H),
    )
```

Debug color recommendation:

```text
Blue
```

---

# Hurtbox

Purpose:

```text
Where the player can receive damage.
```

Current settings:

```python
PLAYER_HURTBOX_W = PLAYER_W * 0.6
PLAYER_HURTBOX_H = PLAYER_H * 0.6
PLAYER_HURTBOX_OFFSET_X = PLAYER_W * 0.2
PLAYER_HURTBOX_OFFSET_Y = PLAYER_H * 0.1
```

Result:

```text
Width  = 76
Height = 153
Offset X = 25
Offset Y = 25
```

Recommended function:

```python
def get_hurt_rect(self):
    return pygame.Rect(
        int(self.x + PLAYER_HURTBOX_OFFSET_X),
        int(self.y + PLAYER_HURTBOX_OFFSET_Y),
        int(PLAYER_HURTBOX_W),
        int(PLAYER_HURTBOX_H),
    )
```

Debug color recommendation:

```text
Red
```

---

# Player Default Hitbox

Current generic player hitbox:

```python
PLAYER_HITBOX_W = PLAYER_W * 0.4
PLAYER_HITBOX_H = PLAYER_H * 0.5
PLAYER_HITBOX_OFFSET_Y = PLAYER_H * 0.2
```

Result:

```text
Width  = 51
Height = 128
Offset Y = 51
```

This is currently a generic placeholder.

Future direction:

```text
Replace this generic hitbox with attack-specific hitboxes.
```

Examples:

* Fist attack hitbox
* Knee attack hitbox
* Jump attack hitbox
* Knife hitbox
* Bat hitbox
* Pistol muzzle position

---

# Grab Knee Hitbox

Current grab knee values:

```python
PLAYER_GRAB_KNEE_HITBOX_W = PLAYER_W * 0.6
PLAYER_GRAB_KNEE_HITBOX_H = PLAYER_H * 0.45
```

Result:

```text
Width  = 76
Height = 115
```

Grab knee timing:

```python
PLAYER_GRAB_KNEE_DURATION = 14
PLAYER_GRAB_KNEE_HIT_FRAME = 6
```

Meaning:

```text
Total duration = 14 frames
Damage frame   = frame 6
```

At 60 FPS:

```text
Duration ≈ 0.23 seconds
Hit frame ≈ 0.10 seconds after start
```

---

# Enemy Box Baseline

Enemy base size now follows player base size.

```python
ENEMY_W = PLAYER_W
ENEMY_H = PLAYER_H
```

Result:

```text
Normal enemy = 128 x 256
```

Enemy variants:

```python
FAST_ENEMY_W = ENEMY_W * 0.8
FAST_ENEMY_H = ENEMY_H * 0.8

HEAVY_ENEMY_W = ENEMY_W * 1.3
HEAVY_ENEMY_H = ENEMY_H * 1.3

RAPTOR_ENEMY_W = ENEMY_W * 0.8
RAPTOR_ENEMY_H = ENEMY_H * 0.8

BOSS_ENEMY_W = ENEMY_W * 2
BOSS_ENEMY_H = ENEMY_H * 2
```

Result:

```text
Fast enemy   = 102 x 204
Heavy enemy  = 166 x 332
Raptor enemy = 102 x 204
Boss enemy   = 256 x 512
```

---

# Enemy Collision Box

Current settings:

```python
ENEMY_COLLISION_W = ENEMY_W * 0.5
ENEMY_COLLISION_H = ENEMY_H * 0.2
```

For normal enemy:

```text
64 x 51
```

Like the player, enemy collision should be centered on the bottom of the logical body box.

---

# Enemy Hurtbox

Current settings:

```python
ENEMY_HURTBOX_W = ENEMY_W * 0.6
ENEMY_HURTBOX_H = ENEMY_H * 0.6
ENEMY_HURTBOX_OFFSET_X = ENEMY_W * 0.2
ENEMY_HURTBOX_OFFSET_Y = ENEMY_H * 0.1
```

For normal enemy:

```text
Width  = 76
Height = 153
Offset X = 25
Offset Y = 25
```

---

# Enemy Hitbox

Current generic enemy attack hitbox:

```python
ENEMY_HITBOX_W = ENEMY_W * 0.4
ENEMY_HITBOX_H = ENEMY_H * 0.5
ENEMY_HITBOX_OFFSET_Y = ENEMY_H * 0.2
```

For normal enemy:

```text
Width  = 51
Height = 128
Offset Y = 51
```

This is also a placeholder.

Future direction:

```text
Different enemy types should have different attack hitboxes.
```

---

# Player Visual Frame Sizes

Visual frame size is independent of logical body size.

The logical body remains:

```text
128 x 256
```

But attack frames can be wider.

---

## Idle Frame

```python
PLAYER_IDLE_FRAME_W = PLAYER_W
PLAYER_IDLE_FRAME_H = PLAYER_H
```

Result:

```text
128 x 256
```

---

## Fist Attack Frame

```python
PLAYER_FIST_FRAME_W = PLAYER_W * 1.5
PLAYER_FIST_FRAME_H = PLAYER_H
```

Result:

```text
192 x 256
```

Purpose:

```text
Allows arm and fist to extend outside the logical body box.
```

---

## Knee Attack Frame

```python
PLAYER_KNEE_FRAME_W = PLAYER_W * 1.3
PLAYER_KNEE_FRAME_H = PLAYER_H
```

Result:

```text
166 x 256
```

Purpose:

```text
Allows forward body/knee extension.
```

---

## Jump Attack Frame

```python
PLAYER_JUMP_ATTACK_FRAME_W = PLAYER_W * 1.4
PLAYER_JUMP_ATTACK_FRAME_H = PLAYER_H
```

Result:

```text
179 x 256
```

Purpose:

```text
Allows air attack extension.
```

---

## Knife Frame

```python
PLAYER_KNIFE_FRAME_W = PLAYER_W * 1.55
PLAYER_KNIFE_FRAME_H = PLAYER_H
```

Result:

```text
198 x 256
```

Purpose:

```text
Allows arm and knife extension.
```

---

## Bat Frame

```python
PLAYER_BAT_FRAME_W = PLAYER_W * 1.9
PLAYER_BAT_FRAME_H = PLAYER_H
```

Result:

```text
243 x 256
```

Purpose:

```text
Allows full bat swing extension.
```

---

## Pistol Frame

```python
PLAYER_PISTOL_FRAME_W = PLAYER_W * 1.45
PLAYER_PISTOL_FRAME_H = PLAYER_H
```

Result:

```text
185 x 256
```

Purpose:

```text
Allows extended pistol arm pose.
```

---

# Drawing Rule

When facing right:

```text
Draw visual frame from player.x.
Extra width extends to the right.
```

When facing left:

```text
Shift draw_x left by the extra visual width.
Extra width extends to the left.
```

Recommended logic:

```python
def get_visual_draw_x(self, camera_x, visual_w):
    screen_x = self.x - camera_x

    if self.facing_right:
        return screen_x

    extra_w = visual_w - self.width
    return screen_x - extra_w
```

This keeps the logical body stable while allowing the animation to extend forward.

---

# Recommended Attack-Specific Hitboxes

The current `settings.py` still has a generic player hitbox.

Recommended next step is to add attack-specific hitboxes.

Suggested values based on the new `PLAYER_W = 128`, `PLAYER_H = 256` baseline:

```python
PLAYER_FIST_HITBOX_W = PLAYER_W * 0.65
PLAYER_FIST_HITBOX_H = PLAYER_H * 0.22
PLAYER_FIST_HITBOX_OFFSET_Y = PLAYER_H * 0.33

PLAYER_COMBO2_HITBOX_W = PLAYER_W * 0.72
PLAYER_COMBO2_HITBOX_H = PLAYER_H * 0.24
PLAYER_COMBO2_HITBOX_OFFSET_Y = PLAYER_H * 0.32

PLAYER_COMBO3_HITBOX_W = PLAYER_W * 0.85
PLAYER_COMBO3_HITBOX_H = PLAYER_H * 0.26
PLAYER_COMBO3_HITBOX_OFFSET_Y = PLAYER_H * 0.31

PLAYER_JUMP_ATTACK_HITBOX_W = PLAYER_W * 0.8
PLAYER_JUMP_ATTACK_HITBOX_H = PLAYER_H * 0.35
PLAYER_JUMP_ATTACK_HITBOX_OFFSET_Y = PLAYER_H * 0.42

PLAYER_RUNNING_ATTACK_HITBOX_W = PLAYER_W * 1.05
PLAYER_RUNNING_ATTACK_HITBOX_H = PLAYER_H * 0.28
PLAYER_RUNNING_ATTACK_HITBOX_OFFSET_Y = PLAYER_H * 0.38

PLAYER_KNIFE_HITBOX_W = PLAYER_W * 0.95
PLAYER_KNIFE_HITBOX_H = PLAYER_H * 0.22
PLAYER_KNIFE_HITBOX_OFFSET_Y = PLAYER_H * 0.34

PLAYER_BAT_HITBOX_W = PLAYER_W * 1.35
PLAYER_BAT_HITBOX_H = PLAYER_H * 0.26
PLAYER_BAT_HITBOX_OFFSET_Y = PLAYER_H * 0.32

PLAYER_PISTOL_MUZZLE_OFFSET_X = PLAYER_W * 0.8
PLAYER_PISTOL_MUZZLE_OFFSET_Y = PLAYER_H * 0.28
```

With current size, this gives approximately:

```text
Fist hitbox:          83 x 56
Combo 2 hitbox:       92 x 61
Combo 3 hitbox:       108 x 66
Jump attack hitbox:   102 x 89
Running hitbox:       134 x 71
Knife hitbox:         121 x 56
Bat hitbox:           172 x 66
```

---

# Enemy Attack Timing

Current enemy timing:

```python
ENEMY_ATTACK_WINDUP = 20
ENEMY_ATTACK_ACTIVE = 8
ENEMY_ATTACK_RECOVERY = 25
ENEMY_ATTACK_COOLDOWN = 45
```

At 60 FPS:

```text
Windup   = 0.33 sec
Active   = 0.13 sec
Recovery = 0.42 sec
Cooldown = 0.75 sec
```

Enemy attack should follow:

```text
Windup -> Active -> Recovery -> Cooldown
```

Enemy damage should only happen during active frames.

---

# Animation Event Direction

Future animation system should support frame events.

Example:

```text
Frame 0-5:
startup / windup

Frame 6-9:
enable hitbox

Frame 10+:
recovery

Frame 14:
allow combo cancel
```

Future structure:

```python
animation_events = {
    "attack_1": {
        6: ["enable_hitbox"],
        10: ["disable_hitbox"],
        14: ["allow_combo"],
    }
}
```

---

# Asset Production Rules

For player sprites:

```text
Logical body reference = 128 x 256
```

Idle/walk/run frames:

```text
128 x 256
```

Attack frames may be wider:

```text
Fist:  192 x 256
Knee:  166 x 256
Jump:  179 x 256
Knife: 198 x 256
Bat:   243 x 256
Pistol:185 x 256
```

All frames must preserve foot baseline alignment.

---

# Debug Drawing Standard

Recommended debug colors:

```text
Green  = logical body box
Blue   = collision box
Red    = hurtbox
Yellow = attack hitbox
Purple = visual frame bounds
```

---

# Current Status

Approved baseline.

Based on latest `settings.py`.

Last updated:

```text
2026-06-09
```

This document should guide the next player animation, hitbox, hurtbox, and visual frame refactor work.
