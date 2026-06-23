# Player Jump Design

## Design Goal

Jump should feel like an arcade beat 'em up action, not a platformer system.
The player moves on the ground plane with `x` and `y`, while jump height is a
separate fake vertical value.

Recommended model:

```text
ground position: x, y
fake height: z
vertical motion: jump_velocity_z + gravity
state flow: takeoff -> jump / jump_attack -> landing
```

The sprite should draw higher on screen while airborne:

```python
draw_x = self.x
draw_y = self.y - self.z
```

Most collision can still use the player's ground position. Attack and hurtboxes
can be visually adjusted by `z`.

## Recommended Player States

Add air states to the existing player state machine:

```text
IDLE
WALK
JUMP_TAKEOFF
JUMP
JUMP_ATTACK
LANDING
HIT
DEAD
```

Keep jump attack separate from the standing combo chain at first. A jump attack
should be one simple action, not `ATTACK`, `ATTACK2`, `ATTACK3`.

## Core Jump Fields

Recommended fields for `Player`:

```python
self.is_grounded = True
self.z = 0
self.jump_velocity_z = 0
self.air_time = 0
self.jump_direction_x = 0
self.jump_direction_y = 0
self.has_used_jump_attack = False
self.jump_attack_hit_enemies = set()
```

Suggested first tuning values at 60 FPS:

```python
self.jump_power = 12
self.gravity = 0.7
self.air_move_speed = 3.0
self.landing_recovery_frames = 6
```

This should produce a short arcade jump instead of a floaty platformer jump.

## Takeoff

`JUMP_TAKEOFF` should be a short commitment state, around 4-6 frames.

Purpose:

- Play a readable takeoff animation.
- Capture the starting jump direction.
- Prevent jump and attack from happening on the exact same frame.
- Make jump feel intentional instead of instant.

Example behavior:

```python
if jump_pressed and self.is_grounded:
    self.state = PlayerState.JUMP_TAKEOFF
    self.takeoff_timer = 6
    self.jump_direction_x = input_x
    self.jump_direction_y = input_y
```

When takeoff ends:

```python
self.state = PlayerState.JUMP
self.is_grounded = False
self.z = 1
self.jump_velocity_z = self.jump_power
self.air_time = 0
self.has_used_jump_attack = False
self.jump_attack_hit_enemies.clear()
```

## Air Time

Use simple gravity:

```python
self.z += self.jump_velocity_z
self.jump_velocity_z -= self.gravity
self.air_time += 1

if self.z <= 0:
    self.land()
```

Air time should continue during jump attack. The attack should not freeze the
player in midair.

## Air Movement

Move on the ground plane while airborne:

```python
self.x += self.jump_direction_x * self.air_move_speed
self.y += self.jump_direction_y * self.air_move_speed * 0.6
```

Recommended feel:

- Lock most of the jump direction at takeoff.
- Allow only small air correction.
- Do not allow instant full reversal in the air.
- Make depth movement slower than horizontal movement.

## Landing

Landing should be its own short state, around 4-8 frames.

Purpose:

- Play landing animation or dust later.
- Reset air state.
- Prevent immediate jump/attack spam.
- Leave room for input buffering in a future milestone.

Example:

```python
def land(self):
    self.is_grounded = True
    self.z = 0
    self.jump_velocity_z = 0
    self.air_time = 0
    self.state = PlayerState.LANDING
    self.landing_timer = self.landing_recovery_frames
```

When landing recovery ends, return to `WALK` or `IDLE` based on movement input.

## Jump Attack

Start with one jump attack per jump:

```python
if attack_pressed and not self.is_grounded and not self.has_used_jump_attack:
    self.state = PlayerState.JUMP_ATTACK
    self.has_used_jump_attack = True
    self.jump_attack_timer = 18
```

Recommended timing:

| Phase | Frames | Meaning |
| --- | ---: | --- |
| Startup | 4 | Leg begins extending |
| Active | 8 | Attack can hit |
| Recovery | 6 | Leg retracts / body prepares to land |

If the player lands during jump attack, resolve the current frame and transition
to `LANDING`.

## Fist Or Foot?

Use foot for the default jump attack.

Reason:

- In beat 'em ups, the standard jump attack usually reads as a flying kick.
- The foot gives a clear forward striking point.
- The body can stay vulnerable while the leg is dangerous.
- It has better reach than a fist without making the whole body a hitbox.
- It visually separates air combat from the standing punch combo.

Recommended default:

```text
normal jump attack = flying kick / knee-forward kick
```

Use fist later only as a character-specific variation:

```text
fast character: jump kick
heavy character: air body press or elbow
weapon user: downward weapon swing
special move: jumping punch or diving punch
```

For Mustapha, a fast forward jump kick is the best first implementation.

