# Animation System

Cadillacs & Dinosaurs Pygame Project

Version: 1.0

Last Updated: 2026-06-08

---

# Purpose

This document defines the animation system architecture for the Pygame beat-em-up project.

The goal is to make animation:

* Easy to understand
* Easy to debug
* Easy to expand
* Data-driven where practical
* Ready for combat timing integration

---

# Design Goals

The animation system should support:

* Idle animation
* Walk animation
* Run animation
* Jump animation
* Attack animation
* Hurt animation
* Knockdown animation
* Death animation
* Enemy attack windup / active / recovery
* Animation events such as hit frames

The system should avoid:

* Hardcoded frame indices inside gameplay code
* Loading images inside update loops
* Duplicated animation logic between player and enemy

---

# Core Classes

Recommended classes:

```text
SpriteSheet
Animation
AnimationPlayer
AnimationSet
AssetManager
```

---

# Class Responsibilities

## SpriteSheet

Responsible for:

* Holding one loaded sprite sheet image
* Extracting frames from the sheet
* Returning individual frame surfaces

Should not handle:

* Animation timing
* Entity state
* Combat logic

---

## Animation

Responsible for:

* List of frames
* Frame duration
* Loop setting
* Optional animation events

Should not handle:

* Drawing position
* Movement
* Combat decisions

---

## AnimationPlayer

Responsible for:

* Current animation
* Current frame index
* Timer
* Loop handling
* Detecting animation finished
* Triggering animation events

Should not handle:

* Entity AI
* Player input
* Damage calculation

---

## AnimationSet

Responsible for:

* Storing animations by name

Example:

```text
idle
walk
run
punch1
punch2
hurt
knockdown
dead
```

---

## AssetManager

Responsible for:

* Loading images once
* Loading JSON once
* Caching resources
* Returning shared assets

---

# Suggested File Layout

```text
src/
├── animation.py
├── spritesheet.py
├── asset_manager.py
```

or:

```text
src/core/
├── animation.py
├── spritesheet.py
├── asset_manager.py
```

---

# Asset Layout

```text
assets/
├── characters/
│   └── jack/
│       ├── spritesheet.png
│       └── animations.json
│
├── enemies/
│   └── punk/
│       ├── spritesheet.png
│       └── animations.json
```

---

# Animation JSON Example

```json
{
  "frame_width": 80,
  "frame_height": 160,

  "animations": {
    "idle": {
      "frames": [0, 1, 2, 3],
      "fps": 8,
      "loop": true
    },

    "walk": {
      "frames": [4, 5, 6, 7, 8, 9],
      "fps": 12,
      "loop": true
    },

    "punch1": {
      "frames": [10, 11, 12, 13],
      "fps": 15,
      "loop": false,
      "events": {
        "2": ["hit"]
      }
    }
  }
}
```

---

# Frame Indexing Rule

Frames are indexed left to right, top to bottom.

Example:

```text
0  1  2  3
4  5  6  7
8  9  10 11
```

---

# Animation Timing

Use FPS-based timing.

Example:

```text
animation fps = 12
game fps = 60
```

This means:

```text
60 / 12 = 5
```

Each animation frame lasts 5 game frames.

---

# Recommended Animation Speeds

## Player

```text
idle: 6-8 fps
walk: 10-12 fps
run: 14-16 fps
punch: 14-18 fps
kick: 12-16 fps
hurt: 10-12 fps
knockdown: 8-10 fps
```

## Enemy

```text
idle: 4-6 fps
walk: 8-10 fps
attack_windup: 8-12 fps
attack_active: 12-16 fps
attack_recovery: 8-12 fps
hurt: 10-12 fps
dead: 6-8 fps
```

---

# Entity State to Animation Mapping

Each entity state should map to an animation name.

Example:

```python
STATE_TO_ANIMATION = {
    "idle": "idle",
    "walk": "walk",
    "run": "run",
    "punch": "punch1",
    "hurt": "hurt",
    "knockdown": "knockdown",
    "dead": "dead",
}
```

Gameplay code changes state.

Animation system plays the matching animation.

---

# Player Animation States

Recommended player states:

```text
idle
walk
run
jump
fall
land
punch1
punch2
punch3
kick
running_attack
hurt
knockdown
getup
dead
```

---

# Enemy Animation States

Recommended enemy states:

