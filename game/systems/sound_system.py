# No special handling is needed — pygame.mixer.Sound.play() is fire-and-forget.
#When you call sound.play(), pygame hands the sound off to a dedicated mixer thread 
# that runs independently of the game loop. 
# The sound plays to completion on its own, regardless of how many game frames pass. 
# The game loop never waits for it.
# The only case that needs care is the walk loop — sound.play(-1) loops indefinitely, 
# so stop_walk_loop() must be called when the player stops. 
# That's already handled in sound_system.py by checking player.state each frame.

# The only real concern is channel exhaustion: if too many sounds fire simultaneously, 
# pygame runs out of the 16 channels and drops new sounds silently. 
# For a beat-em-up with multiple enemies this can happen. 
# The fix if needed is to assign higher-priority sounds (player hit, player dead) to reserved channels:
def update_sound(game_state, sound_manager):
    _process_player_sound(game_state.player, sound_manager)
    for enemy in game_state.enemies:
        _process_enemy_sound(enemy, sound_manager)


def _process_player_sound(player, sound_manager):
    for event in player.events.drain():
        sound_manager.play(event["type"])

    is_walking = (
        player.state in (player.WALK, player.RUN)
        and not player.movement.is_jumping
    )
    if is_walking:
        sound_manager.start_walk_loop()
    else:
        sound_manager.stop_walk_loop()


def _process_enemy_sound(enemy, sound_manager):
    if not hasattr(enemy, "events"):
        return
    for event in enemy.events.drain():
        sound_manager.play(event["type"])
