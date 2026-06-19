# Player And Enemy Class Design

## Goal

This document defines the recommended class design for player and enemy entities in this beat-em-up project.

The preferred inheritance shape is:

```text
GameObject
  Character
    Player
    Enemy
```

The main goal is to keep shared game mechanics in common classes while keeping player input and enemy AI separate.

```text
Share mechanics, not decisions.
```

Players and enemies both move, animate, collide, attack, take damage, and die. The main difference is who decides the next action:

- `Player` actions come from input.
- `Enemy` actions come from AI/state resolution.

## Design Principles

- Keep classes easy to understand and easy to test.
- Use small shared base classes for truly shared behavior.
- Use components/controllers for movement, combat, animation, lifecycle, geometry, and rendering.
- Use managers/systems for groups of objects or cross-entity rules.
- Keep enemy types and player types data-driven where possible.
- Avoid moving too much behavior into inheritance. Prefer composition for behavior that changes often.
- Preserve existing comments where possible because they document learning and design intent.

## Class Responsibilities

### GameObject

`GameObject` is the smallest common base for things that exist in the world.

Common fields:

```python
id
x
y
width
height
active
visible
```

Common responsibilities:

- Store world position.
- Store basic size.
- Provide a minimal `update()` and `draw()` interface.
- Provide basic frame or bounds helpers if useful.

`GameObject` should not know about health, attacks, AI, or input.

### Character

`Character` is the shared base for living combat actors.

Common fields:

```python
display_name
state
facing_right
speed
sprite_scale

health
movement
combat
lifecycle
geometry
animation_controller
renderer
```

Common responsibilities:

- Track shared combat state.
- Apply damage through a common method shape.
- Expose shared geometry methods:
  - `get_frame_rect()`
  - `get_collision_rect()`
  - `get_hurt_rect()`
  - `get_attack_rect()`
- Expose shared rendering and animation hooks.
- Apply world/lane bounds.

`Character` should contain mechanics that are true for both player and enemy. It should not read keyboard input and should not choose enemy AI behavior.

### Player

`Player` is a `Character` controlled by player input.

Player-specific fields:

```python
player_id
player_type
input_state
air
grab
weapon_slot
events
lives
score
```

Player-specific responsibilities:

- Load player config.
- Convert input state into actions through player controllers.
- Handle player-only combat actions such as combo attacks, jump attacks, run attacks, grabs, throws, and weapon usage.
- Manage player-only lifecycle rules such as lives or continue flow, if not handled by a system.

### Enemy

`Enemy` is a `Character` controlled by AI/state resolution.

Enemy-specific fields:

```python
enemy_id
enemy_type
archetype
spawn_x
patrol_direction
detect_range
attack_range
attack_lane_range
score_points
loot_generated
```

Enemy-specific responsibilities:

- Load enemy config.
- Choose behavior based on player distance, lane position, coordination, and current state.
- Execute patrol, chase, attack, grabbed, thrown, knockdown, and death behavior.
- Generate loot or score rewards.

Enemy types should remain easy to expand through `enemy_config`, factories, and behavior/controller composition.

## Common Components

The current codebase already has a good component direction. Continue using this style.

Useful shared or parallel components:

```text
Geometry
Movement
CombatController
LifecycleController
AnimationController
Renderer
StateResolver
ReactionController
Health
WeaponSlot
```

Some components may remain player/enemy-specific at first:

```text
PlayerMovement
EnemyMovement
PlayerCombatController
EnemyCombatController
PlayerAnimationController
EnemyAnimationController
```

Do not force them to merge too early. First create common interfaces and shared base fields. Merge only when duplication becomes obvious and safe.

## Recommended Folder Structure

Use a classic game-project structure with clear ownership boundaries.

Recommended long-term shape:

