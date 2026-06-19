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

## Current Status

This refactor is implemented.

Current package ownership:

```text
game/entities/     world objects and entity-owned data
game/components/   reusable entity components
game/input/        player input snapshots and input edge state
game/core/         shared infrastructure such as event queues
game/controllers/  per-entity controllers and state controllers
game/combat/       attack data, timing, hit reactions, and hitbox helpers
game/data/         player and enemy config registries
game/factories/    player and enemy construction registries
game/managers/     asset, score, announcement, and stage-clear managers
game/systems/      cross-object gameplay rules
```

The old compatibility wrapper modules for moved combat, data, factory, and manager files have been removed after first-party imports were updated.

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
StateController
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

  input/
    player_input.py
    player_input_state.py
    input_buffer.py

  entities/
    game_object.py
    character.py
    player_state.py
    player.py
    enemy.py
    projectile.py
    weapon.py
    loot.py
    breakable_object.py

  components/
    health.py
    character_state.py
    character_geometry.py
    player_movement.py
    enemy_movement.py
    player_air_state.py
    enemy_flanking.py
    player_renderer.py
    enemy_renderer.py
    enemy_lifecycle_state.py
    player_weapon_slot.py

  controllers/
    player_action_controller.py
    player_animation_controller.py
    player_combat_controller.py
    player_grab_controller.py
    player_lifecycle_controller.py
    player_state_controller.py
    enemy_animation_controller.py
    enemy_combat_controller.py
    enemy_lifecycle_controller.py
    enemy_loot_controller.py
    enemy_reaction_controller.py
    enemy_state_controller.py

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
    player_config.py
    enemy_config.py

  factories/
    player_factory.py
    enemy_factory.py

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

This structure is now mostly implemented. `game/components/` exists and owns reusable or attachable entity parts. `game/input/` owns player input snapshots and edge-state data. `game/core/events.py` owns the shared event queue. `PlayerHealth` and `EnemyHealth` remain under `game/entities/` because player lives and enemy removal still differ. `PlayerStateMachine` also remains under `game/entities/` because it is still player-specific state coordination.

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
EnemyStateController
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

### Completed Migration Notes

The following ownership moves are complete:

```text
game/entities/game_object.py
game/entities/character.py
game/entities/player_state.py
game/core/events.py
game/input/player_input.py
game/input/player_input_state.py
game/input/input_buffer.py
game/controllers/player_action_controller.py
game/controllers/player_animation_controller.py
game/controllers/player_combat_controller.py
game/controllers/player_grab_controller.py
game/controllers/player_lifecycle_controller.py
game/controllers/player_state_controller.py
game/controllers/enemy_animation_controller.py
game/controllers/enemy_combat_controller.py
game/controllers/enemy_lifecycle_controller.py
game/controllers/enemy_loot_controller.py
game/controllers/enemy_reaction_controller.py
game/controllers/enemy_state_controller.py
game/components/health.py
game/components/character_state.py
game/components/character_geometry.py
game/components/movement_math.py
game/components/debug_renderer.py
game/components/player_movement.py
game/components/enemy_movement.py
game/components/player_air_state.py
game/components/enemy_flanking.py
game/components/player_renderer.py
game/components/enemy_renderer.py
game/components/enemy_lifecycle_state.py
game/components/player_weapon_slot.py
game/combat/attack_data.py
game/combat/attack_manager.py
game/combat/combat_geometry.py
game/combat/damage_request.py
game/combat/hit_reaction.py
game/data/player_config.py
game/data/enemy_config.py
game/factories/player_factory.py
game/factories/enemy_factory.py
game/managers/asset_manager.py
game/managers/score_manager.py
game/managers/announcement_manager.py
game/managers/stage_clear_manager.py
```

Do not move files just to make the tree look tidy. Move a file when it clarifies ownership or reduces coupling.

### Entity Construction Order

Keep `Player` and `Enemy` setup grouped in this order:

```text
identity/config data
body and combat tuning
state components
capability components
controllers
presentation components
```

Direct fields such as `movement`, `combat`, `geometry`, `renderer`, and `state_controller` should remain easy to find on the entity. The grouping is for readability during construction, not a reason to hide everything behind a generic component map.

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
enemy.state_controller = EnemyStateController(...)
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

## Completed Component Migration Plan

These steps were completed after the controller, combat, data, factory, and manager folder migrations.

### Step 13: Create The Components Package And Move Shared Character State

Goal:

Create `game/components/` with the smallest safe shared pieces first.

Tasks:

- Create `game/components/__init__.py`.
- Move `character_health.py` to `game/components/health.py`.
- Move `character_state.py` to `game/components/character_state.py`.
- Update `Player`, `Enemy`, `EnemyState`, tests, and any imports.
- Keep `PlayerHealth` and `EnemyHealth` in `entities/` for now because lives and enemy removal still differ.

Expected result:

```text
game/components exists and contains only truly shared character concepts.
```

### Step 14: Move Geometry Components

Goal:

Put reusable hitbox, hurtbox, and frame-rectangle ownership in the component layer.

Tasks:

- Move `player_geometry.py` and `enemy_geometry.py` into `game/components/`.
- Merge them into `CharacterGeometry` when the shared frame, collision, hurtbox, and attack-box behavior is clear.
- Update imports in `Player`, `Enemy`, and geometry/combat tests.
- Review duplicated geometry method names and extract shared helpers only if it reduces code.

Expected result:

```text
Entity classes still expose geometry methods, but the geometry implementation lives under components.
```

### Step 19: Merge Player And Enemy Geometry

Goal:

Use one shared geometry component for both `Player` and `Enemy`.

Tasks:

- Replace `PlayerGeometry` and `EnemyGeometry` with `CharacterGeometry`.
- Keep player jump-attack visual Y behavior as a small hook.
- Keep enemy config-driven hurtbox offsets.
- Update imports and tests.

Expected result:

```text
Player and Enemy both use CharacterGeometry.
```

### Step 20: Fix Player Hurtbox Config Ownership

Goal:

Make player hurtbox dimensions come from config cleanly instead of relying on settings fallbacks.

Tasks:

- Add player hurtbox offsets to `PlayerConfig`.
- Correct `hurt_box_w` to use `PLAYER_HURTBOX_W`.
- Update `CharacterGeometry` to trust owner hurtbox fields for both player and enemy.
- Add or update tests for player hurtbox dimensions.

Expected result:

```text
Player and enemy hurtboxes both come from entity config fields.
```

### Step 21: Evaluate Shared Movement Helpers

Goal:

Reduce duplication between player and enemy movement only where it is obvious.

Tasks:

- Compare facing, bounds, lane, and collision response helpers.
- Extract tiny shared helpers if they reduce repeated math.
- Keep input-driven player movement and AI-driven enemy movement separate.

Expected result:

```text
Shared movement math exists, but player and enemy movement controllers remain separate.
```

### Step 22: Review Renderer Duplication

Goal:

Decide whether `PlayerRenderer` and `EnemyRenderer` should share a base renderer.

Tasks:

- Compare sprite drawing and debug box rendering.
- Extract shared debug drawing only if it reduces duplication.
- Keep player/enemy UI or visual special cases separate.

Expected result:

```text
Combat debug box drawing is shared while sprite and health rendering stay specific.
```

### Step 23: Introduce Shared Damage Request If Needed

Goal:

Normalize damage calls without forcing player and enemy lifecycle rules together.

Tasks:

- Review current `take_damage` signatures.
- Introduce `DamageRequest` only if systems keep needing adapter logic.
- Keep player lives and enemy removal separate.

Expected result:

```text
Damage call sites can pass one request object without merging lifecycle rules.
```

### Step 15: Move Movement And Air/Flanking Components

Goal:

Move movement-related state and behavior out of `entities/` without merging player and enemy movement too early.

Tasks:

- Move `player_movement.py`, `enemy_movement.py`, `player_air_state.py`, and `enemy_flanking.py` into `game/components/`.
- Keep names player/enemy-specific because input-driven movement and AI movement still differ.
- Update imports and targeted movement tests.
- Consider a tiny shared movement helper only for simple bounds or facing math if duplication becomes obvious.

Expected result:

```text
Movement behavior is component-owned, while Player and Enemy remain coordinators.
```

### Step 16: Move Renderer And Lifecycle State Components

Goal:

Move rendering helpers and pure lifecycle state holders into the component layer.

Tasks:

- Move `player_renderer.py` and `enemy_renderer.py` into `game/components/`.
- Move `enemy_lifecycle_state.py` into `game/components/`.
- Keep lifecycle controllers in `game/controllers/` because they actively drive behavior.
- Update imports and render/lifecycle tests.

Expected result:

```text
Render helpers and passive lifecycle data sit under components; behavior controllers stay under controllers.
```

### Step 17: Review Player-Specific Data Components

Goal:

Decide which player-only helpers are reusable components versus entity-local data.

Tasks:

- Review `game/input/player_input_state.py`, `game/core/events.py`, `player_weapon_slot.py`, and `player_state_machine.py`.
- Move `player_weapon_slot.py` into `game/components/` if weapon ownership is expected to be shared later by enemies or pickups.
- Keep player input state under `game/input/`.
- Keep events under `game/core/` once more than one gameplay feature can emit them.
- Move `player_state_machine.py` only if a shared state machine abstraction is introduced.

