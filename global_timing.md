# Global Timing Guidelines

This project should use base timing values plus scalers.

The main benefit is that the whole game can be tuned faster or slower without manually editing every enemy, player, animation, cooldown, and hit-stun number.

## Core Idea

Keep readable base values:

```python
BASE_WINDUP = 20
BASE_ACTIVE = 8
BASE_RECOVERY = 25
```

Then apply a global preset:

```python
windup = scale_frames(BASE_WINDUP, COMBAT_TIMING_SCALE)
active = scale_active_frames(BASE_ACTIVE, COMBAT_TIMING_SCALE)
recovery = scale_frames(BASE_RECOVERY, COMBAT_TIMING_SCALE)
```

This keeps individual attacks understandable while still allowing global tuning.

## Why Not Use One Scaler For Everything?

One master scaler can work for debug or turbo mode, but it is usually too blunt for game balance.

Movement, animation, and combat timing affect the game differently.

| Scaler | Affects | Example |
|---|---|---|
| Animation scale | Sprite playback speed | walk cycle, attack animation, hit reaction |
| Combat scale | Timing windows | windup, active, recovery, cooldowns |
| Movement scale | World movement | player speed, enemy chase speed |
| Projectile scale | Projectile travel speed | bullets, thrown objects, enemy projectiles |

For example, making animations 20% faster does not always mean movement should also be 20% faster. If movement changes too much, spacing and hitboxes can stop feeling fair.

## Recommended Presets

Use presets for quick testing.

| Preset | Animation Scale | Combat Scale | Movement Scale | Feel |
|---|---:|---:|---:|---|
| `slow` | 0.90 | 1.15 | 0.90 | Easier and more readable |
| `normal` | 1.00 | 1.00 | 1.00 | Default balance |
| `fast` | 1.15 | 0.90 | 1.10 | Snappier arcade feel |
| `turbo` | 1.30 | 0.75 | 1.20 | Fast testing or hard mode |

Important detail:

```text
Higher animation scale = faster animation.
Lower combat scale = shorter combat timing.
```

So fast mode usually uses:

```text
animation scale > 1.0
combat scale < 1.0
movement scale > 1.0
```

## Scaling Game Frames

Most gameplay timing values are measured in game frames.

Examples:

- attack windup
- attack active frames
- attack recovery
- attack cooldown
- hit-stun
- knockdown duration
- get-up duration
- spawn delay
- invulnerability duration

Use:

```python
scale_frames(base_frames, scale)
```

Example:

```python
scale_frames(20, 0.9)  # 18 frames
scale_frames(20, 1.15) # 23 frames
```

## Scaling Active Frames

Active frames should not become too short.

If a punch has only 1 active frame, it may feel broken because collision can easily miss.

Use a minimum active window:

```python
scale_active_frames(base_active, scale, minimum=3)
```

Recommended minimums:

| Attack Type | Minimum Active Frames |
|---|---:|
| Fast jab | 3 |
| Normal punch | 4 |
| Heavy swing | 5 |
| Weapon swing | 5 |
| Boss attack | 6 |

## Scaling Animation FPS

Animation FPS means how quickly sprite frames advance.

Use:

```python
scale_animation_fps(base_fps, animation_scale)
```

Example:

```python
scale_animation_fps(6, 1.15) # 6.9 FPS
```

This is okay because the animation system converts FPS into frame duration:

```python
frame_duration = int(GAME_FPS / animation_fps)
```

## Scaling Movement

Movement speed can be scaled directly:

```python
enemy.speed = scale_speed(BASE_ENEMY_SPEED, movement_scale)
```

Be careful with movement scaling. If enemies move faster but attack range and timing stay the same, they may feel unfair.

## Recommended Implementation Pattern

Use base values near the enemy/player definition:

```python
BASE_FERRIS_ATTACK_TIMING = {
    "windup": 20,
    "active": 8,
    "recovery": 25,
}
```

Then apply global tuning in the entity:

```python
timing = scale_timing(
    windup=20,
    active=8,
    recovery=25,
)

self.attack_windup = timing["windup"]
self.attack_active = timing["active"]
self.attack_recovery = timing["recovery"]
self.attack_total_duration = timing["total"]
```

## Practical Rules

- Store base values, not already-scaled values.
- Apply scalers once during initialization.
- Keep combat timing and animation FPS separate.
- Do not scale active frames below a useful minimum.
- Test attacks from both left and right after changing timing.
- Test slow, normal, and fast presets before accepting a new enemy.

## Future Direction

Eventually, each enemy can define base animation and combat data:

```python
FERRIS_TIMING = {
    "attack": {
        "windup": 20,
        "active": 8,
        "recovery": 25,
    },
    "cooldown": 45,
}
```

Then all final gameplay values are produced through `game.tuning`.

That keeps enemy data easy to read and makes global game-speed tuning predictable.
