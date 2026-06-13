# Animation Guidelines

This guide explains practical animation frame counts, animation FPS, and combat timing values for this beat 'em up project.

The goal is not perfect arcade accuracy. The goal is clear, readable animation data that is easy to tune.

## Key Concepts

### Game Frames

The game runs at `FPS = 60`, so:

| Game Frames | Time |
|---:|---:|
| 6 | 0.10s |
| 10 | 0.17s |
| 12 | 0.20s |
| 15 | 0.25s |
| 20 | 0.33s |
| 30 | 0.50s |
| 45 | 0.75s |
| 60 | 1.00s |

### Animation FPS

Animation FPS controls how quickly sprite frames change.

Example:

```python
FERRIS_ANIM_FPS = {
    "attack": 6,
}
```

At 60 game FPS:

```text
60 / 6 = 10 game frames per sprite frame
```

So an attack animation with 3 sprite frames at 6 animation FPS takes about:

```text
3 sprite frames * 10 game frames = 30 game frames = 0.5 seconds
```

### Combat Timing

Combat timing is separate from animation FPS.

For enemy attacks:

```python
self.attack_windup = 20
self.attack_active = 8
self.attack_recovery = 25
```

| Field | Meaning |
|---|---|
| `attack_windup` | Frames before the hit can connect |
| `attack_active` | Frames where the hitbox can damage the target |
| `attack_recovery` | Frames after the hit before the attacker can act again |

For frame-data enemies, the active window should overlap sprite frames that have an `attack_rect`.

## Recommended Animation Frames

These are good starting points for a readable arcade beat 'em up.

| Action | Recommended Sprite Frames | Recommended Anim FPS | Loop? | Notes |
|---|---:|---:|---|---|
| Idle | 3-6 | 4-8 | Yes | Small breathing or stance movement. Avoid too much motion. |
| Walk | 4-8 | 8-12 | Yes | Should clearly show foot movement and weight shift. |
| Run | 4-8 | 10-15 | Yes | Faster than walk, with stronger forward lean. |
| Jump Start | 1-3 | 8-12 | No | Optional. Squash/launch pose before airborne frame. |
| Jump / Airborne | 1-3 | 6-10 | Optional | Usually held while character is in air. |
| Landing | 1-3 | 8-12 | No | Optional. Helps make jumps feel heavier. |
| Light Attack | 3-5 | 8-12 | No | Anticipation, strike, recovery. |
| Heavy Attack | 4-8 | 6-10 | No | Longer windup and recovery. |
| Weapon Attack | 4-8 | 8-12 | No | Hitbox should cover weapon during active frames. |
| Projectile Shoot | 3-6 | 8-12 | No | Spawn projectile on the firing/release frame. |
| Hit Reaction | 1-3 | 8-15 | No | Short readable flinch. |
| Knockdown | 2-5 | 6-10 | No | Fall or thrown-to-ground motion. |
| Get Up | 3-6 | 6-10 | No | Should leave character vulnerable until finished. |
| Dead | 3-8 | 6-10 | No | Ends on final grounded/dead pose. |
| Grabbed | 1-2 | 4-8 | Optional | Usually held while player controls grab. |
| Throw | 3-6 | 8-12 | No | Release target on the throw/release frame. |
| Boss Intro | 6-12 | 6-10 | No | Large readable entrance or roar. |
| Boss Special | 6-12 | 6-10 | No | Telegraph clearly before damage. |

## Recommended Timing Windows

Use these as starting values, then tune by feel.

### Enemy Attacks

