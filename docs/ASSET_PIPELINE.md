# Asset Pipeline

Cadillacs & Dinosaurs Pygame Project

Version: 1.0

Last Updated: 2026-06-08

---

# Purpose

This document defines:

* Asset folder structure
* Naming conventions
* Sprite sheet organization
* Animation architecture
* Loading workflow
* Future expansion guidelines

The goal is to keep assets manageable as the project grows.

---

# Asset Design Goals

Assets should be:

* Easy to locate
* Easy to replace
* Easy to expand
* Consistent naming
* Programmer friendly

---

# Root Structure

```text
project/

assets/
├── characters/
├── enemies/
├── weapons/
├── effects/
├── ui/
├── backgrounds/
├── audio/
├── fonts/
└── data/
```

---

# Characters

```text
assets/characters/

jack/
├── spritesheet.png
├── spritesheet.json
└── portrait.png

hannah/
├── spritesheet.png
├── spritesheet.json
└── portrait.png
```

Each character should be self-contained.

---

# Enemies

```text
assets/enemies/

punk/
├── spritesheet.png
├── spritesheet.json

brute/
├── spritesheet.png
├── spritesheet.json

boss/
├── spritesheet.png
├── spritesheet.json
```

---

# Weapons

```text
assets/weapons/

knife.png
club.png
rifle.png
rock.png
```

---

# Effects

```text
assets/effects/

hit_spark.png
dust.png
explosion.png
```

---

# UI

```text
assets/ui/

health_bar.png
life_icon.png
score_panel.png
```

---

# Audio

```text
assets/audio/

music/
sfx/
voice/
```

Example:

```text
audio/

music/
stage1.ogg

sfx/
punch.wav
kick.wav
throw.wav
```

---

# Data Files

```text
assets/data/

animations/
enemies/
stages/
```

---

# Animation Data Files

Future JSON files:

```text
assets/data/animations/

jack.json
punk.json
brute.json
```

---

# Animation Naming Convention

Use lowercase.

Examples:

```text
idle
walk
run

punch1
punch2
punch3

kick

jump
fall
land

grab
throw

hurt

knockdown
getup

dead
```

Avoid:

```text
IdleAnimation
WalkAnimation
PunchAnimation01
```

---

# Sprite Sheet Rules

One sprite sheet per character.

Example:

```text
jack/

spritesheet.png
spritesheet.json
```

Advantages:

* Easy replacement
* Easy modding
* Easier debugging

---

# Recommended Sprite Sheet Layout

```text
Idle Frames

0 1 2 3

Walk Frames

4 5 6 7 8 9

Punch Frames

10 11 12 13
```

Grouped by animation.

Never randomly scatter frames.

---

# Animation Metadata Example

Example:

```json
{
  "idle": {
    "frames": [0,1,2,3],
    "fps": 8,
    "loop": true
  },

  "walk": {
    "frames": [4,5,6,7,8,9],
    "fps": 12,
    "loop": true
  },

  "punch1": {
    "frames": [10,11,12,13],
    "fps": 15,
    "loop": false
  }
}
```

---

# Animation Architecture

Future Classes

```text
SpriteSheet
Animation
AnimationSet
AnimationPlayer
AssetManager
```

Responsibilities:

SpriteSheet

* Extract frames

Animation

* Frame sequence
* Playback speed

AnimationSet

* Collection of animations

AnimationPlayer

* Current animation
* Frame timing

AssetManager

* Loading
* Caching
* Sharing resources

---

# Loading Flow

```text
Game Starts

↓

AssetManager Loads

↓

SpriteSheet Loaded

↓

Frames Extracted

↓

Animations Built

↓

Cached

↓

Ready For Use
```

---

# Asset Cache Rules

Never load the same image repeatedly.

Bad:

```python
pygame.image.load(...)
```

inside update loops.

Good:

```python
AssetManager.load_image(...)
```

once during initialization.

Reuse afterwards.

---

# Future Stage Assets

```text
backgrounds/

stage1/
stage2/
stage3/
```

Example:

```text
stage1/

background.png
collision.json
spawn_points.json
```

---

# Future Enemy Data

```text
assets/data/enemies/

punk.json
brute.json
boss.json
```

Example:

```json
{
  "health": 30,
  "speed": 4,
  "damage": 8
}
```

---

# Future Stage Data

```text
assets/data/stages/

stage1.json
stage2.json
```

Example:

```json
{
  "world_width": 3840,
  "camera_locks": [
    [800, 1200],
    [2200, 2600]
  ]
}
```

---

# Future Modding Support

Long-term goal:

Allow adding content without changing code.

Possible:

```text
assets/
data/
mods/
```

New enemies could be added by:

* PNG
* JSON

Only.

No Python changes required.

---

# Current Priority

Next Milestone:

Animation Framework

Required Components:

1. SpriteSheet
2. Animation
3. AnimationPlayer
4. AssetManager
5. Character Animation Integration

After completion:

Proceed to Combat Foundation milestone.

---

# Asset Pipeline Principles

1. One responsibility per asset.
2. One sprite sheet per character.
3. One JSON per asset type.
4. Cache everything.
5. Never hardcode frame indices in gameplay code.
6. Data-driven whenever practical.
7. Organize for future multiplayer and modding support.

```
```
