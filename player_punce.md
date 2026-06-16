# Player Punch Design Summary

## Goal

Make the normal fist attack feel closer to a classic arcade beat 'em up punch:

- readable windup
- clear active impact pose
- visible recovery/retract posture
- combat timing remains the source of truth
- animation supports the combat phases instead of replacing them

## Current Combat Timing

The player fist combo uses three attack phases in code:

| Attack | Windup | Active | Recovery |
| --- | ---: | ---: | ---: |
| ATTACK_1 | 8 | 4 | 3 |
| ATTACK_2 | 8 | 4 | 5 |
| ATTACK_3 | 8 | 4 | 6 |

The active hitbox is only available during the active phase.

## 3-Phase Animation Plan

Use three animation frames for the normal fist punch:

| Frame | Phase | Visual Purpose |
| --- | --- | --- |
| 1 | Windup | Guard up, shoulder/body preparing to punch |
| 2 | Active | Full fist extension, impact pose |
| 3 | Recovery | Fist retracts toward guard, body returns |

This makes the animation easier to debug:

- frame 1 means "attack is coming"
- frame 2 means "hitbox should be active"
- frame 3 means "attack is ending, player is recovering"

## Current Applied Asset

The fist attack now uses:

```text
assets/player/mustapha_attack_3phase_preview.png
```

Frame layout:

| Frame | Rect | Offset | Notes |
| --- | --- | --- | --- |
| Windup | `(0, 0, 111, 168)` | `(-60, -168)` | Existing windup frame |
| Active | `(111, 0, 193, 168)` | `(-63, -168)` | Existing full punch frame |
| Recovery | `(304, 0, 140, 168)` | `(-76, -168)` | New retract/recovery pose |

The labeled visual reference is:

```text
assets/player/mustapha_attack_3phase_preview_labeled.png
```

## Important Design Notes

Combat timing should stay independent from animation FPS. The code decides when
the hitbox is active; the animation explains that timing visually.

The recovery frame is important because it prevents the punch from looking like
it snaps directly from full extension back to idle or the next combo step.

## Recommended Next Steps

1. Set normal attack animation FPS to 10 or 12 after judging the 3-frame punch in game.
2. Split combo visuals later:
   - ATTACK_1: quick jab
   - ATTACK_2: stronger straight punch
   - ATTACK_3: heavier finisher with more body twist
3. Tune hitboxes after animation feels right:
   - ATTACK_1: shorter reach
   - ATTACK_2: medium reach
   - ATTACK_3: larger finisher hitbox
4. Consider a tiny forward nudge on ATTACK_3 only, not on every punch.
