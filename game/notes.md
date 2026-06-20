

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