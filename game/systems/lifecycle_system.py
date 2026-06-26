def is_player_blocked(player):
    """True if the player cannot act this frame (dead or in hit-stun)."""
    return player.state == player.DEAD or player.reaction_controller.is_in_hit_stun(player)


def get_active_enemies(game_state):
    """Return enemies that are not reaction-locked this frame."""
    return [
        enemy for enemy in game_state.enemies
        if not enemy.reaction_controller.is_reaction_blocked(enemy)
    ]


def advance_player_frame_state(game_state):
    """Guard dead/stun state, advance timers. Returns player_can_act."""
    player = game_state.player
    player.update_lifecycle_state()
    player_can_act = not is_player_blocked(player)
    if player_can_act:
        player.advance_timers()
    return player_can_act


def advance_enemy_frame_state(game_state):
    """Tick forced states (thrown, knockdown, dead), then advance timers. Returns active_enemies list."""
    for enemy in game_state.enemies:
        enemy.update_state()
    active_enemies = get_active_enemies(game_state)
    for enemy in active_enemies:
        enemy.advance_timers()
    return active_enemies
