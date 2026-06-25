# 2D Game Architecture Design Patterns and Best Practices

Research and design notes for the Cadillacs and Dinosaurs style PyGame beat 'em up.

This document is not limited to PyGame. It uses PyGame as the target runtime, but borrows proven ideas from Unity, Godot, Unreal, fighting games, beat 'em ups, and general game programming architecture.

## 1. Design Goals

The project should feel production-scale while remaining easy to understand.

Core goals:

- Keep game objects small and readable.
- Share mechanics between players and enemies, but keep decision logic separate.
- Prefer data-driven configuration for characters, enemies, weapons, attacks, animation, waves, and levels.
- Use composition for behavior that changes often.
- Use inheritance only for stable identity and shared contracts.
- Make combat frame-based and box-based: startup, active, recovery, hitboxes, hurtboxes, and hit memory.
- Make movement and animation driven by the same state and timing model.
- Make enemy behavior expandable without rewriting existing enemy classes.
- Make level editing possible later by keeping stage, wave, spawn, bounds, and prop data separate from game logic.

Useful rule:

```text
Entity = identity and shared body
Component = reusable capability
Controller = decision maker for one entity
System = rule applied across many entities
Manager = ownership, lifetime, loading, or orchestration
Data = numbers and authored content
```

## 2. Research Summary

Important external patterns and engine lessons:

- Game Programming Patterns recommends the Component pattern when one object spans many domains such as input, physics, rendering, sound, AI, and combat. It also warns that components add complexity, so use them to solve real coupling, not for everything.
- Godot's architecture is strongly composition-oriented: a game is a tree of scenes, each scene is a tree of nodes, and scenes can be saved, instanced, and reused like custom node types.
- Godot separates variable frame updates from fixed physics updates. `_physics_process()` runs at fixed intervals, defaulting to 60 Hz, and is recommended for stable movement/collision work.
- Unity separates scene objects from reusable data assets. ScriptableObjects let many instances reference one copy of authored data, which maps well to Python dataclasses, JSON, TOML, or module-level config objects.
- Unity's animation state machines model behavior as one active state at a time, with transitions based on conditions or action completion.
- Unreal Behavior Trees use blackboards for AI memory and event-driven updates to avoid checking everything every frame. Conditions are decorators, while leaves are action tasks.
- Unreal Gameplay Ability System separates attributes, abilities, gameplay effects, ability tasks, animation, VFX, and sounds. For this project, the useful lesson is: attack behavior should be represented as data plus execution state, not as ad hoc methods.
- Unreal StateTree combines hierarchical state machines with behavior-tree-style selectors. This is useful for enemies and bosses where simple FSMs become too flat and behavior trees become too open-ended.
- Fighting game and beat 'em up design commonly uses frame data: startup, active, recovery, hitstun, blockstun, cooldown, invulnerability, cancel windows, and per-move hit memory.
- Tiled shows a strong level-editor model for 2D games: tile layers, object layers, custom properties, templates, tile collisions, and map annotations. That maps well to future stage editing.
- Aseprite's sprite-sheet and tag workflow is a practical production model: animation clips should be named ranges of frames, exported with metadata, and kept consistent with engine-side animation IDs.
- MonoGame and Celeste show that successful 2D games can be built on relatively small frameworks when the project has strong game-specific architecture above the framework.
- Interactive fiction and visual novel design show that story choices need consequence, memory, and emotional structure. Branching alone is not enough.

## 2.1 Lessons From Different 2D Game Types

Do not design only for beat 'em ups. A production 2D architecture should borrow patterns from several genres.

### Platformers

Examples: Mario, Sonic, Mega Man, Metroid, Celeste, Hollow Knight.

Useful patterns:

- Movement is the game. Use precise physics, coyote time, jump buffering, variable jump height, wall contact rules, and predictable collision.
- Collision is usually tile-based plus special volumes.
- State machines need to handle ground, air, wall, dash, climb, hurt, death, and cutscene states cleanly.
- Camera design is critical: lookahead, room bounds, vertical dead zones, and transition triggers.
- Level design uses affordances: solid, one-way, hazard, ladder, moving platform, pickup, checkpoint, trigger.

Design takeaway for this project:

- Add input buffering and forgiving timing to attacks the same way platformers use jump buffering.
- Keep camera rules data-driven per stage segment.
- Treat stage objects as authored objects with properties, not hardcoded rectangles.

### Top-Down Action / Adventure

Examples: Zelda, Hyper Light Drifter, Enter the Gungeon, Hotline Miami.

Useful patterns:

- Use intent-based movement, facing, aim direction, interaction volumes, and rooms.
- Combat often uses arcs, projectiles, shields, dodge invulnerability, and enemy telegraphs.
- Object interaction is usually as important as combat: doors, switches, pickups, NPCs, chests.
- Room state matters: cleared, locked, discovered, puzzle solved.

Design takeaway:

- Build a general `InteractionSystem`, not only combat.
- Make trigger volumes and object layers future-ready.
- Separate player facing from movement direction so weapons and grabs can aim independently later.

### Shoot 'Em Ups

Examples: Gradius, R-Type, DoDonPachi, Touhou.

Useful patterns:

- Object pooling is important because bullets/effects are created constantly.
- Hitboxes are intentionally smaller than sprites for fairness.
- Enemy waves are timeline- or pattern-driven.
- Difficulty is tuned through bullet speed, density, pattern complexity, spawn timing, and recovery resources.

Design takeaway:

- Use object pools for hit sparks, floating text, projectiles, shell casings, and short-lived effects.
- Keep projectile movement as data/patterns.
- Make hurtboxes fair and visually readable.

### Fighting Games

Examples: Street Fighter, King of Fighters, Guilty Gear, Smash.

Useful patterns:

- Frame data is the contract.
- Hitboxes, hurtboxes, throw boxes, invulnerability boxes, cancel windows, hitstop, hitstun, and blockstun are explicit.
- Move identity and move runtime state are separate.
- Training/debug tools are part of production, not optional.

Design takeaway:

- Treat each attack like a small ability with authored data.
- Build frame-step debug early.
- Record hit results and attack phase in logs.

### Tactical / Strategy / Tower Defense

Examples: Advance Wars, Into the Breach, Fire Emblem, Mindustry.

Useful patterns:

- Systems are clearer than object scripts: pathfinding, targeting, resource economy, build rules, turn order.
- Data-driven units and abilities are central.
- AI often uses scoring functions: evaluate possible actions and choose the highest utility action.

Design takeaway:

- Enemy AI can use utility scoring for choosing attack/reposition/retreat.
- Stage waves can use budgets and tags instead of fixed enemy lists only.

### Puzzle Games

Examples: Tetris, Sokoban, Baba Is You, puzzle-platformers.

Useful patterns:

- Rules must be deterministic and easy to inspect.
- Level data matters more than character code.
- Undo/restart/debug tools are very valuable.

Design takeaway:

- Keep combat and movement deterministic enough to test.
- Use small reproducible scenarios for tuning: one enemy, one lane, one attack.

### Rhythm Games

Examples: osu!, Rhythm Heaven, Crypt of the NecroDancer.

Useful patterns:

- Timing windows are authored and measured.
- Input latency and feedback are part of design.
- Good debug tools show early/late/perfect timing.

Design takeaway:

- Combos and attacks can benefit from timing windows and input-buffer diagnostics.
- Log input timestamps relative to attack cancel windows.

### RPG / Narrative 2D Games

Examples: Undertale, EarthBound, Stardew Valley, visual novels, interactive fiction.

Useful patterns:

- Data drives dialogue, quests, NPC schedules, flags, inventory, save state, and triggers.
- Story state should be separate from scene code.
- Choices need remembered consequences, not just immediate dialogue changes.

Design takeaway:

- Add a future `StoryState` or `GameFlags` service for stage progression, NPC dialogue, unlocks, and endings.
- Avoid putting story progression directly inside enemy or level classes.

## 2.2 Lessons From Popular and Classic Projects

Use these as architecture references, not as code to copy.

### Celeste

Celeste is a strong example of a 2D game built on a focused framework with game-specific architecture. Public source snippets and the Monocle framework are useful references for entity/component style, scene management, precise platforming feel, and debug-minded development.

Lessons:

- The engine/framework can stay small if game rules are well organized.
- Feel features such as coyote time, input buffering, dash locks, assist options, and camera rules are first-class design systems.
- A small set of core primitives can support many mechanics when they compose well.

### Stardew Valley

Useful as a data-heavy 2D game reference.

Lessons:

- Save data, world state, schedules, items, shops, crops, tools, NPCs, events, and maps need clear data ownership.
- 2D games can become content-heavy very quickly, so naming and folder structure matter.
- Story and economy systems should not be hidden inside rendering or input classes.

### Streets of Rage / Final Fight / Cadillacs and Dinosaurs

Useful beat 'em up references.

Lessons:

- Fake depth, lane control, crowd pressure, pickups, weapon drops, destructible props, and short enemy telegraphs define the genre.
- Difficulty comes more from group composition and screen pressure than one enemy having huge damage.
- Attacks need generous readability because many characters overlap.

### Hollow Knight / Metroid

Useful action exploration references.

Lessons:

- Abilities double as combat tools and traversal keys.
- World state, unlocks, doors, checkpoints, and map regions should be data-driven.
- Bosses need hierarchical states and telegraphs, not just faster normal enemy AI.

### Into the Breach

Useful design reference for fairness and readability.

Lessons:

- Telegraphing enemy intent makes difficult combat feel fair.
- Showing future danger can create strategic depth without increasing control complexity.
- Enemy AI can be predictable by design and still interesting.

### Touhou / Bullet Hell Games

Useful projectile and fairness reference.

Lessons:

- Player hurtbox can be smaller than sprite.
- Bullet patterns should be authored as data and debugged visually.
- Readability depends on consistent colors, sizes, speeds, and layering.

### Tiled-Based Indie Games

Tiled's model is a strong editor target for many 2D games.

Lessons:

- Tile layers should represent visuals and coarse collision.
- Object layers should represent spawns, triggers, doors, camera zones, props, NPCs, pickups, and wave volumes.
- Custom properties are the bridge between editor-authored content and game runtime.

## 2.3 Architecture Patterns Across Engines

### Unity-Style

Useful ideas:

- GameObject plus components.
- Prefabs as reusable authored entity templates.
- ScriptableObjects as reusable data assets.
- Animator Controllers for animation state and transitions.

Python/PyGame equivalent:

```text
Prefab -> factory function + data definition
ScriptableObject -> dataclass/JSON/TOML config
MonoBehaviour component -> Python component with update/draw hooks
Animator Controller -> AnimationController + state mapping data
```

### Godot-Style

Useful ideas:

- Scenes are reusable composed node trees.
- Nodes are small single-responsibility objects.
- Signals decouple event senders from receivers.
- `_physics_process` gives stable fixed-step logic.
- Project organization keeps assets close to scenes/content.

Python/PyGame equivalent:

```text
Scene -> Level/Screen object
Node tree -> entity/component hierarchy
Signal -> event queue
PackedScene -> factory + authored data
Physics process -> fixed update loop
```

### Unreal-Style

Useful ideas:

- Actors own components.
- Gameplay Ability System separates attributes, abilities, effects, and execution tasks.
- Behavior Trees use blackboards and task/decorator/service separation.
- StateTree combines hierarchical states with task execution and transitions.

Python/PyGame equivalent:

