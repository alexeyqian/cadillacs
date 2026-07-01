class SoundSystem:
    @staticmethod
    def update(game_state, sound_manager):
        _process_player_sound(game_state.player, sound_manager)
        for enemy in game_state.enemies:
            _process_enemy_sound(enemy, sound_manager)


def _process_player_sound(player, sound_manager):
    for event in player.events.drain():
        sound_manager.play(event["type"])
    is_walking = player.state in (player.WALK, player.RUN) and not player.movement.is_jumping
    if is_walking:
        sound_manager.start_walk_loop()
    else:
        sound_manager.stop_walk_loop()


def _process_enemy_sound(enemy, sound_manager):
    if not hasattr(enemy, "events"):
        return
    for event in enemy.events.drain():
        sound_manager.play(event["type"])
