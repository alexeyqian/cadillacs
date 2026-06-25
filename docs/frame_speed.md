# Player Animation Timing Guidelines

Project runs at `FPS = 60`.

Animation frame duration is calculated as:

```python
frame_duration = max(1, round(60 / animation_fps))
```

Examples:

| Target Animation FPS | Game Frames Per Animation Frame |
|---:|---:|
| 6 FPS | 10 frames |
| 10 FPS | 6 frames |
| 12 FPS | 5 frames |
| 15 FPS | 4 frames |
| 20 FPS | 3 frames |

## Recommended Animation Settings

| Action | Art Frames | Target Anim FPS | Approx Total Time | Notes |
|---|---:|---:|---:|---|
| Idle | 4-8 | 4-8 FPS | 0.7-1.5 sec loop | Slow breathing/stance. Avoid looking nervous. |
| Walk | 6-10 | 8-12 FPS | 0.5-1.0 sec loop | Match footfalls to movement speed. |
| Run | 6-8 | 12-16 FPS | 0.35-0.65 sec loop | Faster than walk, sharper contact frames. |
| Jump | 4-8 | 10-15 FPS | Physics-driven | Animation follows jump state, not jump height. |
| Fist Attack | 3-6 | 15-24 FPS | 0.15-0.35 sec | Snappy. Active hitbox usually 1-2 art frames. |
| Leg Attack / Kick | 4-7 | 12-20 FPS | 0.25-0.45 sec | Slightly heavier than punch. Active hitbox 1-3 art frames. |
| Run Attack | 4-8 | 12-20 FPS | 0.25-0.55 sec | Short startup, readable impact, slightly longer recovery. |
| Jump Attack | 4-6 | 12-18 FPS | Physics-driven | Active frames may last longer while airborne. |
| Grab Hold | 1-4 | 4-8 FPS | Held / loop | Mostly pose or struggle loop. |
| Grab Knee | 3-5 | 15-20 FPS | 0.18-0.35 sec | Hit on knee extension frame. |
| Throw | 5-8 | 12-18 FPS | 0.35-0.65 sec | Needs readable windup, release, recovery. |
| Hit / Hurt | 2-4 | 12-18 FPS | 0.15-0.35 sec | Should interrupt clearly. |
| Dead / Knockdown | 4-8 | 8-14 FPS | 0.4-0.9 sec | Slower and heavier. Usually non-looping later. |

## Suggested Starting Constants

```python
ANIM_FPS_IDLE = 6
ANIM_FPS_WALK = 10
ANIM_FPS_RUN = 14

ANIM_FPS_ATTACK = 18
ANIM_FPS_RUN_ATTACK = 16
ANIM_FPS_JUMP_ATTACK = 14

ANIM_FPS_JUMP = 12
ANIM_FPS_GRAB = 6
ANIM_FPS_GRAB_KNEE = 18
ANIM_FPS_THROW = 14
ANIM_FPS_HIT = 14
ANIM_FPS_DEAD = 10
```

## Attack Timing Rule

Most attacks should be designed in three parts:

```text
startup -> active -> recovery
```

Example light punch at 60 FPS:

```text
startup: 4-6 game frames
active: 3-5 game frames
recovery: 6-10 game frames
total: 13-21 game frames
```

Example heavier kick:

```text
startup: 6-8 game frames
active: 4-8 game frames
recovery: 10-16 game frames
total: 20-32 game frames
```

## Data-Driven Hitbox Rule

Use animation data to control when attacks are active:

```python
"attack_rect": None       # startup / recovery / inactive frame
"attack_rect": (...)      # active hit frame
```

Animation speed controls how the move feels.

`attack_rect` timing controls when the move can actually hit.

## Tuning Guidelines

If an animation looks too slow:

```text
Increase animation FPS.
```

If an animation looks too twitchy:

```text
Decrease animation FPS or add more art frames.
```

If gameplay feels unfair:

```text
Adjust startup / active / recovery frames.
Do not rely only on changing animation FPS.
```

If a hit feels too strong:

```text
Reduce active frames.
Shrink attack_rect.
Add recovery.
```

If a hit feels weak or hard to land:

```text
Add 1 active frame.
Move attack_rect closer to the visible fist/foot.
Slightly increase attack_rect size.
```

## Beat 'Em Up Rule Of Thumb

Idle and movement should feel smooth and readable.

Attacks should feel snappy, but the active hitbox should only appear on frames where the fist, foot, weapon, or body mass is visibly dangerous.

Do not make every attack frame active.
