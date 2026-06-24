def advance_player_lifecycle(game_state):
    """Guard dead state, run reactions, advance timers. Returns (player_can_act)."""
    player = game_state.player
    lifecycle_blocked = player.state == player.DEAD
    player.update_lifecycle_state()
    player_is_blocked = lifecycle_blocked or player.update_reactions()
    player_can_act = not player_is_blocked
    if player_can_act:
        player.advance_timers()
    return player_can_act


def advance_enemy_lifecycle(game_state):
    """Run lifecycle/reactions/timers for each enemy. Returns active_enemies list."""
    active_enemies = []
    for enemy in game_state.enemies:
        if enemy.update_lifecycle_state():
            continue
        if enemy.update_reactions():
            continue
        enemy.advance_timers()
        active_enemies.append(enemy)
    return active_enemies


def advance_managers(game_state):
    game_state.score_manager.update()
    game_state.announcement_manager.update()
    game_state.stage_clear_manager.update()
