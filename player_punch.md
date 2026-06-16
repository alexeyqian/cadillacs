# Player Fist Punch / Attack Design

## Reference Direction

Cadillacs and Dinosaurs is a Capcom side-scrolling beat 'em up. Its combat is
primarily close-range melee against groups of enemies, with each playable
character having different strengths and special attacks.

Important reference ideas for this project:

- Fist attacks should be readable, fast, and physical.
- The player should understand when a punch is preparing, when it can hit, and
  when it is recovering.
- Combo hits should not feel like one generic repeated pose.
- Mustapha is a fast character, so his punches should feel quick and efficient,
  while his movement attacks carry more range and momentum.
- Charge attacks can hit one or several enemies, but normal fist attacks should
  usually be more focused.

Reference sources:

- English overview: https://en.wikipedia.org/wiki/Cadillacs_and_Dinosaurs_(video_game)
- Spanish gameplay notes and Mustapha attributes: https://es.wikipedia.org/wiki/Cadillacs_and_Dinosaurs_(videojuego)
- Portuguese gameplay overview: https://pt.wikipedia.org/wiki/Cadillacs_and_Dinosaurs

## Project Combat Model

The player punch already uses a three-phase combat model:

| Phase | Meaning |
| --- | --- |
| Windup | The attack is starting, but cannot hit yet |
| Active | The hitbox is active and can damage enemies |
| Recovery | The attack is ending, and the player is committed |

Current fist combo timing:

| Attack | Windup | Active | Recovery | Role |
| --- | ---: | ---: | ---: | --- |
| ATTACK_1 | 8 | 4 | 3 | quick opener |
| ATTACK_2 | 8 | 4 | 5 | middle combo hit |
| ATTACK_3 | 8 | 4 | 6 | heavier finisher |

The code timing is the source of truth. Animation should communicate the timing
visually, but collision should continue to use attack data.

## Applied Animation Baseline

The normal fist attack now uses a three-frame animation:

```text
assets/player/mustapha_attack_3phase_preview.png
```

Frame mapping:

| Frame | Combat Phase | Visual |
| --- | --- | --- |
| 1 | Windup | guard / punch preparation |
| 2 | Active | full fist extension |
| 3 | Recovery | fist retracts toward guard |

Recommended animation speed:

```python
"attack": 12
```

This keeps the punch snappy while still showing the recovery posture.

## Combo Animation Slots

The player animation controller supports separate combo animation states:

```text
ATTACK_1 -> attack_1
ATTACK_2 -> attack_2
ATTACK_3 -> attack_3
```

Mustapha now has separate three-phase sheets for each combo punch:

```text
attack_1 -> assets/player/mustapha_attack_1.png
attack_2 -> assets/player/mustapha_attack_2.png
attack_3 -> assets/player/mustapha_attack_3.png
```

The current art is still conservative and derived from the same base punch, but
the game now has separate animation data for each combo step. This makes later
pose refinement much easier.

## Hitbox Design

Current fist attacks use a light progression:

```python
ATTACK_1: AttackHitboxData(x=92, y=-300, width=135, height=38)
ATTACK_2: AttackHitboxData(x=94, y=-300, width=160, height=40)
ATTACK_3: AttackHitboxData(x=96, y=-304, width=185, height=48)
```

This keeps the opener quick and focused, preserves the second hit as the medium
baseline, and makes the finisher visibly/mechanically larger.

Applied hitbox direction:

| Attack | Suggested Hitbox Feel |
| --- | --- |
| ATTACK_1 | shorter, quick jab |
| ATTACK_2 | medium straight punch |
| ATTACK_3 | wider/taller finisher |

## Counter-Hurtbox Design

The current punch includes a counter-hurtbox for the extended limb:

```python
AttackHitboxData(x=54, y=-300, width=40, height=40)
```

Design intent:

- the fist can hit enemies during active frames
- the extended limb can also be punished if the player is mistimed
- the shoulder/body should remain vulnerable instead of the whole attack being
  completely safe

This fits the current counter-hit direction for the project.

## Combo Feel Goals

The fist combo should eventually feel like:

1. ATTACK_1: fast opener, low commitment
2. ATTACK_2: stronger follow-up, slightly more recovery
3. ATTACK_3: finisher, more impact and more commitment

Important: do not make every punch equally large or equally safe. The finisher
should feel better, but it should also be easier to punish if whiffed.

## Next Recommended Steps

1. Watch the 3-frame punch in game and confirm the recovery posture reads well.
2. If the punch feels too twitchy, reduce only Mustapha's `attack` FPS to 10.
3. Improve the actual silhouettes for `attack_2` and `attack_3` with more
   hand-drawn body twist and weight.
4. Retune hitboxes after the distinct combo silhouettes are final.
5. Consider a tiny forward nudge only on `ATTACK_3`, not on every punch.

## Visual Preview Notes

Generated preview assets:

```text
assets/player/mustapha_attack_combo_preview_labeled.png
assets/player/mustapha_attack_combo_preview_12fps.gif
```

Current visual finding:

- The combo is technically separated into three sheets.
- The 3-phase structure reads clearly.
- `attack_2` has a stronger shoulder/guard variation than the opener.
- `attack_3` has a heavier body lean and more committed recovery.
- These sheets are still derived from the same base punch, so the next art pass
  can improve them further with true hand-drawn body twist and weight.

## Non-Goals For Now

- Do not build a complex ECS combat system.
- Do not make fist attacks hit many enemies by default.
- Do not couple animation frames directly to collision logic.
- Do not remove the attack-data-driven phase system.
