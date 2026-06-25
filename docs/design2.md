Guidelines:

Component = state/data capability
Controller = behavior/process using components
Entity = wiring + stable public API
The component can manage its own fields when the behavior is tightly local:
Controllers can have fields too, but mostly when the fields are part of the controller’s process, not the character’s identity.

For this codebase, I’d keep the practical rule:
If it describes what the character has/is, use a component.
If it describes what process is currently running, controller field is okay.
If many systems read it constantly and it is fundamental, keep it on Character.
If a field only exists because a controller needs bookkeeping, keep it inside that controller.
If a component has enough state plus local behavior, let it manage itself. That is exactly the point of the component.

GameObject handles position, rect, rendering basics
Character handles health, movement, combat, state, animation
Player handles input-driven behavior
Enemy handles AI-driven behavior
The key rule: share mechanics, not decisions.

Players and enemies both move, take damage, attack, collide, die and animate. But players decide actions from keyboard input, while enemies decide actions from AI.

Common Fields For Player And Enemy
These usually belong in a shared Character class:
class Character:
    id
    name

    # Position / space
    x
    y
    z_or_depth
    velocity_x
    velocity_y
    facing_direction

    # Collision
    collision_rect
    hurtbox
    hitboxes

    # Stats
    max_health
    health
    move_speed
    attack_damage
    defense
    knockback_resistance

    # Combat
    current_attack
    attack_cooldown
    combo_index
    is_invincible
    invincibility_timer
    can_be_hit

    # State
    state
    previous_state
    state_timer
    is_alive
    is_grounded
    is_stunned
    is_attacking

    # Animation
    animation_controller
    current_animation
    frame_index

    # Equipment / weapons
    equipped_weapon
    held_item

    # Team / faction
    faction

Because movement is not purely platformer-style. The player moves left/right and slightly up/down in a stage-depth plane. So also consider add these fields:
screen_depth_y
lane_y
grabbed_target
grabbed_by
combo_state

class Player(Character):
    player_index
    input_controller
    selected_character_id

    lives
    score
    continues
    special_meter

    combo_buffer
    input_buffer

    inventory

Player-specific behavior:

read keyboard/gamepad input
convert input into character intentions
manage combo input
trigger special attacks
handle player-only UI values like score, lives, continues
The player should not directly poll PyGame everywhere. Prefer this:
InputManager -> PlayerController -> Player

Enemy-Specific Fields

These should stay in Enemy:
class Enemy(Character):
    enemy_type
    ai_controller
    target

    detection_range
    attack_range
    leash_range

    aggression
    patrol_points
    spawn_position

    score_value
    loot_table

    behavior_state

Enemy-specific behavior:

choose target
chase player
decide when to attack
retreat or reposition
coordinate with other enemies
drop item or points on death
Enemy classes should be expandable through data/config as much as possible.

Example
ENEMY_DEFINITIONS = {
    "punk": {
        "health": 50,
        "move_speed": 2.0,
        "attack_damage": 8,
        "ai": "basic_melee",
        "score_value": 100,
    },
    "brute": {
        "health": 120,
        "move_speed": 1.2,
        "attack_damage": 18,
        "ai": "slow_heavy",
        "score_value": 300,
    },
}

class Character:
    def update(self, dt):
        update_state()
        update_movement()
        update_animation()
        update_timers()

    def move(self, direction, dt):
        ...

    def take_damage(self, damage, source):
        ...

    def attack(self):
        ...

    def die(self):
        ...

A useful split is:
Character = body and mechanics
Controller = decision maker
Manager = owns groups/lifetime/system coordination

A manager usually handles collections or systems.
Use a manager when something owns or coordinates many objects. like:
EntityManager
EnemyManager
CollisionManager
CombatManager
InputManager
SpawnManager
LevelManager
AudioManager

Simple rule:
Controller = controls one thing.
Manager = manages many things.
System = applies rules across many things.

Recommended Class Design

A clean design could look like:
src/
  entities/
    game_object.py
    character.py
    player.py
    enemy.py

  controllers/
    player_controller.py
    enemy_ai_controller.py

  combat/
    attack.py
    hitbox.py
    hurtbox.py
    combat_system.py

  animation/
    animation.py
    animation_controller.py

  managers/
    entity_manager.py
    enemy_manager.py
    input_manager.py
    spawn_manager.py

  data/
    players.py
    enemies.py
    weapons.py

Ideally
Player = Character + player-specific data
Enemy = Character + enemy-specific data
Controller = behavior
Manager/System = coordination
Data files = stats/configuration

Combat Design
Attack creates hitbox
CombatSystem checks hitbox vs hurtbox
Target receives damage
Example flow:
Player presses attack
PlayerController tells Player to attack
Character starts attack animation
Attack frame activates hitbox
CombatSystem detects overlap
Enemy.take_damage(...)
Enemy enters HIT_STUN

Common combat objects:
AttackDefinition:
    name
    damage
    startup_frames
    active_frames
    recovery_frames
    hitbox_size
    knockback
    stun_time
    animation_name

Weapon can modify or replace attack definitions.

for enemy, Prefer behavior composition:
enemy.ai = BasicMeleeAI()
enemy.ai = ChargerAI()
enemy.ai = RangedAI()
enemy.ai = BossAI()

A good production-friendly balance is:
Small inheritance for shared identity/mechanics.
Composition for behavior, AI, weapons, animation, attacks.
Managers for coordination.

I would design it like this:
class Character(GameObject):
    def update(self, dt, world):
        self.controller.update(self, world, dt)
        self.state_machine.update(self, dt)
        self.physics.update(self, dt)
        self.animation.update(self, dt)

class Player(Character):
    pass

class Enemy(Character):
    pass

That keeps the game flexible:

different playable characters
different enemy types
reusable combat
future level editor support
easier testing
cleaner milestone development