```text
Actor -> Entity/GameObject
ActorComponent -> component
GameplayAbility -> AttackData/AbilityData + runtime instance
GameplayEffect -> DamageRequest/status effect
Blackboard -> AI memory object
Behavior Tree Task -> AI action
Decorator -> condition
Service -> periodic evaluator
StateTree -> hierarchical action/AI state machine
```

## 3. Recommended Folder Structure

The current project already has a good direction. The best practice is to keep folders grouped by responsibility, not by "all player files here" and "all enemy files there" only.

Recommended long-term structure:

```text
game/
  animation/
    animation.py
    animation_config.py
    animation_manager.py
    frame_animation.py
    spritesheet.py
    *_data.py

  assets/
    asset_manifest.py
    backgrounds/
    enemy/
    loot/
    objects/
    player/
    props/
    weapon/

  combat/
    attack_data.py
    attack_instance.py
    attack_manager.py
    box_data.py
    combat_geometry.py
    damage_request.py
    hit_reaction.py

  components/
    character_geometry.py
    character_state.py
    health.py
    movement_math.py
    player_movement.py
    enemy_movement.py
    renderer.py
    weapon_slot.py

  controllers/
    player_action_controller.py
    player_combat_controller.py
    player_state_controller.py
    enemy_ai_controller.py
    enemy_combat_controller.py
    enemy_state_controller.py
    enemy_coordination_controller.py

  core/
    events.py
    clock.py
    ids.py
    math2d.py

  data/
    player_config.py
    enemy_config.py
    weapon_config.py
    attack_config.py
    level_config.py
    difficulty_config.py

  entities/
    game_object.py
    character.py
    player.py
    enemy.py
    weapon.py
    projectile.py
    loot.py
    prop.py
    breakable_object.py

  factories/
    player_factory.py
    enemy_factory.py
    weapon_factory.py

  input/
    player_input.py
    player_input_state.py
    input_buffer.py

  level/
    lane.py
    level.py
    prop.py
    stage_config.py
    stage_manager.py
    wave.py

  managers/
    asset_manager.py
    score_manager.py
    announcement_manager.py

  systems/
    arena_system.py
    bounds_system.py
    camera_system.py
    cleanup_system.py
    collision_system.py
    combat_system.py
    enemy_system.py
    gameplay_system.py
    loot_system.py
    projectile_system.py
    wave_system.py

tests/
  test_attack_data_validation.py
  test_combat_system.py
  test_enemy_ai.py
  test_movement.py
  test_animation_state.py
```

Guidelines:

- Keep source under `game/`.
- Keep authored numbers under `game/data/` or dedicated data files.
- Keep generated or raw art under `assets/` or `game/assets/`, but avoid duplicating the same concept forever in both places.
- Keep external reference material under `reference/`.
- Keep design notes under `docs/` or root markdown files. Over time, move stable documents into `docs/`.
- Use `snake_case` file and folder names. This also matches Godot's style recommendation and avoids macOS/Windows case-sensitivity surprises.

## 4. Classes and Inheritance

Best practice: use shallow inheritance for identity, composition for behavior.

Good inheritance:

```python
GameObject
  Character
    Player
    Enemy
  Prop
    BreakableObject
  Pickup
    Loot
    WeaponPickup
  Projectile
```

Avoid deep trees like:

```text
Enemy -> MeleeEnemy -> FastMeleeEnemy -> KnifeFastMeleeEnemy -> RedKnifeFastMeleeEnemy
```

Use data and components instead:

```python
Enemy(
    enemy_id="knife_punk_red",
    stats=EnemyStats(...),
    movement=ChaseMovement(...),
    combat=AttackSet(...),
    ai=AggressiveMeleeAI(...),
    renderer=EnemyRenderer(...),
)
```

Common interfaces:

```python
class GameObject:
    id: int
    x: float
    y: float
    visible: bool
    alive: bool

    def update(self, dt: float, world) -> None: ...
    def draw(self, screen, camera_x: float) -> None: ...
    def get_sort_y(self) -> float: ...
```

```python
class Character(GameObject):
    state: CharacterState
    facing_right: bool
    health: HealthComponent
    movement: MovementComponent
    combat: CombatComponent
    geometry: CharacterGeometry
    animation_controller: AnimationController
    renderer: Renderer

    def request_move(self, move_intent) -> None: ...
    def request_attack(self, attack_id: str) -> bool: ...
    def receive_damage(self, request: DamageRequest) -> None: ...
    def enter_state(self, state_name: str, reason: str = "") -> None: ...
```

```python
class Controller:
    def update(self, character: Character, world, dt: float) -> None: ...
```

```python
class System:
    def update(self, world, dt: float) -> None: ...
```

Important rule:

```text
Character owns mechanics.
Controller chooses intentions.
System resolves shared rules.
```

So a player and enemy can both attack, but the player attack is requested from input while the enemy attack is requested from AI.

## 5. Components Inside Common Classes

Recommended components for `Character`:

### HealthComponent

Owns health, death, invulnerability, armor, and damage gates.

Interface:

```python
class HealthComponent:
    def can_receive_damage(self, character, request) -> bool: ...
    def take_damage(self, character, request) -> DamageResult: ...
    def heal(self, amount: int) -> None: ...
    def update_timers(self, dt: float) -> None: ...
```

### MovementComponent

Owns velocity, acceleration, friction, lane movement, jump arcs, knockback, and world bounds.

Interface:

```python
class MovementComponent:
    def set_intent(self, x: float, y: float) -> None: ...
    def apply_impulse(self, vx: float, vy: float) -> None: ...
    def update(self, character, dt: float, level) -> None: ...
    def apply_world_bounds(self, character, world_width, lane_top, lane_bottom) -> None: ...
```

### CombatComponent

Owns current attack instance, combo state, attack lockout, hit memory, cancel windows, and attack requests.

Interface:

```python
class CombatComponent:
    def can_start_attack(self, character, attack_id: str) -> bool: ...
    def start_attack(self, character, attack_id: str) -> bool: ...
    def update_attack(self, character, dt: float) -> None: ...
    def get_active_hitboxes(self, character) -> list: ...
    def notify_hit(self, target_id: int) -> None: ...
```

### CharacterGeometry

Owns frame rect, collision/base rect, hurtboxes, attack hitboxes, grab boxes, and debug boxes.

Interface:

```python
class CharacterGeometry:
    def get_frame_rect(self, character) -> pygame.Rect: ...
    def get_collision_rect(self, character) -> pygame.Rect: ...
    def get_hurtboxes(self, character) -> list[pygame.Rect]: ...
    def get_attack_hitboxes(self, character) -> list[pygame.Rect]: ...
```

### AnimationController

Owns current clip, frame index, elapsed time, animation events, locks, and animation-to-state mapping.

Interface:

```python
class AnimationController:
    def play(self, animation_id: str, restart: bool = False) -> None: ...
    def update(self, dt: float) -> list[AnimationEvent]: ...
    def get_frame(self) -> AnimationFrame: ...
    def is_finished(self) -> bool: ...
```

### Renderer

Owns sprite drawing, camera offset, flipping, debug overlay, shadows, and render sorting.

Interface:

```python
class Renderer:
    def draw(self, character, screen, camera_x: float) -> None: ...
    def draw_debug(self, character, screen, camera_x: float) -> None: ...
```

## 6. Data-Driven Design

Use authored data for numbers that designers will tune.

Python options:

- `dataclass` objects for typed in-code config.
- JSON/TOML/YAML for future editor-friendly content.
- Python modules for quick iteration while the project is still moving fast.

Recommended attack data:

```python
@dataclass(frozen=True)
class AttackData:
    attack_id: str
    animation_id: str
    startup_frames: int
    active_frames: tuple[int, int]
    recovery_frames: int
    damage: int
    hitstun_frames: int
    knockback_x: float
    knockback_y: float
    cancel_windows: tuple[CancelWindow, ...]
    hitboxes: tuple[HitboxFrameData, ...]
    stamina_cost: int = 0
    cooldown_frames: int = 0
```

Recommended enemy data:

```python
@dataclass(frozen=True)
class EnemyDefinition:
    enemy_id: str
    display_name: str
    stats: CharacterStats
    movement_profile: str
    attack_set_id: str
    ai_profile_id: str
    animation_set_id: str
    score_value: int
    loot_table_id: str | None
```

Why this matters:

- Designers can tune numbers without touching logic.
- Tests can validate invalid values.
- New enemies and weapons become content work, not architecture work.
- Future level editor can save and load these definitions.

## 7. Movement System

Beat 'em up movement is not pure platformer movement. Characters move in a 2D screen plane with fake depth.

Use world coordinates:

```text
world_x = horizontal stage position
world_y = floor/depth lane position
z       = vertical jump height above floor
```

Screen projection:

```text
screen_x = world_x - camera_x
screen_y = world_y - z
```

Sorting:

```text
Draw lower world_y later, so characters closer to camera appear in front.
```

Movement rules:

- Use fixed-step simulation for movement, collision, combat timing, and AI decisions.
- Use `dt` but design authored frame data around 60 FPS.
- Keep a stable collision/base rect anchored at the feet.
- Keep animation sprite size separate from movement collision.
- Support lock states: attacking may allow no movement, reduced movement, root motion, or authored lunge movement.
- Apply acceleration and friction for responsive feel, unless arcade movement requires instant velocity.
- Separate player input intent from actual velocity.
- Separate knockback velocity from voluntary movement velocity.

Recommended movement update order:

```text
1. Read controller intent.
2. State machine decides whether movement is allowed.
3. Movement component computes desired velocity.
4. Apply attack root motion, jump z velocity, or knockback.
5. Move on x/y.
6. Resolve bounds, lanes, obstacles, and entity push.
7. Update facing if allowed.
```

Movement interface:

```python
@dataclass
class MoveIntent:
    x: float
    y: float
    wants_run: bool = False
    wants_jump: bool = False
```

```python
class MovementProfile:
    walk_speed: float
    run_speed: float
    acceleration: float
    friction: float
    lane_speed_scale: float
    knockback_resistance: float
```

Best practice for fairness:

- Player walking speed should be slightly faster than common enemies.
- Fast enemies can outrun the player but should have lower health or weaker attacks.
- Large enemies can have armor and range, but slower startup and recovery.
- Enemy movement should use intent delays and decision intervals so it does not feel frame-perfect.

## 8. Combat System

Combat should be a pipeline, not scattered distance checks.

Recommended flow:

```text
Controller requests attack.
Character combat component checks if attack can start.
Character enters attack state.
Animation and attack timer advance.
Active frames expose attack hitboxes.
CombatSystem checks attack hitboxes against target hurtboxes.
DamageRequest is created.
Target Health/Reaction applies damage, stun, knockback, invulnerability.
Attack instance records already-hit target IDs.
Character enters recovery, cancel, combo, or neutral state.
```

Core combat objects:

```python
class AttackInstance:
    attack_data: AttackData
    owner_id: int
    frame_index: int
    elapsed_frames: int
    hit_targets: set[int]
    phase: AttackPhase

    def update(self) -> None: ...
    def is_active(self) -> bool: ...
    def can_hit(self, target_id: int) -> bool: ...
    def mark_hit(self, target_id: int) -> None: ...
```

```python
class DamageRequest:
    source_id: int
    target_id: int
    attack_id: str
    damage: int
    hitstun_frames: int
    knockback_x: float
    knockback_y: float
    hitstop_frames: int
    reaction: str
```

CombatSystem responsibilities:

- Build active attack hitboxes from attackers.
- Build hurtboxes from valid targets.
- Ignore same team/faction unless friendly fire is enabled.
- Ignore dead, invulnerable, grabbed, or untargetable targets.
- Prevent repeated hits using `AttackInstance.hit_targets`.
- Resolve hit priority, clashes, armor, grabs, projectiles, and counter-hits.
- Emit events: `AttackHit`, `DamageApplied`, `CharacterDefeated`, `HitstopStarted`.

Important best practices:

- Never use sprite rect as combat rect.
- Never use center-distance as the final hit test for melee attacks.
- Allow multiple hurtboxes when sprites pose dramatically.
- Attack hitboxes should appear only during active frames.
- Store all timing in frames and convert to seconds only for display/debugging.
- Add debug overlay for base rect, hurtbox, hitbox, grab box, and attack phase.

## 9. Attack Combo System

Combo design should be explicit, not a growing pile of `if attack_count == 2`.

Recommended data:

```python
@dataclass(frozen=True)
class ComboStep:
    attack_id: str
    next_attack_id: str | None
    input_window_start: int
    input_window_end: int
    cancel_on_hit_only: bool = False
```

```python
@dataclass(frozen=True)
class ComboDefinition:
    combo_id: str
    steps: tuple[ComboStep, ...]
    reset_frames: int
```

Runtime state:

```python
class ComboState:
    combo_id: str | None
    step_index: int
    buffered_attack: str | None
    reset_timer: int

    def buffer_input(self, input_id: str) -> None: ...
    def consume_next_attack(self, current_frame: int, did_hit: bool) -> str | None: ...
    def reset(self) -> None: ...
```

Combo concepts:

- Input buffer: player presses attack slightly early; game stores it for a few frames.
- Cancel window: current attack can transition to next attack during certain frames.
- Hit confirm: some cancels only work if current attack hit.
- Whiff recovery: missed attacks should usually be more punishable.
- Chain combo: fixed attack sequence, common for beat 'em ups.
- Branch combo: different next attacks based on direction, weapon, grab state, or air state.

Recommended player combo flow:

```text
Attack 1 startup -> active -> recovery
During cancel window, if attack input buffered:
  if hit-confirm rule passes:
    transition to Attack 2
  else:
    finish recovery
```

Enemy combos:

- Use shorter combo chains than players.
- Add cooldown and decision delay after combo ends.
- Let elites/bosses cancel on hit, but normal enemies should commit more often.

## 10. Enemy AI and Coordination

Use three layers:

```text
Enemy AI Controller = one enemy's decisions.
Enemy Coordination = group-level slots, spacing, surround behavior.
Enemy System = updates all enemies and applies global rules.
```

For normal enemies, a finite state machine is enough:

```text
Spawn -> EnterArena -> ChoosePosition -> Approach -> Telegraph -> Attack -> Recover -> Reposition
                                      -> HitStun -> Knockdown -> GetUp
                                      -> Dead
```

For advanced enemies and bosses, use a hierarchical state machine or behavior-tree-inspired model:

```text
Root
  Disabled
  Combat
    Recovering
    Defensive
    Offensive
      Approach
      Strafe
      Attack
      Combo
    Special
```

AI blackboard/memory:

```python
class EnemyBlackboard:
    target_id: int | None
    distance_x: float
    distance_y: float
    has_line_of_attack: bool
    assigned_slot: str | None
    last_attack_time: float
    recently_hit: bool
    aggression: float
```

Decision best practices:

- Do not let every enemy attack at once.
- Use attack slots around the player: front, back, upper lane, lower lane.
- Use cooldowns at both enemy and group level.
- Use weighted choices, not pure randomness.
- Add reaction delay so enemies feel readable.
- Use telegraph states for dangerous attacks.
- Let enemies reposition after attacks instead of standing inside the player.
- Use difficulty profiles to alter aggression, cooldown, allowed simultaneous attackers, health, and damage.

Coordinate system for AI:

```text
dx = target.world_x - enemy.world_x
dy = target.world_y - enemy.world_y
same_lane = abs(dy) <= lane_attack_tolerance
in_x_range = min_range <= abs(dx) <= max_range
can_attack = same_lane and in_x_range and attack_slot_available
```

For fake depth games, `dy` matters as much as `dx`. An enemy should not punch when x is close but the player is clearly in another lane.

## 11. State Control Systems

Use a state machine for character action state, but keep it focused.

Recommended character states:

```text
idle
walk
run
jump_start
jump_air
jump_land
attack
grab
throw
hitstun
knockdown
getup
dead
```

State interface:

```python
class CharacterState:
    name: str

    def can_enter(self, character, context) -> bool: ...
    def enter(self, character, context) -> None: ...
    def update(self, character, dt: float) -> None: ...
    def exit(self, character, context) -> None: ...
    def allows_movement(self, character) -> bool: ...
    def allows_facing_change(self, character) -> bool: ...
    def allows_attack(self, character) -> bool: ...
```

Transition best practices:

- Centralize transition rules.
- Do not let animation code directly mutate game state except through explicit animation events.
- Give high-priority reactions clear overrides: death, hitstun, knockdown, grab.
- Record transition reasons for debugging.
- Keep state names stable because animation, tests, AI, and debug UI will reference them.

Priority model:

```text
dead > grabbed > knockdown > hitstun > attack > jump > run/walk > idle
```

For enemies, combine action state with AI state:

```text
Action state: attacking, hitstun, walking, dead.
AI state: approach, flank, wait, attack_decision, retreat.
```

Do not merge them into one giant enum. An enemy can be in action state `walk` while AI state is `flank`.

## 12. Animation System Matching Movement

Animation should visualize state; state should not be guessed from animation names.

Best practices:

- Anchor all frames at the feet/ground pivot.
- Store per-frame sprite offsets.
- Keep visual frame, collision rect, hurtboxes, and hitboxes separate.
- Use animation events for important timing: active hitbox start, active hitbox end, footstep, landing, throw release, projectile spawn.
- Let attack data own combat timing. Animation should match it, not secretly define it in scattered frame checks.
- Use speed-based animation for locomotion and frame-based animation for attacks/reactions.
- Use fixed frame indices for attack gameplay timing so balance remains stable.

