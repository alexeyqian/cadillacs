# AI Prompts For Mustapha Combo Punch Sprite Sheets

Use these prompts in another game AI art platform to generate improved
`attack_2` and `attack_3` sprite sheets.

## Shared Requirements

Use these constraints for both prompts:

- Character: Mustapha-style male arcade beat 'em up fighter.
- Preserve the existing outfit: green shirt/vest, yellow pants, brown boots, yellow/orange cap.
- Preserve the same pixel-art style, palette feel, black pixel outlines, and 1990s Capcom arcade sprite proportions.
- Side-view beat 'em up sprite, facing right.
- Output must be a horizontal sprite sheet with exactly 3 frames.
- Frames represent: windup, active punch, recovery.
- Use a flat solid blue background matching old sprite sheets, or transparent background if supported.
- No shadows, no floor, no text, no labels, no extra characters, no effects.
- Keep the same approximate character height and anchor behavior as the existing Mustapha attack sheet.
- Make the frames cleanly separable for slicing.

Reference files in this project:

```text
assets/player/mustapha_attack.png
assets/player/mustapha_attack_3phase_preview.png
assets/player/mustapha_attack_2.png
assets/player/mustapha_attack_3.png
```

## Prompt: Attack 2 Sprite Sheet

```text
Create a 3-frame horizontal pixel-art sprite sheet for a Mustapha-style arcade beat 'em up fighter performing the second punch in a combo.

Character and style:
- 1990s Capcom arcade beat 'em up pixel art style.
- Same character design as Mustapha: green shirt/vest, yellow pants, brown boots, yellow/orange cap, athletic slim build.
- Facing right, side-view brawler perspective.
- Keep the same approximate height, proportions, color palette, black outlines, and sprite density as the reference Mustapha attack sprite.

Animation frames:
Frame 1: windup. The fighter rotates his shoulders slightly more than a jab, guard hand raised, punching arm drawn back, weight shifting forward.
Frame 2: active punch. A stronger straight punch than the first jab, arm fully extended to the right, shoulder and torso rotated into the punch, opposite arm balancing near the body.
Frame 3: recovery. The fist retracts toward guard, torso still slightly twisted, feet planted, body returning to neutral but not fully idle.

Composition:
- Output as one horizontal sprite sheet with exactly 3 frames: windup, active, recovery.
- Keep generous spacing between frames so they can be sliced cleanly.
- Flat solid blue background or transparent background if supported.
- No labels, no text, no effects, no extra characters, no shadows.

Important:
- Do not change the character costume.
- Do not make it look like a kick or weapon attack.
- Do not make the active frame identical to the first punch; it should feel like a stronger second combo hit with more shoulder rotation.
```

## Prompt: Attack 3 Sprite Sheet

```text
Create a 3-frame horizontal pixel-art sprite sheet for a Mustapha-style arcade beat 'em up fighter performing the third punch / combo finisher.

Character and style:
- 1990s Capcom arcade beat 'em up pixel art style.
- Same character design as Mustapha: green shirt/vest, yellow pants, brown boots, yellow/orange cap, athletic slim build.
- Facing right, side-view brawler perspective.
- Keep the same approximate height, proportions, color palette, black outlines, and sprite density as the reference Mustapha attack sprite.

Animation frames:
Frame 1: heavy windup. The fighter winds up more dramatically than the first two punches, torso coiled, front shoulder pulled back, guard hand up, weight loaded into the rear leg.
Frame 2: active finisher punch. A powerful committed straight or cross punch to the right, arm fully extended, torso strongly twisted, shoulder driving forward, stance wider and heavier than attack 1 and attack 2.
Frame 3: recovery. Clear follow-through/retract posture after the heavy punch, torso leaning forward slightly, punching arm coming back toward guard, body visibly committed and recovering before returning to idle.

Composition:
- Output as one horizontal sprite sheet with exactly 3 frames: heavy windup, active finisher, recovery.
- Keep generous spacing between frames so they can be sliced cleanly.
- Flat solid blue background or transparent background if supported.
- No labels, no text, no effects, no extra characters, no shadows.

Important:
- Do not change the character costume.
- Do not make it a kick, uppercut, weapon swing, or special attack.
- The third punch must feel heavier and more committed than attack 1 and attack 2.
- Make the recovery frame especially readable: the player should clearly look like he is retracting after a powerful punch, not snapping back to idle.
```

## Optional Negative Prompt

```text
Avoid modern smooth illustration, 3D rendering, anime redesign, realistic lighting, blur, motion trails, oversized effects, changed costume, changed character identity, front-facing pose, weapon, kick, jump attack, extra characters, floor shadows, text labels, watermark.
```

## Suggested Output Targets

After generating, save as:

```text
assets/player/mustapha_attack_2_ai.png
assets/player/mustapha_attack_3_ai.png
```

Then update `game/animation/mustapha_data.py` frame rectangles after measuring the generated sheet dimensions.