| Attack Type | Windup | Active | Recovery | Total | Feel |
|---|---:|---:|---:|---:|---|
| Fast jab | 8-14 | 4-6 | 12-18 | 24-38 | Quick, interruptible, low damage |
| Normal punch | 14-22 | 5-8 | 18-28 | 37-58 | Standard enemy attack |
| Heavy swing | 24-35 | 8-12 | 30-45 | 62-92 | Slow but threatening |
| Weapon swing | 18-30 | 8-14 | 25-40 | 51-84 | Active longer because weapon has reach |
| Ranged shot | 20-35 | 1-3 | 25-45 | 46-83 | Projectile spawns during active/release frame |
| Boss attack | 30-50 | 10-20 | 35-60 | 75-130 | Strong telegraph, strong punishment |

### Player Attacks

| Attack Type | Startup | Active | Recovery | Total | Feel |
|---|---:|---:|---:|---:|---|
| Combo hit 1 | 5-8 | 4-6 | 8-14 | 17-28 | Fast opener |
| Combo hit 2 | 6-10 | 4-6 | 10-16 | 20-32 | Slightly slower follow-up |
| Combo finisher | 10-16 | 6-10 | 18-28 | 34-54 | More damage, more recovery |
| Running attack | 8-14 | 8-12 | 18-30 | 34-56 | Long reach, risky if missed |
| Jump attack | 4-8 | 8-20 | 8-18 | variable | Active while falling or during kick pose |
| Weapon swing | 8-16 | 8-14 | 16-28 | 32-58 | Strong reach, readable timing |

## How To Match Animation FPS With Timing

For frame-data enemies, follow this workflow:

1. Decide which sprite frame visually shows the strike.
2. Put `attack_rect` only on that frame, or on a few frames where the weapon/fist is dangerous.
3. Set `attack_windup` so the active window starts when that sprite frame appears.
4. Set `attack_active` so it lasts only while the strike frame is visible.
5. Set `attack_recovery` so the attacker cannot immediately repeat the attack.

Example with 3 attack frames at 6 animation FPS:

| Sprite Frame | Game Frames | Purpose |
|---:|---:|---|
| 0 | 0-9 | Windup / anticipation |
| 1 | 10-19 | More windup / body twist |
| 2 | 20-29 | Punch extended, has `attack_rect` |

Good timing:

```python
self.attack_windup = 20
self.attack_active = 8
self.attack_recovery = 25
```

That means the attack can hit during frames 20-27, while sprite frame 2 is visible.

## Hitbox Guidelines

### Hurtboxes

Hurtboxes represent vulnerable body parts.

| Action | Hurtbox Guideline |
|---|---|
| Idle / Walk / Run | Cover torso, head, and legs. Keep it slightly smaller than the visible sprite. |
| Attack | Keep shoulder/body vulnerable. Extended arm may be vulnerable if you want counter-hits. |
| Jump | Cover body in air. Avoid huge boxes that feel unfair. |
| Hit | Usually same as body, or slightly wider if the sprite leans back. |
| Dead | Usually no hurtbox, or only for thrown-body collision if needed. |

### Attack Rectangles

Attack rectangles represent dangerous parts of the animation.

| Attack | Attack Rect Guideline |
|---|---|
| Punch / Kick | Cover fist/boot plus 10-15 pixels of forearm/shin. |
| Knife / Pipe | Cover the full weapon length plus the hand holding it. |
| Shoulder tackle | Cover chest, shoulder, and leading arm. |
| Jump kick | Cover foot and lower leg during the kick pose. |
| Boss slam | Use a larger box, but telegraph it clearly with longer windup. |

For this project's frame-data format:

```python
"attack_rect": (x, y, width, height)
```

The values are local to the current sprite frame before scaling.

If `sprite_scale = 4`, then:

```text
(30, 10, 20, 8) becomes 120x40 pixels in the game world
```

## State-Specific Guidelines

### Idle

Idle should be calm and readable.

Recommended:

```text
3-6 frames
4-8 animation FPS
looping
```

Avoid large movement because it makes hitboxes look unstable.

### Walk

Walk animation should match movement speed.

Recommended:

```text
4-8 frames
8-12 animation FPS
looping
```

If feet slide, adjust either:

- movement speed
- animation FPS
- sprite frame spacing