Recommended animation data:

```python
@dataclass(frozen=True)
class AnimationFrame:
    image_id: str
    duration_frames: int
    offset_x: int
    offset_y: int
    hurtboxes: tuple[BoxData, ...] = ()
    events: tuple[AnimationEvent, ...] = ()
```

```python
@dataclass(frozen=True)
class AnimationClip:
    animation_id: str
    frames: tuple[AnimationFrame, ...]
    loop: bool
    movement_tag: str | None = None
```

Matching movement and animation:

- Idle/walk/run animation chosen from movement state and speed.
- Facing direction chosen by controller or target lock rules.
- Attack animation chosen by attack data.
- Jump animation chosen by `z` velocity and landing state.
- Hit animation chosen by reaction type.
- Root motion should be authored in attack data or movement events, not hidden in sprite offsets.

Render order:

```text
background far
background mid
props behind characters
characters sorted by world_y
foreground props
effects sorted by owner/world_y
HUD
debug overlay
```

## 12.1 Animation Production Design

Animation design has two sides:

```text
Art production = how frames are drawn, named, exported, reviewed.
Runtime animation = how frames are selected, timed, events fired, and matched to gameplay.
```

Recommended production pipeline:

```text
1. Concept pose sheet.
2. Gameplay animation list.
3. Rough key poses.
4. Timing pass in frames.
5. Hitbox/hurtbox planning pass.
6. Cleanup pass.
7. Export sprite sheet plus metadata.
8. Import to runtime animation data.
9. Verify in debug viewer.
10. Tune gameplay timing against animation.
```

Recommended animation folders:

```text
assets/player/mustapha/source/
assets/player/mustapha/export/
assets/player/mustapha/preview/
assets/enemies/ferris/source/
assets/enemies/ferris/export/
game/animation/mustapha_data.py
game/animation/ferris_data.py
```

Recommended animation naming:

```text
character_action_variant_direction

mustapha_idle
mustapha_walk
mustapha_run
mustapha_attack_light_1
mustapha_attack_light_2
mustapha_attack_heavy
mustapha_jump_start
mustapha_jump_air
mustapha_jump_land
mustapha_hit_light
mustapha_knockdown
mustapha_getup
mustapha_dead
```

Clip metadata should include:

```text
animation_id
source_file
sprite_sheet
frame_count
frame_durations
loop
root_pivot
frame_offsets
tags
events
recommended_state
debug_notes
```

Aseprite-style tags are useful even if the runtime is not Aseprite-based:

```text
idle: frames 0-5, loop
walk: frames 6-13, loop
punch_1: frames 14-22, once
hit: frames 23-28, once
```

Runtime importer should convert tags into `AnimationClip` definitions. This avoids hardcoding frame ranges in Python.

Animation quality checklist:

- Clear silhouette in every important pose.
- Strong anticipation before heavy moves.
- Contact frame matches active hitbox.
- Recovery pose communicates vulnerability.
- Feet stay anchored unless the move has authored root motion.
- Looping animations have matching first/last pose.
- Different states are visually readable at gameplay zoom.
- Enemy dangerous attacks use stronger anticipation than normal attacks.
- Hit reactions communicate direction and severity.
- Death/knockdown animations end in stable collision state.

Timing guidelines:

```text
Idle:
  low-frequency motion; do not distract.

Walk:
  foot contact should match movement speed.

Run:
  faster cycle and stronger body lean.

Light attack:
  short anticipation, clear contact, modest recovery.

Heavy attack:
  longer anticipation, bigger smear/extension, longer recovery.

Hit reaction:
  immediate readable impact; do not overlong for common hits.

Boss attack:
  unique telegraph, distinct color/sound/effect if dangerous.
```

Animation and movement synchronization:

- For walk/run, choose animation speed from actual velocity.
- For attacks, choose movement from attack data, not from visual frame offset.
- For jumps, drive animation from `z_velocity`: rising, apex, falling, landing.
- For knockback, movement component owns displacement while animation shows reaction.
- For grabs/throws, use paired animation events: grab lock, hold loop, release frame.

Debug viewer requirements:

- Play any animation by ID.
- Step frame-by-frame.
- Show pivot, frame rect, base rect, hurtboxes, hitboxes, and event markers.
- Show frame duration and total clip length.
- Toggle facing direction.
- Compare sprite against target logical body size.

## 12.2 Storyline and Narrative Design

Story design should support gameplay instead of sitting beside it.

For an arcade beat 'em up or action game, story can be light, but it still needs structure:

```text
Who is the player?
What do they want?
Who or what blocks them?
Why does each stage exist?
What changes after each stage?
What does the player learn before the finale?
```

Recommended story architecture:

```python
class StoryState:
    flags: dict[str, bool]
    counters: dict[str, int]
    chapter_id: str
    completed_stages: set[str]
    unlocked_characters: set[str]

    def set_flag(self, flag_id: str) -> None: ...
    def has_flag(self, flag_id: str) -> bool: ...
```

Story content should be data:

```text
game/data/story/
  chapters.json
  dialogue.json
  stage_events.json
  character_bios.json
```

Simple story structure:

```text
Act 1: Setup
  Introduce hero, threat, city/world, first enemy faction.

Act 2: Escalation
  New enemy types, bigger arenas, rival character, first major setback.

Act 3: Revelation
  Explain villain plan, reveal dinosaur/technology/environment stakes.

Act 4: Finale
  Boss gauntlet, final choice/reveal, ending and unlocks.
```

Stage story template:

```text
stage_id
location_name
visual_theme
gameplay_theme
opening_text
mid_stage_event
boss_intro
stage_clear_text
new_enemy_or_mechanic
story_flag_set_on_clear
```

