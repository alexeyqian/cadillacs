

Key snapshot
An input snapshot records the exact state of the controls at a single, frozen millisecond, rather than a history of everything that happened between frames.

An input snapshot is taken at the very beginning of the frame interval.This specific timing ensures that the game engine has the most up-to-date player choices before it runs any game logic, physics updates, or graphics rendering.

The Order of a Game FrameEvery frame in a 2D game follows a strict, linear timeline. It looks like this:Start of Frame → [Take Input Snapshot]: The game grabs the current state of the keyboard, mouse, or controller right now.Process Logic & Physics: The game updates positions. (e.g., Is Jump True in the snapshot? Move the player up.)Render Graphics: The GPU draws the updated positions on the screen.End of Frame → Display: The completed frame is pushed to your monitor.

Projectile and Frame
So a projectile collected in this lifecycle phase will not move or hit the player until the next frame. That matches the frame sequence idea: spawn late, begin logic next frame.

Player interface
update_lifecycle_state()
advance_timers()
request_actions(...)
update_movement(...)
update_animation()

Enemy Interface
update_lifecycle_state()
advance_timers()
update_ai(...)
update_movement(...)
update_attack(...)
update_animation()

Correct structure
_advance_lifecycle_and_timers   ← timers only
_update_enemy_decisions         ← AI
_request_player_actions         ← input
_update_character_movement      ← voluntary movement only (no apply_knockback)
_resolve_collisions             ← push-apart, bounds
_update_combat                  ← hitbox/hurtbox detection → sets damage + knockback velocity
_update_damage_and_reactions    ← apply_knockback, apply_hit_stun effects ← NEW
_update_lifecycle               ← spawn/cleanup
_update_presentation            ← animation, camera, render

Best practice: the entity owns the API surface, the controller owns the logic.

combat_system calls enemy.take_damage(DamageRequest)   ← entity: thin public API
    → unpacks DamageRequest
    → delegates to reaction_controller.take_damage()   ← controller: all decisions
        → health.take_damage()                         ← component: pure data
        → state transitions (die, knockdown, flinch)


enemy ai controller
owner.intent.move_toward_player()
owner.intent.attack_player()
owner.intent.patrol()
owner.intent.flank_to(position)

enemy flow
enemy.update_lifecycle_state()
enemy.advance_timers()
enemy.update_ai(context)        # decide intent/state only
enemy.update_movement(context)  # execute movement intent
enemy.update_attack(context)    # execute attack intent
enemy.update_animation()

def _advance_timers(game_state, active_enemies):
    game_state.player.advance_timers()

    for enemy in active_enemies:
        enemy.advance_timers()

    for projectile in game_state.player_projectiles:
        projectile.advance_timers()

    for projectile in game_state.enemy_projectiles:
        projectile.advance_timers()

    game_state.advance_timers()

The right hybrid approach
DataUnitReasonvelocity, gravity, timersseconds (dt)frame-rate independent, physics correctstartup_frames, active_frames, recovery_framesframesdesigner-facing, deterministic, genre conventionPhysics simulation stepfixed dt (e.g. 1/60s)deterministic collision, same as frame count but expressed clearly

int() in Python truncates toward zero. For damage you probably want floor (always round down, favoring the defender slightly), which int() achieves for positive values. But make the intent explicit.
The rounding policy is a design decision worth naming explicitly in the code rather than leaving as an implicit side effect of the type conversion.

class CollisionLayer(IntFlag):
    NONE       = 0
    PLAYER     = auto()
    ENEMY      = auto()
    PROJECTILE = auto()
    WORLD      = auto()
    PICKUP     = auto()