### Run

Run needs stronger motion than walk.

Recommended:

```text
4-8 frames
10-15 animation FPS
looping
```

Use for player dash/run or fast enemies.

### Attack

A clear attack usually has:

| Phase | Visual |
|---|---|
| Windup | Arm pulls back, body twists, weapon raises |
| Active | Fist/weapon extended |
| Recovery | Body returns to stance |

Recommended:

```text
3-6 frames for normal attacks
4-8 frames for heavy attacks
8-12 animation FPS for quick attacks
6-10 animation FPS for heavy attacks
```

Only put `attack_rect` on active strike frames.

### Hit

Hit reactions should be short.

Recommended:

```text
1-3 frames
8-15 animation FPS
duration: 10-20 game frames
```

Too long makes combat feel sluggish. Too short makes hits feel weak.

### Knockdown And Get Up

Use knockdown for heavy attacks, throws, explosions, and boss hits.

Recommended:

| State | Frames | Anim FPS | Duration |
|---|---:|---:|---:|
| Knockdown fall | 2-5 | 6-10 | 20-40 game frames |
| Grounded pause | 1 | held | 30-90 game frames |
| Get up | 3-6 | 6-10 | 30-60 game frames |

### Dead

Death animation should end on a final pose.

Recommended:

```text
3-8 frames
6-10 animation FPS
do not loop
```

After the animation finishes, keep the final frame visible for a short time before cleanup.

## Suggested Defaults For This Project

Use this table when adding a new enemy.

| Enemy Type | Idle FPS | Walk FPS | Attack FPS | Hit FPS | Dead FPS | Windup | Active | Recovery |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Basic enemy | 6 | 8 | 6 | 12 | 8 | 18-22 | 6-8 | 20-28 |
| Fast enemy | 8 | 12 | 10 | 14 | 10 | 8-14 | 4-6 | 12-18 |
| Heavy enemy | 4 | 6 | 6 | 10 | 8 | 26-35 | 8-12 | 30-45 |
| Ranged enemy | 6 | 8 | 8 | 12 | 8 | 22-35 | 1-3 | 30-45 |
| Boss | 4-6 | 6 | 5-8 | 8-10 | 6 | 30-50 | 10-20 | 35-60 |

## Practical Checklist

Before considering an animation finished:

- The sprite faces the correct default direction for the entity class.
- `facing_right` flips the sprite correctly.
- Hurtboxes stay aligned with the visible body.
- Attack rectangles appear only on dangerous frames.
- `attack_windup` starts before the `attack_rect` frame.
- `attack_active` overlaps the `attack_rect` frame.
- The attack can hit the player from both left and right.
- The recovery is long enough that repeated enemy attacks do not feel unfair.
- The animation FPS does not make feet slide during movement.

## Common Mistakes

| Problem | Likely Cause | Fix |
|---|---|---|
| Enemy visually faces wrong direction | Source sprite direction does not match draw flip logic | Confirm whether source art faces left or right, then adjust flip logic |
| Attack never hits | `attack_rect` is `None`, on wrong frame, or active window misses it | Move `attack_rect` or adjust `attack_windup` |
| Attack hits behind the enemy | Mirroring math is wrong for `attack_rect` | Test left and right side attacks |
| Attack feels unfair | Windup too short or active window too long | Increase windup, shorten active, add clearer animation |
| Combat feels sluggish | Recovery too long or hit reaction too long | Reduce recovery/hit-stun carefully |
| Feet slide while walking | Animation FPS does not match movement speed | Tune walk FPS or movement speed |

## Recommended Long-Term Structure

For maintainability, keep animation timing close to animation data:

```python
FERRIS_ATTACK_TIMING = {
    "windup": 20,
    "active": 8,
    "recovery": 25,
}
```

Then `FerrisEnemy` can load timing from data instead of hardcoding values in the class.

This makes it easier to add new enemy types without scattering animation tuning across multiple files.