Expected result:

```text
Only component-shaped files move; player-only coordination details do not move just for tidiness.
```

### Step 18: Remove Compatibility Dust And Update Tests/Docs

Goal:

Finish the component migration cleanly.

Tasks:

- Search for stale imports from old `game/entities/*` component paths.
- Remove empty folders or temporary wrappers if any were created.
- Update `design.md` current status and completed migration notes.
- Run the full test suite.

Expected result:

```text
The component folder is active, imports are clean, and tests pass.
```

## Completed Input/Event/Damage Refinement Plan

These steps were completed after the component and combat request migrations.

### Step 24: Normalize Player Input Ownership

Goal:

Decide whether player input data should stay entity-local or move into an input package.

Tasks:

- Review `player_input.py` and `player_input_state.py`.
- Move them only if an `input/` or `core/events` package becomes clearer than entity ownership.
- Keep action decisions in `PlayerActionController`.

Expected result:

```text
Input snapshots and input edge state live under game/input.
```

### Step 25: Review Player Event Queue

Goal:

Decide whether the player-local event queue should become a broader game event queue.

Tasks:

- Review current event usage, especially projectile spawning.
- Keep events local if only player actions emit through them.
- Move toward a shared event model only when enemies, weapons, or level objects need the same channel.

Expected result:

```text
Player projectile spawning uses the shared GameEventQueue shape.
```

### Step 26: Add Tests Around Real Renderer Debug Boxes

Goal:

Protect the shared debug renderer without requiring a full game window.

Tasks:

- Add small tests with fake rect-owning characters and a pygame surface.
- Verify collision, frame, hurt, and attack boxes draw without errors.

Expected result:

```text
The shared debug renderer has surface-level coverage.
```

### Step 27: Revisit DamageRequest Adoption

Goal:

Use `DamageRequest` more broadly after more combat features land.

Tasks:

- Consider accepting `DamageRequest` directly in `Player.take_damage` and `Enemy.take_damage`.
- Keep legacy-friendly adapters until tests and lightweight fakes are migrated.
- Avoid merging player lives and enemy death/removal behavior.

Expected result:

```text
Player and Enemy can accept DamageRequest directly while old adapters keep working.
```

## Completed State/Input Cleanup Plan

These steps were completed after input, event, and damage ownership were clarified.

### Step 28: Review Player State Machine Ownership

Goal:

Decide whether `PlayerStateMachine` should stay player-specific or become a shared state-machine component.

Tasks:

- Compare player state transitions with enemy state controller needs.
- Keep `PlayerStateMachine` local if enemies do not need the same state object model.
- Extract shared state-machine code only when both sides benefit.

Expected result:

```text
PlayerStateMachine remains entity-local because it is still player-specific.
```

### Step 29: Split Large Gameplay System Imports

Goal:

Reduce wildcard imports in high-level systems after the folder migration has stabilized.

Tasks:

- Review `game/systems/gameplay_system.py`.
- Replace wildcard imports with explicit function imports in small groups.
- Keep update order clear because gameplay sequencing matters.

Expected result:

```text
Gameplay and player-input systems use explicit imports.
```

### Step 30: Add Input Mapping Tests

Goal:

Protect `PlayerInput` key mapping after moving it into `game/input`.

Tasks:

- Add tests for keyboard aliases such as arrows/WASD, attack, jump, grab, fire, and drop.
- Use a small fake key object instead of needing a live pygame event loop.

Expected result:

```text
Player input key mappings are covered by focused tests.
```

## Completed Naming/Import/Event Cleanup Plan

These steps were completed after state, input, and event ownership were clarified.

### Step 31: Review Generic Utility Wildcard Imports

Goal:

Clean up remaining wildcard imports outside the gameplay system path.

Tasks:

- Review wildcard imports from settings/colors where they make modules harder to scan.
- Replace them gradually in touched files only.
- Avoid noisy mechanical churn across the whole project.

Expected result:

```text
Touched render/combat/system modules use explicit imports.
```

### Step 32: Review State Constants And Attack Names

Goal:

Separate shared character state constants from player-only attack-state names.

Tasks:

- Keep `CharacterState` for shared states.
- Decide whether player attack names should become attack IDs instead of state constants.
- Avoid changing gameplay behavior while renaming.

Expected result:

```text
Player-specific state names are grouped under PlayerState while Player keeps readable aliases.
```

### Step 33: Add Event Queue Integration Tests

Goal:

Test the real projectile spawn path through `PlayerWeaponSlot` and `collect_player_projectiles`.

Tasks:

- Use a fake ranged weapon and fake player owner.
- Emit a projectile through weapon firing.
- Verify the projectile system drains the event queue into `game_state.projectiles`.

Expected result:

```text
The player projectile event path is covered from weapon slot to projectile collection.
```

## Completed Input/Data Compatibility Cleanup Plan

These steps were completed after input buffering and data import ownership were reviewed.

### Step 34: Adopt InputBuffer In Player Action Flow

Goal:

Use `InputBuffer` for forgiving attack/jump input timing instead of only edge flags.

Tasks:

- Decide which actions should buffer first, probably attack and jump.
- Keep current behavior until tests define expected buffered timing.
- Add tests around pressing slightly early during attack recovery or landing.

Expected result:

```text
Attack and jump input can be buffered without reintroducing hold-to-auto-combo.
```

### Step 35: Review Data Module Wildcard Imports

Goal:

Clean up broad imports in data-heavy modules when the constant list is stable.

Tasks:

- Review `player_config.py`, `enemy_config.py`, and `attack_data.py`.
- Replace wildcard imports only when it improves readability.
- Avoid a giant mechanical import patch unless tests remain easy to review.

Expected result:

```text
Core attack/player/enemy data modules use explicit imports.
```

### Step 36: Review Compatibility Aliases

Goal:

Remove old aliases only when first-party code and tests no longer need them.

Tasks:

- Review `Entity = GameObject` compatibility.
- Review backward-compatible attack table names in player config.
- Keep aliases that help tests or data validation stay readable.

Expected result:

```text
Unused compatibility aliases are removed; tests use canonical names.
```

## Completed Historical Plan/Input Coverage Cleanup Plan

These steps were completed after input buffering and compatibility cleanup.

### Step 37: Clean Up Historical Plan Text

Goal:

Move the original completed step-by-step plan out of the active planning section or clearly label it historical.

Tasks:

- Keep the useful architecture guidance.
- Avoid making completed steps look like future work.
- Preserve important comments and rationale.

Expected result:

```text
The old step-by-step plan is clearly labeled historical.
```

### Step 38: Add Real Input Buffer Gameplay Tests

Goal:

Cover buffered jump/attack behavior through `Player.update`, not only `PlayerActionController`.

Tasks:

- Use a lightweight player-like fixture or factory-backed player if practical.
- Verify early attack press during recovery starts the next combo.
- Verify jump buffer does not bypass invalid states.

Expected result:

```text
Buffered input is covered through Player.update.
```

### Step 39: Review Remaining Wildcard Imports Opportunistically

Goal:

Continue removing wildcard imports only in modules being actively edited.

Tasks:

- Prioritize `settings` and `colors` imports in gameplay modules.
- Leave data-heavy or generated-style modules alone until touched.
- Keep patches reviewable.

Expected result:

```text
Newly touched entity/data/gameplay modules avoid broad imports where practical.
```

## Remaining Refactoring Steps

These steps are useful next, but they are not required before adding more gameplay.

### Step 40: Review Remaining Entity Field Groups After Gameplay Changes

Goal:

Keep Player and Enemy field ownership readable as new features land.

Tasks:

- Keep construction grouped by config, state/input, capability components, controllers, and presentation.
- Avoid moving stable direct fields into opaque dictionaries.
- Extract a new component only when behavior or state has a clear owner.

### Step 41: Add Real Player/Enemy Construction Smoke Tests

Goal:

Make sure factories or direct constructors keep all required components wired.

Tasks:

- Instantiate real Player/Enemy through factories where possible.
- Assert required components/controllers exist.
- Avoid depending on rendering details beyond construction.

### Step 42: Continue Opportunistic Import Cleanup

Goal:

Clean remaining wildcard imports in files already being touched.

Tasks:

- Prioritize gameplay/runtime modules.
- Leave asset manifest and animation data modules alone unless they become noisy.
- Keep import patches small and test-backed.

## Historical Refactoring Plan

This original step-by-step plan is complete and kept here as historical design rationale. Future work should use the active remaining steps above.

### Step 1: Rename And Clarify The Base Entity

Goal:

Create the intended root type without changing behavior.

Tasks:

- Rename or wrap `game/entities/entity.py` so it provides `GameObject`.
- Keep a temporary `Entity = GameObject` compatibility alias if many imports still use `Entity`. This alias has since been removed after first-party imports were updated.
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
  - `EnemyStateController`
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
  state_controller
  reactions
  flanking
  coordination
  loot_controller
```

This keeps the project production-oriented while staying understandable and milestone-friendly.
