# Timer Guidelines

This project uses two common timer styles:

- elapsed timers: `timer += 1`
- countdown timers: `timer -= 1`

Both are useful. The important thing is to use each style consistently.

## Game Frames

The game runs at `FPS = 60`.

| Frames | Time |
|---:|---:|
| 6 | 0.10s |
| 10 | 0.17s |
| 15 | 0.25s |
| 20 | 0.33s |
| 30 | 0.50s |
| 45 | 0.75s |
| 60 | 1.00s |

Most gameplay timers in this project are measured in game frames.

## Elapsed Timers

Elapsed timers count upward.

```python
self.attack_timer += 1
```

Use elapsed timers when you care about how far into an action you are.

Good for:

- attack windup / active / recovery
- animation phase checks
- combo timing
- throw timing
- spawning a projectile on a specific frame
- applying damage on a specific attack frame

Example:

```python
self.attack_timer += 1

active_start = self.attack_windup
active_end = self.attack_windup + self.attack_active

if active_start <= self.attack_timer < active_end:
    damage_player()

if self.attack_timer >= self.attack_total_duration:
    finish_attack()
```

Meaning:

| `attack_timer` | Meaning |
|---:|---|
| 0 | Attack just started |
| 1-19 | Windup |
| 20-27 | Active hit frames |
| 28-52 | Recovery |
| 53 | Attack finished |

Elapsed timers are best when an action has multiple phases.

## Countdown Timers

Countdown timers count downward.

```python
self.hit_stun_remaining -= 1
```

Use countdown timers when you only care about how much time remains.

Good for:

- cooldowns
- hit-stun remaining
- knockdown duration
- get-up duration
- invulnerability duration
- death cleanup delay
- respawn delay
- UI message duration
- spawn delay

Example:

```python
if self.attack_cooldown > 0:
    self.attack_cooldown -= 1

if self.attack_cooldown <= 0:
    can_attack = True
```

Meaning:

| `attack_cooldown` | Meaning |
|---:|---|
| 45 | Wait 45 more frames |
| 20 | Wait 20 more frames |
| 1 | Last blocked frame |
| 0 | Ready |

Countdown timers are best when a state just needs to expire.

## Quick Rule

| Situation | Timer Style |
|---|---|
| Need exact frame inside an action | `timer += 1` |
| Need phase windows like windup/active/recovery | `timer += 1` |
| Need to trigger something on frame 20 | `timer += 1` |
| Need to wait until time expires | `timer -= 1` |
| Need cooldown behavior | `timer -= 1` |
| Need temporary state duration | `timer -= 1` |

## Naming Guidelines

Timer names should make the direction obvious.

Project convention:

```python
*_timer       # elapsed timer, counts upward with += 1
*_cooldown    # cooldown countdown, counts downward with -= 1
*_remaining   # non-cooldown countdown, counts downward with -= 1
*_duration    # fixed duration value
*_window      # fixed input/combo window value
```

### Good Names For Elapsed Timers

Use these when counting upward:

```python
attack_timer
phase_timer
animation_timer
```

These names imply "how long this action has been running." Keep `_timer`
for elapsed timers only.

### Good Names For Countdown Timers

Use `_cooldown` for cooldowns that count downward:

```python
attack_cooldown
shoot_cooldown
special_attack_cooldown
```

Use `_remaining` for other timers that count downward:

```python
hit_stun_remaining
respawn_remaining
death_remaining
action_lock_remaining
throw_remaining
grab_knee_remaining
knockdown_remaining
getup_remaining
phase_message_remaining
```

Long names are acceptable when they prevent confusion.

## Reset Rules

Always reset timers at the moment a state starts.

Example:

```python
def start_attack(self):
    self.state = self.ATTACK
    self.attack_timer = 0
    self.attack_has_hit = False
```

For countdown timers:

```python
def take_damage(self):
    self.state = self.HIT
    self.hit_stun_remaining = 15
```

Avoid resetting timers every frame while already in the state. That causes the state to never finish.

## Avoid Negative Countdown Bugs

Countdown timers often go below zero if not clamped.

This is usually okay:

```python
if self.hit_stun_remaining > 0:
    self.hit_stun_remaining -= 1
```

This is also okay:

```python
self.hit_stun_remaining -= 1
if self.hit_stun_remaining <= 0:
    finish_hit_state()
```

But avoid using exact equality:

```python
if self.hit_stun_remaining == 0:
    finish_hit_state()
```