```text
game/
  main.py
  settings.py
  tuning.py
  colors.py

  core/
    game_loop.py
    game_state.py
    events.py

  entities/
    game_object.py
    character.py
    player.py
    enemy.py
    projectile.py
    weapon.py
    loot.py
    breakable_object.py

  components/
    health.py
    movement.py
    geometry.py
    lifecycle.py
    renderer.py
    state_machine.py

  controllers/
    player_action_controller.py
    player_combat_controller.py
    player_grab_controller.py
    enemy_combat_controller.py
    enemy_lifecycle_controller.py
    enemy_reaction_controller.py
    enemy_state_resolver.py

  systems/
    combat_system.py
    collision_system.py
    enemy_system.py
    wave_system.py
    loot_system.py
    projectile_system.py
    camera_system.py
    gameplay_system.py

  managers/
    asset_manager.py
    input_manager.py
    score_manager.py
    announcement_manager.py
    stage_clear_manager.py

  animation/
    animation.py
    animation_config.py
    animation_manager.py
    animation_controller.py
    frame_animation.py
    spritesheet.py
    asset_loader.py

  combat/
    attack_data.py
    attack_manager.py
    combat_geometry.py
    hit_reaction.py

  data/
    players.py
    enemies.py
    weapons.py
    attacks.py

  factories/
    player_factory.py
    enemy_factory.py
    weapon_factory.py

  level/
    level.py
    lane.py
    prop.py
    wave.py
    stage_config.py
    stage_manager.py

  ui/
    hud.py
    score_view.py
    announcements.py

  effects/
    hit_spark.py
    explosion.py
    floating_text.py

  assets/
    ...
```

This is a target structure, not a one-step migration. The current project already has many of these concepts, but some are still grouped under `game/entities` or `game/systems`.

### Folder Responsibilities

`entities/` should contain world objects and their public game-facing API.

Examples:

```text
Player
Enemy
Weapon
Projectile
Loot
BreakableObject
```

`components/` should contain reusable parts that can attach to entities.

Examples:

```text
Health
Movement
Geometry
Lifecycle
Renderer
StateMachine
```

`controllers/` should contain per-entity behavior coordinators.

Examples:

```text
PlayerActionController
EnemyStateResolver
EnemyReactionController
```

`systems/` should contain cross-object rules.

Examples:

```text
CombatSystem
CollisionSystem
WaveSystem
LootSystem
```

`managers/` should contain long-lived services or collection owners.

Examples:

```text
AssetManager
InputManager
ScoreManager
AnnouncementManager
```

`combat/` should contain combat-specific data and helpers that are shared by player, enemy, weapons, and systems.

Examples:

```text
AttackData
AttackManager
HitReaction
CombatGeometry
```

`data/` should contain data definitions and registries. This keeps stats and tuning separate from behavior code.

Examples:

```text
players.py
enemies.py
weapons.py
attacks.py
```

`factories/` should contain object creation logic when construction becomes more than a few lines.

Examples:

```text
EnemyFactory
PlayerFactory
WeaponFactory
```

### Migration Notes For Current Code

Do not move files just to make the tree look tidy. Move a file when it clarifies ownership or reduces coupling.

Likely future moves:

```text
game/entities/entity.py              -> game/entities/game_object.py
game/entities/attack_data.py         -> game/combat/attack_data.py
game/entities/attack_manager.py      -> game/combat/attack_manager.py
game/entities/combat_geometry.py     -> game/combat/combat_geometry.py
game/entities/hit_reaction.py        -> game/combat/hit_reaction.py
game/entities/player_config.py       -> game/data/players.py
game/entities/enemy_config.py        -> game/data/enemies.py
game/entities/enemy_factory.py       -> game/factories/enemy_factory.py
game/assets/asset_manager.py         -> game/managers/asset_manager.py
game/ui/score_manager.py             -> game/managers/score_manager.py
```

These moves should happen after `GameObject` and `Character` exist, because stable base classes make imports easier to reason about.

## State Management

Prefer one main state value over many competing booleans.

Good:

```python
state = CharacterState.IDLE
```