```text
idle
walk
chase
attack_windup
attack_active
attack_recovery
hurt
knockdown
getup
dead
```

---

# Combat Animation Events

Animations may contain events.

Example:

```json
"punch1": {
  "frames": [10, 11, 12, 13],
  "fps": 15,
  "loop": false,
  "events": {
    "2": ["hit"]
  }
}
```

Meaning:

When animation reaches local frame index 2, trigger hit detection.

---

# Supported Event Types

Initial event types:

```text
hit
footstep
attack_start
attack_end
invulnerable_start
invulnerable_end
sound
effect
```

Start simple.

First implementation only needs:

```text
hit
```

---

# Enemy Windup / Active / Recovery

Enemy combat can be animation-driven.

Recommended mapping:

```text
attack_windup   -> warning animation
attack_active   -> damaging animation
attack_recovery -> punishable animation
```

Example timing:

```text
windup: 20 frames
active: 10 frames
recovery: 25 frames
```

The enemy should only create a damaging hitbox during:

```text
attack_active
```

---

# AnimationPlayer Behavior

Required methods:

```python
play(name, reset=True)
update()
get_current_frame()
is_finished()
consume_events()
```

---

# play(name, reset=True)

Behavior:

* If animation is already playing, do nothing
* If animation changes, switch to new animation
* Reset frame index when reset is true

---

# update()

Behavior:

* Advance timer
* Change frame when enough time passed
* Loop if animation loops
* Stop on final frame if animation does not loop
* Collect events for current frame

---

# get_current_frame()

Returns:

```python
pygame.Surface
```

The current frame image.

---

# is_finished()

Returns true when:

* Current animation is non-looping
* Final frame has completed

Useful for:

* Returning from punch to idle
* Returning from hurt to chase
* Returning from recovery to chase

---

# consume_events()

Returns and clears animation events.

Example:

```python
events = animation_player.consume_events()

if "hit" in events:
    perform_hit_check()
```

---

# Drawing Rule

Entity controls position.

Animation controls image.

Example:

```python
image = self.animation_player.get_current_frame()
screen.blit(image, (screen_x, screen_y))
```

---

# Flipping Rule

Do not store duplicate left and right frames.

Store one direction.

Use:

```python
pygame.transform.flip(image, True, False)
```

when facing left.

---

# Performance Rule

Do not flip every frame repeatedly if performance becomes an issue.

Future optimization:

* Cache flipped frames

For now:

* Simple runtime flip is acceptable

---

# Minimal First Implementation

First version should implement:

1. SpriteSheet frame extraction
2. Animation class
3. AnimationPlayer class
4. Manual animation definitions in Python
5. Player idle / walk switching

Do not start with full JSON loading unless needed.

---

# Second Implementation

Add:

1. JSON animation loading
2. Animation events
3. Enemy animation support
4. Attack animation support

---

# Third Implementation

Add:

1. Sound events
2. Effect events
3. Footstep events
4. Cached flipped frames

---

# Debug Tools

Recommended debug display:

```text
Current state
Current animation
Current frame index
Animation finished
Triggered events
```

This helps debug combat timing.

---

# Common Bugs

## Bug 1

Animation restarts every frame.

Cause:

```python
play("walk")
```

called every update with reset true.

Fix:

Only reset if animation name changed.

---

## Bug 2

Attack never finishes.

Cause:

Non-looping animation finish state not checked.

Fix:

Use:

```python
if animation_player.is_finished():
    state = "idle"
```

---

## Bug 3

Hit triggers multiple times.

Cause:

Same frame event checked repeatedly.

Fix:

Events should be consumed once.

---

## Bug 4

Image loads repeatedly.

Cause:

Loading inside update or draw.

Fix:

Load once through AssetManager.

---

# Integration With Combat

Combat should ask animation:

```text
Did hit event happen?
```

Combat should not ask:

```text
Is current frame index 2?
```

This keeps combat independent from exact frame numbers.

---

# Integration With Enemy AI

Enemy AI controls state:

```text
chase
attack_windup
attack_active
attack_recovery
```

Animation system displays matching animation.

Combat system enables hitbox only during:

```text
attack_active
```

---

# Final Design Principle

Gameplay chooses what the character is doing.

Animation shows what the character is doing.

Combat reacts to animation events.

These systems should stay separate.
