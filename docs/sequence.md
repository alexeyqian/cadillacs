# 2D Game Update Loop — Frame Sequence

Per-frame update order for a 2D beat-em-up, with reasoning for each position.

---

## Update Order

### 1. Input Collection (system level)
Read raw device state (keyboard, gamepad) into a clean input snapshot. Done once per frame before any entity updates. This is just hardware → struct; no game logic runs here yet.

---

### 2. Lifecycle Guards (per entity)
Check dead / hit-stunned / frozen states **before** doing anything else with the entity.

- Dead player → run death animation, skip all input and movement
- Hit-stunned enemy → skip AI and movement

**Why before timers:** a dead entity should not process input, advance its own attack timers, or move. Guarding first keeps the rest of the update clean and free of invalid-state edge cases.

---

### 3. Timer / Cooldown Advance
Decrement all countdowns **before** anything else reads them.

- Attack animations finish → state transitions to IDLE
- Action locks expire → new actions become available
- Hit stun ends → enemy can move again
- Cooldowns tick down

**Why first:** everything after this reads timer-derived state. If you advance timers after movement or input, you're making decisions on stale state (e.g. blocking a new attack that was actually free this frame).

---

### 3. AI / State Decisions
Enemies decide what to do: patrol, chase, attack, retreat. Runs after timers so enemies see up-to-date cooldowns and states, but before movement so the decision drives this frame's movement.

---

### 4. Player Input → Action Requests
Translate input into action requests (start attack, jump, grab). Does **not** move anything yet — just determines intent based on current state.

**Why before movement:** some inputs affect how movement runs this frame (jump start, run attack momentum).

---

### 5. Movement
Apply velocity, handle running/jumping/knockback, enforce arena boundaries.

Order within movement:
1. Horizontal/vertical position update
2. Vertical physics (gravity, jump arc)
3. Arena boundary clamp

**Why after input:** player's movement path (normal vs. attack-momentum vs. jumping) depends on actions decided in step 4.

---

### 6. Collision Detection & Resolution
In order of priority:

1. **Character vs. character** (push-apart, can't overlap)
2. **Character vs. level geometry** (walls, ledges)
3. **Projectile vs. character** (hit detection)

**Why here:** positions are finalized for this frame. Resolving collisions before positions are set means you're working on last-frame data.

---

### 7. Combat — Hitbox vs. Hurtbox
For each active attack: check if its hitbox overlaps any valid target's hurtbox. If yes, create a `DamageRequest` and apply it.

**Why after movement:** hitboxes are anchored to character position. Characters must be at their final positions before checking overlap — otherwise you might miss a hit or register a phantom one.

---

### 8. Damage / Reaction Application
Apply pending `DamageRequest`s: reduce HP, trigger hit stun, start knockback, check for knockdown/death. Separate from hitbox detection so one punch can't kill-and-also-knockdown in conflicting ways.

---

### 9. Entity Lifecycle — Spawn & Cleanup
- Spawn queued enemies/projectiles (wave system triggers here)
- Remove dead/expired entities

**Why late:** you don't want to remove an entity mid-frame while other systems are still iterating over it. Spawning late means new entities start their logic next frame.

---

### 10. Animation Update
Advance animation frames for all entities based on their final state this frame.

**Why before camera:** animation commits the final visual representation of each entity — sprite frame, facing direction, any frame-level offsets. The camera should track this committed visual state, not last frame's.

---

### 11. Camera Update
Follow player/action center. Runs after animation so the camera tracks the entity's final visual state, not an intermediate one.

---

### 12. Render
Draw everything. Always last — you render the final committed state of the world.

---

## Summary Table

| Step | What | Why here |
|------|------|----------|
| 1 | Input snapshot (system) | Single source of truth; just hardware → struct, no logic |
| 2 | Lifecycle guards (per entity) | Dead/stunned entities skip all further steps |
| 3 | Timers advance | State transitions happen before anyone reads timer state |
| 4 | AI decisions | Needs current timer state, drives movement |
| 5 | Player action requests | Drives movement path choices |
| 6 | Movement | Positions finalized |
| 7 | Collision detection | Works on final positions |
| 8 | Hitbox vs hurtbox | Needs final positions; produces damage requests |
| 9 | Damage/reactions | Consumes damage requests cleanly |
| 10 | Spawn/cleanup | Safe to add/remove after all iteration |
| 11 | Animation update | Commits final visual state before camera reads it |
| 12 | Camera | Tracks final position and visual state |
| 13 | Render | Always last |

---

## Core Principle

Each step produces output that the next step consumes. Going out of order creates **one-frame lag** (acting on last frame's state) or **double-updates** (a timer ticks twice if advanced both before and after some other step reads it).

> Advance state first, read it second, render it last.