Risky:

```python
is_idle = True
is_walking = False
is_attacking = False
is_hit = False
is_dead = False
```

Some supporting flags are still useful:

```python
is_invincible
can_cancel_attack
loot_generated
```

Recommended state categories:

```text
IDLE
WALK
RUN
CHASE
PATROL
ATTACK
JUMP
JUMP_ATTACK
HIT
RECOIL
GRABBED
THROWN
KNOCKDOWN
GETUP
DEAD
```

Player and enemy do not need exactly the same states, but shared states should use shared names where possible.

## Combat Model

Combat should use hitboxes, hurtboxes, timing, and attack data rather than hardcoded distance checks.

Recommended flow:

```text
Controller requests attack
Character enters attack state
Animation/attack timing advances
Attack active frames expose hitbox
Combat system checks hitbox vs hurtbox
Target receives damage/reaction
Attack remembers already-hit targets
Character enters recovery or next combo state
```

Important combat objects:

```python
AttackData
AttackManager
HitReaction
CombatGeometry
```

Important rules:

- Visual sprite size is not the same as collision size.
- Collision box, hurtbox, and attack hitbox should stay separate.
- Attack data should describe startup, active, and recovery timing.
- Each attack instance should remember targets already hit to prevent repeated damage every frame.
- Weapons should modify or replace attack data rather than adding special-case logic everywhere.

## Manager, System, Controller

Use these names consistently.

### Controller

A controller decides or performs behavior for one object.

Examples:

```text
PlayerActionController
PlayerCombatController
EnemyCombatController
EnemyLifecycleController
EnemyReactionController
```

Use a controller when the logic belongs to one entity and needs access to that entity's fields.

### Manager

A manager owns or coordinates a collection.

Examples:

```text
EnemyManager
EntityManager
AnnouncementManager
StageClearManager
ScoreManager
```

Use a manager when the object is responsible for many instances or a long-lived service.

### System

A system applies game rules across multiple objects.

Examples:

```text
CollisionSystem
CombatSystem
EnemySystem
WaveSystem
LootSystem
CameraSystem
```

Use a system when behavior depends on relationships between objects, such as player attacks hitting enemies or enemies colliding with each other.

Simple rule:

```text
Controller = controls one thing.
Manager = owns or coordinates many things.
System = applies rules across many things.
```

## Data-Driven Expansion

Player types, enemy types, weapons, and attacks should be mostly driven by config/data.

Good direction:

```text
player_config.py
enemy_config.py
attack_data.py
weapon.py
enemy_factory.py
```

Avoid scattering checks like this:

```python
if enemy.enemy_type == "brute":
    ...
elif enemy.enemy_type == "fast":
    ...
```

Prefer config plus replaceable behavior:

```python
enemy = Enemy(..., enemy_type="gneiss")
enemy.state_resolver = EnemyStateResolver(...)
enemy.combat.attack_data = config.attack
```

Later, if needed, add registries:

```python
ENEMY_AI_REGISTRY = {
    "basic_melee": BasicMeleeAI,
    "charger": ChargerAI,
    "ranged": RangedAI,
}
```

## Refactoring Plan

Each step should be medium-sized and independently testable. Do not refactor everything in one pass.

### Step 1: Rename And Clarify The Base Entity

Goal:

Create the intended root type without changing behavior.

Tasks:

- Rename or wrap `game/entities/entity.py` so it provides `GameObject`.
- Keep a temporary `Entity = GameObject` compatibility alias if many imports still use `Entity`.
- Define the minimal common fields: `x`, `y`, `width`, `height`, `active`, `visible`.
- Keep `update()` and `draw()` as simple extension points.
- Add small tests only if there is existing coverage around entity construction.

Expected result:

```text
GameObject exists and is safe to inherit from.
No Player or Enemy behavior changes yet.
```

### Step 2: Introduce Character As A Shared Base

Goal:

Create `game/entities/character.py` and move only the safest shared fields/method shapes into it.