Example:

```text
stage_id: episode_1_rooftop
location_name: Market Rooftops
gameplay_theme: basic melee enemies, barrels, lane pressure
story_goal: chase raiders who stole supplies
mid_stage_event: bridge collapses, forcing alley route
boss_intro: Ferris blocks the elevator
stage_clear_flag: ferris_defeated
```

Branching story guidelines:

- Use branches for meaningful consequences, not random flavor only.
- Prefer branch-and-rejoin for production control.
- Track consequences with flags.
- Let choices affect later dialogue, enemy composition, item rewards, ally help, or endings.
- Avoid too many branches that multiply content beyond what the team can finish.

Choice types:

```text
Tactical choice:
  which route, which ally, which weapon, which risk.

Moral choice:
  save person A or recover item B.

Character choice:
  respond with mercy, anger, humor, suspicion.

Progression choice:
  unlock character, upgrade, shortcut, secret.
```

Environmental storytelling:

- Background props should show what happened before the player arrived.
- Enemy placement should tell who controls an area.
- Destroyed objects, signs, posters, vehicle wrecks, fossils, lab gear, or barricades can carry story without dialogue.
- Reuse stage art intentionally: before/after versions make world changes visible.

Character design:

```text
Playable character:
  fantasy, silhouette, gameplay role, flaw, motivation, relationship to story.

Enemy:
  faction, combat role, readable silhouette, personality, attack tell.

Boss:
  narrative role, mechanic theme, escalation pattern, defeat consequence.
```

Dialogue guidelines:

- Keep combat-stage dialogue short.
- Use one or two lines before fights, not long cutscenes during action.
- Give bosses memorable intros.
- Let playable characters have different short reactions to the same event.
- Store dialogue by event ID and speaker ID so localization is possible later.

Narrative systems to keep separate from combat:

```text
StoryState
DialogueSystem
CutsceneSystem
StageEventSystem
SaveSystem
UnlockSystem
```

The story should be testable:

```text
stage clear sets expected flag
choice sets expected flag
flag unlocks expected dialogue
completed chapter unlocks expected stage
save/load preserves story state
```

## 13. Game Parameters and Balance

Balance is not only numbers. It is readability, fairness, pacing, enemy composition, animation timing, and recovery windows.

Important parameter groups:

```text
Character:
  max_health, walk_speed, run_speed, acceleration, friction, jump_velocity

Attack:
  startup, active, recovery, damage, range, hitstun, knockback, cooldown, cancel window

Defense:
  invulnerability, armor, knockback resistance, getup time, stun resistance

Enemy AI:
  reaction_time, aggression, attack_cooldown, preferred_range, flank_distance

Group AI:
  max_attackers, attack_slot_cooldown, spawn_budget, wave pressure

Difficulty:
  enemy_health_scale, enemy_damage_scale, enemy_aggression_scale, item_drop_rate
```

Fairness rules:

- Strong attacks need slower startup, shorter active windows, longer recovery, or more risk.
- Long-range attacks need narrower lane tolerance or higher recovery.
- Fast attacks should do less damage or less stun.
- Enemies should telegraph high-damage moves.
- Normal enemies should rarely interrupt player recovery with unavoidable hits.
- Player should usually understand why they were hit.
- Avoid enemies attacking from offscreen unless explicitly designed as a warning/projectile pattern.
- Difficulty should increase by composition and behavior before raw damage scaling.

Suggested baseline for 60 FPS:

```text
Player light attack:
  startup: 4-7 frames
  active: 2-4 frames
  recovery: 8-14 frames
  damage: 8-14
  hitstun: 12-20 frames

Player heavy attack:
  startup: 10-18 frames
  active: 3-6 frames
  recovery: 18-30 frames
  damage: 20-35
  hitstun: 20-35 frames

Normal enemy attack:
  startup: 16-28 frames
  active: 3-5 frames
  recovery: 24-40 frames
  damage: 6-12

Fast enemy attack:
  startup: 10-18 frames
  active: 2-4 frames
  recovery: 20-32 frames
  damage: 4-9

Heavy enemy attack:
  startup: 30-50 frames
  active: 4-8 frames
  recovery: 40-70 frames
  damage: 18-35
```

Balance process:

1. Pick one baseline player.
2. Pick one baseline enemy.
3. Tune movement until spacing feels good.
4. Tune one light attack until it feels fair.
5. Tune enemy reaction and attack windows.
6. Add combo step 2 and 3.
7. Add enemy variety by changing one axis at a time: speed, health, range, damage, AI aggression.
8. Add wave composition and group coordination.
9. Playtest with debug overlay and log frame data.
10. Only then tune difficulty multipliers.

Metrics to log:

```text
time_to_kill_enemy
time_to_kill_player
player_damage_taken_per_wave
enemy_hit_rate
player_hit_rate
average_enemies_attacking_at_once
deaths_by_enemy_type
item_drop_usage
combo_completion_rate
```

Dynamic difficulty should be subtle:

- Prefer spawn pacing, item drops, and enemy aggression changes.
- Avoid obvious enemy damage cheating.
- Do not punish a skilled player by making every enemy unfairly fast.
- Do not reward intentional bad play too obviously.

## 14. Event Queue and Game Loop

Recommended fixed update flow:

```text
while running:
  real_dt = clock.tick()
  accumulator += real_dt

  handle_pygame_events()
  input_system.capture()

  while accumulator >= fixed_dt:
    player_input_system.update(fixed_dt)
    enemy_system.update_ai(fixed_dt)
    state_system.update(fixed_dt)
    movement_system.update(fixed_dt)
    bounds_system.update(fixed_dt)
    collision_system.update(fixed_dt)
    combat_system.update(fixed_dt)
    projectile_system.update(fixed_dt)
    effect_system.update(fixed_dt)
    cleanup_system.update(fixed_dt)
    accumulator -= fixed_dt

  animation_system.update(render_dt_or_fixed_dt)
  camera_system.update()
  render()
```

