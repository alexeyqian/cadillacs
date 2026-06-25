# Codebase Naming Guide

This project favors simple, readable names that match each class's actual job.

## Component Names

Use a direct noun-style name when the class owns one focused capability or area of logic.

Examples:

- `EnemyMovement`
- `EnemyHitboxes`
- `EnemyRenderer`
- `EnemyHealth`
- `PlayerMovement`
- `PlayerHitboxes`

These names read naturally as:

- Enemy has movement.
- Enemy has hitbox.
- Enemy has health.
- Player has movement.

Prefer this style when the class mainly answers one practical question:

- How does this entity move?
- How are its hitbox calculated?
- How is it rendered?
- How is health stored or changed?

## Controller Names

Use `SomethingController` when the class coordinates a multi-step behavior over time.

Controller classes usually manage one or more of these:

- state transitions
- timers
- phases
- start / update / finish flow
- cancel / reset behavior
- command-like actions
- interaction between multiple smaller behaviors

Examples:

- `EnemyCombatController`
- `EnemyAnimationController`
- `EnemyLifecycleController`
- `EnemyReactionController`
- `PlayerActionController`
- `PlayerGrabController`

These names are appropriate because the classes orchestrate behavior, not just calculate one thing.

## Rule of Thumb

Use:

```text
Something
```

when the class is a focused component.

Use:

```text
SomethingController
```

when the class manages a process.

## EnemyMovement Decision

Keep the name `EnemyMovement`.

It currently handles movement helpers such as:

- player distance
- facing direction
- patrol movement
- chase movement
- flanking movement
- world bounds clamping

It does not currently own a separate movement state machine, queued movement commands, or a start/update/finish lifecycle. Because of that, `EnemyMovement` is cleaner than `EnemyMovementController`.

Rename it to `EnemyMovementController` only if it grows into a class that manages movement modes or movement phases over time.

## Avoid Thin Mixins

Avoid keeping mixins that only forward calls to another component.

For example, a mixin with only this kind of behavior is usually not worth keeping:

```python
def start_attack(self):
    self.combat.start_attack(self)
```

In that case, either:

- put the forwarding method directly on the entity if it is part of the entity's public API
- move the real behavior into the correct component or controller

This keeps inheritance shallow and makes the code easier to follow.
