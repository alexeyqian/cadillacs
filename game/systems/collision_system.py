from game.components.character_state import CharacterState
from game.entities.enemy_state import EnemyState


class CollisionSystem:
    @staticmethod
    def enemy_blocks_movement(enemy):
        return _enemy_blocks_movement(enemy)


    @staticmethod
    def resolve_player_enemy(game_state, old_player_x, old_player_y):
        player = game_state.player
        if player.state == player.DEAD:
            return
        for enemy in game_state.enemies:
            if not _enemy_blocks_movement(enemy):
                continue
            player_rect = player.get_collision_rect()
            enemy_rect = enemy.get_collision_rect()
            if not player_rect.colliderect(enemy_rect):
                continue
            old_player_rect = player_rect.copy()
            old_player_rect.x += int(old_player_x - player.x)
            old_player_rect.y += int(old_player_y - player.y)
            _push_player_out_of_enemy(player, player_rect, enemy_rect, old_player_rect)

    @staticmethod
    def resolve_enemy_enemy(game_state):
        enemies = game_state.enemies
        for i, enemy in enumerate(enemies):
            if not _enemy_blocks_movement(enemy):
                continue
            for other in enemies[i + 1:]:
                if not _enemy_blocks_movement(other):
                    continue
                enemy_rect = enemy.get_collision_rect()
                other_rect = other.get_collision_rect()
                if enemy_rect.colliderect(other_rect):
                    _push_enemies_apart(enemy, other, enemy_rect, other_rect)


def _enemy_blocks_movement(enemy):
    non_blocking = {CharacterState.DEAD, CharacterState.GRABBED, CharacterState.KNOCKDOWN, EnemyState.THROWN}
    return enemy.state not in non_blocking


def _push_player_out_of_enemy(player, player_rect, enemy_rect, old_player_rect):
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
    if min(overlap_left, overlap_right) <= min(overlap_top, overlap_bottom):
        if player_rect.centerx < enemy_rect.centerx:
            player.x -= overlap_left
        else:
            player.x += overlap_right
    else:
        if player_rect.centery < enemy_rect.centery:
            player.y -= overlap_top
        else:
            player.y += overlap_bottom


def _push_enemies_apart(enemy, other, enemy_rect, other_rect):
    overlap_left = enemy_rect.right - other_rect.left
    overlap_right = other_rect.right - enemy_rect.left
    overlap_top = enemy_rect.bottom - other_rect.top
    overlap_bottom = other_rect.bottom - enemy_rect.top
    if min(overlap_left, overlap_right) <= min(overlap_top, overlap_bottom):
        if enemy_rect.centerx <= other_rect.centerx:
            enemy.x -= overlap_left / 2
            other.x += overlap_left / 2
        else:
            enemy.x += overlap_right / 2
            other.x -= overlap_right / 2
    else:
        if enemy_rect.centery <= other_rect.centery:
            enemy.y -= overlap_top / 2
            other.y += overlap_top / 2
        else:
            enemy.y += overlap_bottom / 2
            other.y -= overlap_bottom / 2
