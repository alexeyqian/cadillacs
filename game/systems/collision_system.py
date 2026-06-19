from game.entities.character_state import CharacterState
from game.entities.enemy_state import EnemyState


def resolve_player_enemy_collisions(game_state, old_player_x, old_player_y):
    player = game_state.player

    if player.state == player.DEAD:
        return

    for enemy in game_state.enemies:
        if not enemy_blocks_movement(enemy):
            continue

        player_rect = player.get_collision_rect()
        enemy_rect = enemy.get_collision_rect()

        if not player_rect.colliderect(enemy_rect):
            continue

        old_player_rect = player_rect.copy()
        old_player_rect.x += int(old_player_x - player.x)
        old_player_rect.y += int(old_player_y - player.y)

        push_player_out_of_enemy(player, player_rect, enemy_rect, old_player_rect)


def resolve_enemy_enemy_collisions(game_state):
    enemies = game_state.enemies

    for index, enemy in enumerate(enemies):
        if not enemy_blocks_movement(enemy):
            continue

        for other in enemies[index + 1:]:
            if not enemy_blocks_movement(other):
                continue

            enemy_rect = enemy.get_collision_rect()
            other_rect = other.get_collision_rect()

            if not enemy_rect.colliderect(other_rect):
                continue

            push_enemies_apart(enemy, other, enemy_rect, other_rect)


def enemy_blocks_movement(enemy):
    non_blocking_states = {
        CharacterState.DEAD,
        CharacterState.GRABBED,
        CharacterState.KNOCKDOWN,
        EnemyState.THROWN,
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


def push_enemies_apart(enemy, other, enemy_rect, other_rect):
    overlap_left = enemy_rect.right - other_rect.left
    overlap_right = other_rect.right - enemy_rect.left
    overlap_top = enemy_rect.bottom - other_rect.top
    overlap_bottom = other_rect.bottom - enemy_rect.top
    smallest_x_push = min(overlap_left, overlap_right)
    smallest_y_push = min(overlap_top, overlap_bottom)

    if smallest_x_push <= smallest_y_push:
        if enemy_rect.centerx <= other_rect.centerx:
            split_push(enemy, other, -overlap_left, overlap_left)
        else:
            split_push(enemy, other, overlap_right, -overlap_right)
    else:
        if enemy_rect.centery <= other_rect.centery:
            split_push_y(enemy, other, -overlap_top, overlap_top)
        else:
            split_push_y(enemy, other, overlap_bottom, -overlap_bottom)


def split_push(enemy, other, enemy_push, other_push):
    enemy.x += enemy_push / 2
    other.x += other_push / 2


def split_push_y(enemy, other, enemy_push, other_push):
    enemy.y += enemy_push / 2
    other.y += other_push / 2
