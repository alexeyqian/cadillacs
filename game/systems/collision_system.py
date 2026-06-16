def resolve_player_enemy_collisions(game_state, old_player_x, old_player_y):
    player = game_state.player

    if player.state == player.DEAD:
        return

    for enemy in game_state.enemies:
        if not enemy_blocks_player(enemy):
            continue

        player_rect = player.get_collision_rect()
        enemy_rect = enemy.get_collision_rect()

        if not player_rect.colliderect(enemy_rect):
            continue

        old_player_rect = player_rect.copy()
        old_player_rect.x += int(old_player_x - player.x)
        old_player_rect.y += int(old_player_y - player.y)

        push_player_out_of_enemy(player, player_rect, enemy_rect, old_player_rect)


def enemy_blocks_player(enemy):
    non_blocking_states = {
        enemy.DEAD,
        enemy.GRABBED,
        enemy.THROWN,
    }
    return enemy.state not in non_blocking_states


def push_player_out_of_enemy(player, player_rect, enemy_rect, old_player_rect):
    if old_player_rect.right <= enemy_rect.left:
        player.x -= player_rect.right - enemy_rect.left
        return

    if old_player_rect.left >= enemy_rect.right:
        player.x += enemy_rect.right - player_rect.left
        return

    if old_player_rect.bottom <= enemy_rect.top:
        player.y -= player_rect.bottom - enemy_rect.top
        return

    if old_player_rect.top >= enemy_rect.bottom:
        player.y += enemy_rect.bottom - player_rect.top
        return

    overlap_left = player_rect.right - enemy_rect.left
    overlap_right = enemy_rect.right - player_rect.left
    overlap_top = player_rect.bottom - enemy_rect.top
    overlap_bottom = enemy_rect.bottom - player_rect.top
    smallest_x_push = min(overlap_left, overlap_right)
    smallest_y_push = min(overlap_top, overlap_bottom)

    if smallest_x_push <= smallest_y_push:
        if player_rect.centerx < enemy_rect.centerx:
            player.x -= overlap_left
        else:
            player.x += overlap_right
    else:
        if player_rect.centery < enemy_rect.centery:
            player.y -= overlap_top
        else:
            player.y += overlap_bottom
