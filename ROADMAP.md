# ROADMAP.md

## Phase 1 - Core Combat Foundation

Status: Complete

### Milestone 1-20

* Basic game loop
* Camera
* Player movement
* Enemy movement
* Collision
* Animation framework
* Stage scrolling

Completed

---

## Phase 2 - Playable Beat-em-up

Status: Complete

### Milestone 21-35

* Combo attacks
* Weapon system
* Grab system
* Throw system
* Enemy states
* Wave progression
* Boss framework

Completed

---

## Phase 3 - Architecture Refactor

Status: Complete

### Milestone 36-43

* GameState architecture
* System extraction
* Main loop cleanup
* Arena system
* Gameplay system
* Combat system separation

Completed

---

## Phase 4 - Combat Expansion

Status: Partially Complete / Deferred

### Milestone 44

Asset Manager

Status: Complete

### Milestone 45

Grab Combo + Knee Attack

Status: Complete

### Milestone 46

Escape Move

Status: Deferred

Reason:

Player state machine and stage progression work have higher priority before adding another action state.

### Milestone 47

Weapon Throw

Status: Planned

Goals

* Throw held weapon
* Weapon projectile physics
* Weapon damage on impact
* Weapon drop after throw

### Milestone 48

Recovery Roll

Status: Planned

Goals

* Quick recovery from knockdown
* Temporary invulnerability
* Player skill expression

---

## Phase 5 - Episode 1 Stage System

Status: In Progress

### Milestone 49

Generated Episode 1 Stage Backgrounds

Status: Complete

Goals

* Create Episode 1 rooftop, hallway, transition, and arena backgrounds
* Keep 1080px height
* Use dynamic stage widths based on source-image ratios where useful
* Keep style consistent across all four stages

Current Decision

* Playable and transition backgrounds should be at least `SCREEN_WIDTH` wide.
* Avoid narrow backgrounds in runtime.
* Expand/regenerate narrow sources instead of adding special rendering logic.

### Milestone 50

Stage Config Foundation

Status: Complete

Goals

* Add `stage_config.py`
* Store stage id, name, background, size, player start, lanes, completion, and exit data
* Make `Level` load from stage data
* Make camera clamp against current stage width

### Milestone 51

StageManager + Stage Loading

Status: Complete

Goals

* Add `StageManager`
* Add `load_stage()` runtime reset
* Clear stage runtime lists on transition
* Preserve player, score, lives, and broader game state
* Advance to next stage after stage clear

### Milestone 52

Stage Content Config

Status: Complete

Goals

* Move waves into stage data
* Move weapons into stage data
* Move breakable objects/barrels into stage data
* Keep `Level` responsible for converting stage wave data into runtime wave objects

### Milestone 53

Exit Rects

Status: Complete

Goals

* Replace hardcoded right-edge completion with `exit_rect`
* Use player feet/collision rect to enter exits
* Support transition stages with no waves
* Support combat stages that require all waves complete before exit

### Milestone 54

Walkable Areas

Status: Complete / Tuning Needed

Goals

* Add `walkable_polygon` per stage
* Keep `lane_top/lane_bottom` as simple fallback and spawn guidance
* Use player/enemy feet/collision rect for walkable tests
* Add debug polygon drawing

Tuning Needed

* Rooftop angled floor
* Arena combat floor
* Hallway carpet/floor band
* Transition sidewalk once the background is expanded

---

## Phase 6 - Stage Polish

Status: Next

### Milestone 55

Episode 1 Content Tuning

Goals

* Tune enemy waves per stage
* Tune weapon placement per stage
* Tune breakable object placement per stage
* Tune exit rectangles
* Tune walkable polygons
* Confirm arena locks feel good with the new backgrounds

### Milestone 56

Stage 3 Full-Width Transition

Goals

* Regenerate or expand Stage 3 to at least `1920 x 1080`
* Keep runtime rendering simple
* Avoid narrow-stage camera/draw special cases

### Milestone 57

Stage Presentation

Goals

* Stage intro title
* Stage clear presentation
* Episode clear presentation
* Optional transition fade

### Milestone 58

EpisodeManager

Goals

* Add multiple episodes
* Each episode owns ordered stages
* Advance from final stage of one episode to next episode
* Prepare for future save/unlock support

---

## Phase 7 - Combat Polish

Planned

### Combat Timing

* Windup frames
* Active frames
* Recovery frames

### Hitbox Refactor

* Separate body box
* Separate collision box
* Separate hurtbox
* Weapon-specific attack boxes

### Visual Improvements

* Larger attack frames
* Attack offsets
* Better animation alignment

### Effects

* Hit sparks
* Camera shake
* Impact effects
* Screen flash

### Enemy Animation Loading Refactor

* Unified enemy animation loading
* Cleaner configuration system
* Asset manager integration

---

## Phase 8 - Content Expansion

Planned

### New Enemies

* Advanced raptors
* Shield enemy
* Heavy mutant
* Mini-bosses

### New Weapons

* Shotgun
* Rifle
* Grenade
* Spear

### New Stages / Episodes

* City
* Jungle
* Laboratory
* Mine

---

## Phase 9 - Production Features

Planned

### Save System

* Save progress
* Continue system polish
* Unlocks

### Level Editor

* Enemy placement
* Wave editing
* Prop placement
* Walkable polygon editing
* Exit rectangle editing

### Testing

* Balance pass
* Performance pass
* Bug fixing

---

## Phase 10 - Release Preparation

Future

### Local Co-op

* Two players
* Shared camera

### Optional Networking

* Online co-op
* Synchronization layer

### Release

* Windows
* macOS
* Linux
