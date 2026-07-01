import pygame
from game.level.wave import BossWave, Wave
from game.settings import SCREEN_WIDTH


class WaveSystem:
    @staticmethod
    def update_completion(game_state):
        wave = game_state.level.get_current_wave()
        if not wave or not wave.started:
            return
        if not _is_wave_finished(game_state, wave):
            return
        _complete_wave(game_state, wave)

    @staticmethod
    def update(game_state):
        level = game_state.level
        if len(level.waves) == 0:
            _check_stage_exit(game_state)
            return
        wave = level.get_current_wave()
        if wave is None:
            level.camera_locked = False
            level.lock_x = None
            _check_stage_exit(game_state)
            return
        _update_wave_announcement(game_state, wave)
        _update_wave_trigger(game_state, wave)
        _tick_wave_spawns(game_state, wave)


def _player_is_in_exit_rect(player, exit_rect):
    return pygame.Rect(exit_rect).colliderect(player.get_collision_rect())


def _get_player_trigger_x(player):
    return player.get_collision_rect().right


def _get_camera_lock_x(camera_x, level):
    max_lock_x = max(0, level.world_width - SCREEN_WIDTH)
    return max(0, min(camera_x, max_lock_x))


def _check_stage_exit(game_state):
    if (_player_is_in_exit_rect(game_state.player, game_state.level.exit_rect)
            and not game_state.stage_clear_manager.active):
        game_state.stage_clear_manager.activate(game_state.player)


def _is_wave_finished(game_state, wave):
    return wave.is_spawning_done() and len(game_state.enemies) == 0


def _complete_wave(game_state, wave):
    level = game_state.level
    wave.completed = True
    level.current_wave += 1
    level.camera_locked = False
    level.lock_x = None
    if level.current_wave >= len(level.waves):
        _check_stage_exit(game_state)


def _update_wave_announcement(game_state, wave):
    if wave.started:
        return
    player_trigger_x = _get_player_trigger_x(game_state.player)
    if player_trigger_x + 300 < wave.trigger_x:
        return
    if isinstance(wave, BossWave):
        game_state.announcement_manager.show("WARNING", "BOSS APPROACHING", 120)
    else:
        game_state.announcement_manager.show(
            f"WAVE {game_state.level.current_wave + 1}", "GET READY", 90)


def _update_wave_trigger(game_state, wave):
    if wave.started:
        return
    if _get_player_trigger_x(game_state.player) < wave.trigger_x:
        return
    level = game_state.level
    camera = game_state.camera
    wave.start(camera.x, level.lane_top, level.lane_bottom, game_state.player.x)
    level.camera_locked = True
    level.lock_x = _get_camera_lock_x(camera.x, level)


def _tick_wave_spawns(game_state, wave):
    if not wave.started:
        return
    new_enemies = wave.tick(len(game_state.enemies))
    if new_enemies:
        game_state.enemies.extend(new_enemies)
