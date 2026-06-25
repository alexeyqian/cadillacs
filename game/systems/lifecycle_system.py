# --- State queries ---

def is_player_blocked(player):
    """True if the player cannot act this frame (dead or in hit-stun)."""
    return player.state == player.DEAD or player.hit_reaction_controller.is_in_hit_stun()


def get_active_enemies(game_state):
    """Return enemies that are alive and not reaction-locked."""
    return [
        enemy for enemy in game_state.enemies
        if not enemy.update_lifecycle_state()
        and not enemy.reaction_controller.is_reaction_blocked(enemy)
    ]


# --- Timer advancement ---

def advance_player_timers(player):
    player.advance_timers()


def advance_enemy_timers(active_enemies):
    for enemy in active_enemies:
        enemy.advance_timers()


# --- Combined frame-state helpers (used by gameplay_system) ---

def advance_player_frame_state(game_state):
    """Guard dead/stun state, advance timers. Returns player_can_act."""
    player = game_state.player
    player.update_lifecycle_state()
    player_can_act = not is_player_blocked(player)
    if player_can_act:
        advance_player_timers(player)
    return player_can_act


def advance_enemy_frame_state(game_state):
    """Resolve lifecycle, advance timers. Returns active_enemies list."""
    active_enemies = get_active_enemies(game_state)
    advance_enemy_timers(active_enemies)
    return active_enemies