Tasks:

- Make `Character(GameObject)`.
- Add shared fields that both `Player` and `Enemy` already use:
  - `x`
  - `y`
  - `state`
  - `facing_right`
  - `speed`
  - `sprite_scale`
  - `geometry`
  - `animation_controller`
  - `renderer`
- Add shared method interfaces:
  - `draw(screen, camera_x)`
  - `get_frame_rect()`
  - `get_collision_rect()`
  - `get_hurt_rect()`
  - `get_attack_rect()`
  - `apply_world_bounds(...)`
- Keep implementation thin and delegate to existing components.

Expected result:

```text
Character exists, but Player and Enemy can still behave exactly as before.
```

### Step 3: Make Player Inherit From Character

Goal:

Move `Player` onto the new hierarchy with minimal behavior changes.

Tasks:

- Change `class Player` to `class Player(Character)`.
- Call the base initializer with the player's starting position.
- Keep player-specific config loading in `Player`.
- Keep existing player components:
  - `PlayerHealth`
  - `PlayerMovement`
  - `PlayerCombatController`
  - `PlayerGrabController`
  - `PlayerAnimationController`
  - `PlayerRenderer`
  - `PlayerStateMachine`
- Replace duplicate geometry/render wrapper methods only if the base class can do it cleanly.
- Run player movement, attack, animation, and collision tests.

Expected result:

```text
Player is a Character.
Input and player-specific behavior remain in Player and player controllers.
```

### Step 4: Make Enemy Inherit From Character

Goal:

Move `Enemy` onto the new hierarchy with minimal behavior changes.

Tasks:

- Change `class Enemy` to `class Enemy(Character)`.
- Call the base initializer with enemy spawn position.
- Keep enemy-specific config loading in `Enemy`.
- Keep existing enemy components:
  - `EnemyHealth`
  - `EnemyMovement`
  - `EnemyCombatController`
  - `EnemyReactionController`
  - `EnemyLifecycleController`
  - `EnemyStateResolver`
  - `EnemyAnimationController`
  - `EnemyRenderer`
- Replace duplicate geometry/render wrapper methods only if the base class can do it cleanly.
- Run enemy attack timing, enemy combat hitbox, collision, and wave-related tests.

Expected result:

```text
Enemy is a Character.
AI and enemy-specific behavior remain in Enemy and enemy controllers.
```

### Step 5: Standardize Shared Character Method Names

Goal:

Make systems interact with player and enemy through the same character-level interface.

Tasks:

- Audit systems that call player/enemy methods directly.
- Standardize common method names:
  - `take_damage(...)`
  - `draw(...)`
  - `get_hurt_rect()`
  - `get_attack_rect()`
  - `get_collision_rect()`
  - `apply_world_bounds(...)`
- Keep player/enemy-specific method signatures only where the gameplay really differs.
- If `take_damage()` signatures differ too much, introduce a shared damage event object later instead of forcing a bad common signature.

Expected result:

```text
Systems can treat Player and Enemy as Character-like objects for geometry, rendering, and basic combat checks.
```

### Step 6: Extract Shared Health And Damage Concepts Carefully

Goal:

Reduce duplication around health and damage without losing player/enemy-specific rules.

Tasks:

- Compare `PlayerHealth` and `EnemyHealth`.
- Extract a shared health value object only if it simplifies both.
- Keep player lives/continues separate from enemy death/removal.
- Consider a shared `DamageRequest` or `HitReaction` object for future consistency.
- Keep existing hit stun, recoil, knockdown, grab, and throw rules readable.

Expected result:

```text
Health and damage concepts are more consistent, but player lives and enemy removal remain separate.
```

### Step 7: Align State Names And State Transitions

Goal:

Make shared states easier to reason about across player and enemy code.

Tasks:

- Compare player string constants with `EnemyState`.
- Introduce a shared `CharacterState` only for states that truly overlap.
- Keep player-only states such as `JUMP_ATTACK`, `GRAB_KNEE`, and `THROW` if they are not useful for enemies.
- Keep enemy-only states such as `PATROL`, `CHASE`, `GRABBED`, `KNOCKDOWN`, and `GETUP` if they are not useful for players yet.
- Update tests after each small state rename.

Expected result:

```text
State naming becomes more consistent without forcing player and enemy into the exact same state machine.
```

### Step 8: Make Enemy Behavior More Data-Driven

Goal:

Make adding enemy types easier.

Tasks:

- Review `enemy_config.py` and `enemy_factory.py`.
- Keep enemy stats, animation keys, attack data, score value, and ranges in config.
- Move archetype-specific behavior toward resolver/controller selection.
- Add an AI or behavior registry only when there are at least two meaningfully different behavior classes.
- Avoid adding many subclasses unless an enemy has truly unique mechanics.

Expected result:

```text
New enemy types can be added mostly through config and selected behavior components.
```

### Step 9: Prepare Player Selection Support

Goal:

Make different playable characters easier to add.

Tasks:

- Review `player_config.py` and `mustapha_player.py`.
- Keep player stats, animations, attack data, jump values, and weapon attacks in config.
- Move character-specific special cases into config or small behavior components.
- Keep `Player` generic enough to represent different selected characters.
- Introduce a player factory if creation logic becomes larger than a few lines.

Expected result:

```text
The game can support multiple playable characters without duplicating the Player class.
```

### Step 10: Clean Up Systems Around The New Hierarchy

Goal:

Let systems depend on stable interfaces instead of concrete player/enemy internals.

Tasks:

- Review `combat_system.py`, `collision_system.py`, `enemy_system.py`, and `gameplay_system.py`.
- Replace direct field access with methods where it improves clarity.
- Keep direct field access for simple stable fields like `x`, `y`, `state`, and `facing_right` if that remains easier to read.
- Make system tests cover the shared `Character` interface.

Expected result:

```text
Systems are easier to test and less coupled to Player or Enemy internals.
```

### Step 11: Migrate Toward The Classic Folder Structure

Goal:

Move files into clearer folders after the class hierarchy is stable.

Tasks:

- Create only the folders that are immediately useful.
- Move combat-specific helpers from `game/entities` into `game/combat`.
- Move config/data modules into `game/data`.
- Move factories into `game/factories`.
- Move long-lived manager classes into `game/managers`.
- Update imports in small groups.
- Run tests after each group of moves.

Expected result:

```text
The folder structure communicates ownership clearly without changing gameplay behavior.
```

## Recommended Order

Start with the lowest-risk foundation:

```text
1. GameObject
2. Character
3. Player inherits Character
4. Enemy inherits Character
5. Standardize shared methods
6. Improve health/damage consistency
7. Align states
8. Improve enemy data-driven behavior
9. Improve player selection support
10. Clean up systems
11. Migrate toward the classic folder structure
```

This order keeps the game playable while gradually improving the architecture.

## What Not To Do

- Do not move every player/enemy field into `Character`.
- Do not merge player and enemy controllers just because the method names look similar.
- Do not create a deep inheritance chain beyond `GameObject -> Character -> Player/Enemy` unless there is a very strong reason.
- Do not replace working components with abstract patterns before duplication is clear.
- Do not remove useful comments while refactoring.
- Do not do a big-bang rewrite.

## Target Shape

The long-term target is:

```python
class GameObject:
    pass


class Character(GameObject):
    pass


class Player(Character):
    pass


class Enemy(Character):
    pass
```

With behavior composed like this:

```text
Character
  geometry
  movement
  combat
  lifecycle
  animation_controller
  renderer

Player
  input_state
  action_controller
  grab
  weapon_slot
  air

Enemy
  state_resolver
  reactions
  flanking
  coordination
  loot_controller
```

This keeps the project production-oriented while staying understandable and milestone-friendly.