## Jump Attack Hitbox

For the default flying kick, place the hitbox around the foot and lower leg,
not the whole body.

Hitbox rule:

- The foot and lower leg are dangerous.
- The torso and head remain vulnerable hurtboxes.
- The hitbox is active only during active frames.
- Each enemy should be hit only once per jump attack.

Example shape:

```python
attack_box = pygame.Rect(
    self.rect.centerx + self.facing_direction * 25,
    self.rect.centery - self.z + 10,
    42,
    28,
)
```

Tune this after the real jump attack sprite is checked in game.

## Input Recommendation

Current project input baseline maps:

```text
SPACE = jump
J = attack
K = fire
L = grab
Q = drop
SHIFT = run
```

This works, but jump is likely more important than firing in normal combat.
Jump should be close to the attack button so the player can do jump attacks
comfortably.

Recommended keyboard controls:

| Action | Keyboard |
| --- | --- |
| Ground attack | `J` |
| Jump / hop | `K` |
| Fire weapon | `U` or `I` |
| Grab / interact | `L` |
| Drop weapon | `Q` |
| Run | `SHIFT` |
| Jump attack | Press `J` while airborne |
| Directional jump | Hold direction + `K` |
| Forward jump attack | Hold direction + `K`, then press `J` |

Recommended action cluster:

```text
J = attack
K = jump
L = grab / interact
U or I = fire weapon
```

Reason:

- `J` and `K` are next to each other, which makes jump attack easy.
- Jump is used more often than firing, so it should sit in the primary action
  cluster.
- Fire is still reachable, but moved away from the main attack/jump rhythm.
- `SPACE` can remain an alternate jump key for players who expect it.

Best practical default:

```text
K = primary jump
SPACE = alternate jump
J = punch / kick / melee attack
U = fire weapon
L = grab
```

Do not require `K + J` at the exact same time. That is harder to control and can
create input timing bugs. The player should jump first, then press attack in the
air.

Optional future combinations:

| Action | Keyboard |
| --- | --- |
| Running jump attack | Hold `SHIFT` + direction, press `K`, then `J` |
| Downward air attack | Hold `DOWN`, press `J` while airborne |
| Special attack | `J + K` or another explicit special button later |

## Collision Rules

First implementation rules:

- Player cannot pick up weapons while airborne.
- Player cannot start ground combos while airborne.
- Jump attack can hit each enemy once.
- Player body collision can still use ground `x` and `y`.
- Player sprite rendering uses `y - z`.
- If hit while airborne, transition to `HIT`; air knockdown can come later.

Keep the first version forgiving. Arcade beat 'em ups usually allow jump attacks
to hit grounded enemies even when the player is visually above the floor, as
long as the attack box overlaps clearly.

## Implementation Plan

### Step 1: Add Air State Data

- Add `JUMP_TAKEOFF`, `JUMP`, `JUMP_ATTACK`, and `LANDING` to player states.
- Add `z`, `jump_velocity_z`, `air_time`, `is_grounded`, and jump direction
  fields to the player.
- Add simple constants for jump power, gravity, air speed, and landing recovery.

### Step 2: Add Basic Jump

- Start jump when `SPACE` is pressed on the ground.
- Enter `JUMP_TAKEOFF` for 4-6 frames.
- Transition to `JUMP` and apply gravity each update.
- Land when `z <= 0`.
- Draw the player at `y - z`.

### Step 3: Add Air Movement

- Capture initial input direction at takeoff.
- Move `x` and `y` during jump using air speed.
- Clamp movement to world and lane bounds.
- Keep depth movement slower than horizontal movement.

### Step 4: Add Landing Recovery

- Add `LANDING` timer.
- Return to `IDLE` or `WALK` after landing recovery.
- Prevent pickup, ground combo, and new jump during landing recovery.

### Step 5: Add Jump Attack

- Allow `J` during `JUMP`.
- Enter `JUMP_ATTACK`.
- Continue gravity and air movement during the attack.
- Add startup, active, and recovery timing.
- Track `jump_attack_hit_enemies` so each enemy is hit once.

### Step 6: Integrate Combat Collision

- Add jump attack hitbox data.
- Resolve jump attack damage during active frames.
- Apply knockback and hit stun to enemies.
- Keep the player's body hurtbox vulnerable.

### Step 7: Animation And Polish

- Hook up `player_jump.png` and `player_jump_attack.png`.
- Add takeoff and landing animation mapping if available.
- Add landing dust and sound later.
- Tune jump height, gravity, active frames, and hitbox size after playing.

## Non-Goals For First Version

- Do not build a complex physics engine.
- Do not add wall collision or platforming rules.
- Do not support multiple jump attacks per jump.
- Do not add air throws yet.
- Do not add air knockdown until the basic jump feels good.