Prefer:

```python
if self.hit_stun_remaining <= 0:
    finish_hit_state()
```

This is safer if the timer ever skips, starts at zero, or becomes negative.

## Avoid Exact Equality For Elapsed Triggers

For elapsed timers, exact equality can be okay for one-frame events:

```python
if self.attack_timer == self.attack_windup:
    spawn_projectile()
```

But range checks are safer for hit detection:

```python
if active_start <= self.attack_timer < active_end:
    check_attack_collision()
```

Use exact equality only when the event should happen once.

Use a boolean guard when needed:

```python
if self.attack_timer >= release_frame and not self.projectile_spawned:
    spawn_projectile()
    self.projectile_spawned = True
```

This is safer than relying on one exact frame.

## Cooldowns

Cooldowns should usually be countdown timers.

Example:

```python
if self.attack_cooldown > 0:
    self.attack_cooldown -= 1

if self.attack_cooldown <= 0:
    self.start_attack()
```

When an attack ends:

```python
self.attack_cooldown = self.attack_cooldown_duration
```

Do not count cooldown upward unless you need to know how long the cooldown has been running.

## Attack Timers

Attack timers should usually count upward.

This makes windup, active, and recovery easy to read:

```python
self.attack_timer += 1

active_start = self.attack_windup
active_end = self.attack_windup + self.attack_active

if active_start <= self.attack_timer < active_end:
    check_hit()

if self.attack_timer >= self.attack_total_duration:
    end_attack()
```

This maps naturally to animation timing:

```text
0-19   windup
20-27  active
28-52  recovery
53     done
```

## Animation Timers

Animation frame timers usually count upward internally.

Example:

```python
self.timer += 1
if self.timer >= self.frame_duration:
    self.timer = 0
    self.current_frame += 1
```

This is correct because the animation needs to know when enough frames have elapsed to advance to the next sprite frame.

## Hit-Stun And Invulnerability

Hit-stun and invulnerability usually work best as countdown timers.

Example:

```python
if self.hit_stun_remaining > 0:
    self.hit_stun_remaining -= 1
    return
```

Example:

```python
if self.invulnerable_remaining > 0:
    self.invulnerable_remaining -= 1
```

Then collision can check:

```python
if self.invulnerable_remaining <= 0:
    self.take_damage(damage)
```

## Frame Scaling

Do not use global frame scaling for gameplay timers right now.

Keep fixed values explicit:

```python
self.hit_stun_remaining = 15
self.attack_cooldown_duration = 45
```

## Common Mistakes

| Problem | Cause | Fix |
|---|---|---|
| State never ends | Timer is reset every frame | Reset timer only when entering the state |
| Cooldown never reaches zero | Countdown is not decremented | Decrement it in the update loop |
| Attack hits at wrong time | Active window does not match animation frame | Align `attack_windup` with the frame that has `attack_rect` |
| Attack sometimes misses unfairly | Active window too short | Increase `attack_active` or minimum active frames |
| One-frame event fires repeatedly | Missing boolean guard | Add `projectile_spawned`, `attack_has_hit`, or similar |
| Timer check fails after going negative | Used `== 0` | Use `<= 0` for countdown completion |
| Timer names are confusing | Countdown timer uses `_timer` suffix | Rename cooldowns to `_cooldown` and other countdowns to `_remaining` |

## Recommended Pattern

For a multi-phase action:

```python
def start_attack(self):
    self.state = self.ATTACK
    self.attack_timer = 0
    self.attack_has_hit = False

def update_attack(self, player):
    self.attack_timer += 1

    active_start = self.attack_windup
    active_end = self.attack_windup + self.attack_active

    if active_start <= self.attack_timer < active_end:
        if not self.attack_has_hit:
            self.try_hit_player(player)

    if self.attack_timer >= self.attack_total_duration:
        self.state = self.IDLE
        self.attack_timer = 0
        self.attack_has_hit = False
        self.attack_cooldown = self.attack_cooldown_duration
```

For a simple temporary state:

```python
def start_hit_stun(self):
    self.state = self.HIT
    self.hit_stun_remaining = 15

def update_hit_state(self):
    self.hit_stun_remaining -= 1
    if self.hit_stun_remaining <= 0:
        self.state = self.IDLE
```

## Project Rule Of Thumb

Use `+= 1` when the timer answers:

```text
How far into this action are we?
```

Use `-= 1` when the timer answers:

```text
How much time is left?
```