Use an event queue for decoupling:

```python
events.emit(AttackStarted(owner_id, attack_id))
events.emit(AttackHit(source_id, target_id, attack_id))
events.emit(DamageApplied(target_id, amount))
events.emit(CharacterDefeated(target_id))
```

Good event uses:

- Hit spark spawn.
- Sound effects.
- Score changes.
- Camera shake.
- Announcements.
- Enemy death loot drop.

Avoid events for:

- Core state that must be deterministic and immediate.
- Combat hit validity.
- Movement collision resolution.

## 15. Production Guidelines

Coding guidelines:

- Keep comments that explain game-design intent.
- Rename unclear variables when refactoring improves readability.
- Avoid big functions that mix input, movement, combat, animation, and rendering.
- Keep update order explicit.
- Use tests for attack data validation, state transitions, hurtbox/hitbox geometry, combo windows, and enemy AI decisions.
- Add debug draw modes early.
- Make data validation fail loudly when an attack has impossible timing.

Data validation examples:

```text
startup >= 0
active_start <= active_end
recovery >= 0
damage >= 0
hitbox frames must be inside active frames
combo cancel windows must be inside startup/active/recovery duration
animation total frames should match or exceed attack total frames
enemy attack range should match hitbox reach
```

Debug tools to build:

- Toggle hitbox/hurtbox/base rect overlay.
- Show current state and animation frame above character.
- Show current attack phase and frame.
- Show AI state and assigned attack slot.
- Pause and step one frame at a time.
- Slow motion mode.
- Spawn test enemy.
- Reload attack/enemy data without restarting if possible.

## 16. Recommended Architecture for This Project

Given the current codebase, the best direction is incremental refinement, not a rewrite.

Near-term target:

```text
Character:
  thin owner of shared components

Player/Enemy:
  identity plus player/enemy-specific fields

Controllers:
  convert input or AI decisions into requests

Combat:
  attack data, attack instance, damage request, hit reaction

Systems:
  resolve many-object rules

Data:
  expand player/enemy/attack definitions
```

Practical next milestones:

1. Make all attacks data-driven through `AttackData`.
2. Introduce or formalize `AttackInstance` for runtime attack state and hit memory.
3. Replace single generic hitbox functions with per-attack/per-frame hitbox data.
4. Add combo data and input buffering.
5. Split enemy AI into blackboard, decision state, and coordination slots.
6. Add data validation tests for attacks, animations, enemies, and weapons.
7. Add debug overlay for state, attack phase, hitboxes, and AI state.

## 17. Source References

- [Game Programming Patterns: Component](https://gameprogrammingpatterns.com/component.html)
- [Game Programming Patterns: State](https://gameprogrammingpatterns.com/state.html)
- [Game Programming Patterns: Game Loop](https://gameprogrammingpatterns.com/game-loop.html)
- [Game Programming Patterns: Update Method](https://gameprogrammingpatterns.com/update-method.html)
- [Game Programming Patterns: Event Queue](https://gameprogrammingpatterns.com/event-queue.html)
- [Game Programming Patterns: Spatial Partition](https://gameprogrammingpatterns.com/spatial-partition.html)
- [Godot: Nodes and Scenes](https://docs.godotengine.org/en/stable/getting_started/step_by_step/nodes_and_scenes.html)
- [Godot: Idle and Physics Processing](https://docs.godotengine.org/en/stable/tutorials/scripting/idle_and_physics_processing.html)
- [Godot: AnimationTree](https://docs.godotengine.org/en/stable/tutorials/animation/animation_tree.html)
- [Godot: Project Organization](https://docs.godotengine.org/en/stable/tutorials/best_practices/project_organization.html)
- [Unity: ScriptableObject](https://docs.unity3d.com/Manual/class-ScriptableObject.html)
- [Unity: Animation State Machine Basics](https://docs.unity3d.com/Manual/StateMachineBasics.html)
- [Unity: Event Function Execution Order](https://docs.unity3d.com/Manual/execution-order.html)
- [Unreal Engine: Behavior Tree Overview](https://dev.epicgames.com/documentation/en-us/unreal-engine/behavior-tree-in-unreal-engine---overview)
- [Unreal Engine: Gameplay Ability System](https://dev.epicgames.com/documentation/en-us/unreal-engine/gameplay-ability-system-for-unreal-engine)
- [Unreal Engine: StateTree Overview](https://dev.epicgames.com/documentation/en-us/unreal-engine/overview-of-state-tree-in-unreal-engine)
- [Tiled: Introduction](https://doc.mapeditor.org/en/stable/manual/introduction/)
- [Tiled: Custom Properties](https://doc.mapeditor.org/en/stable/manual/custom-properties/)
- [Aseprite: Sprite Sheets](https://www.aseprite.org/docs/sprite-sheet/)
- [Aseprite: Tags](https://www.aseprite.org/docs/tags/)
- [Celeste public source snippets](https://github.com/NoelFB/Celeste)
- [MonoGame repository](https://github.com/MonoGame/MonoGame)
- [osu! repository](https://github.com/ppy/osu)
- [Mindustry repository](https://github.com/Anuken/Mindustry)
- [Game balance overview](https://en.wikipedia.org/wiki/Game_balance)
- [Dynamic game difficulty balancing overview](https://en.wikipedia.org/wiki/Dynamic_game_difficulty_balancing)
- [Interactive fiction and choice-based story context](https://www.theguardian.com/games/article/2024/jun/16/interactive-fiction-game-apps)
- [Branching narrative history example: Consider the Consequences](https://en.wikipedia.org/wiki/Consider_the_Consequences%21)
- [Narrative graph generation research: GENEVA](https://arxiv.org/abs/2311.09213)
