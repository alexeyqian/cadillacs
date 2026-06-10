import pygame
from game.level.wave import SpawnWave

def player_is_in_exit_rect(player, exit_rect):
    exit_area = pygame.Rect(exit_rect)
    player_feet = player.get_collision_rect()
    return exit_area.colliderect(player_feet)

# simple rune for normal stages
# if level has no waves and player reaches right side of stage:
#    activate stage clear
def update_wave_system(game_state):
    level = game_state.level
    player = game_state.player
    camera = game_state.camera
    enemies = game_state.enemies
    
    if len(level.waves) == 0: # for transition stage
        if (player_is_in_exit_rect(player, level.exit_rect)
            and not game_state.stage_clear_manager.active):
            game_state.stage_clear_manager.activate(player)

        return

    wave = level.get_current_wave()

    # add wave warning announcement before distance 300
    if wave and not wave.started and player.x + 300 >= wave.trigger_x:
        if wave.__class__.__name__ == "BossWave":
            game_state.announcement_manager.show(
                "WARNING", "BOSS APPROACHING", 120)
        else:
            game_state.announcement_manager.show(
                f"WAVE {game_state.level.current_wave + 1}",
                "GET READY", 90)

    if wave and not wave.started and player.x >= wave.trigger_x:
            # start the wave and initialize pending enemies
            wave.spawn(camera.x, level.lane_top, level.lane_bottom)
            # lock camera only when wave actually starts
            # set lock_x to current camera.x so the viewport does not jump
            # it only freeze camera, not stop player by itself
            level.camera_locked = True
            level.lock_x = camera.x

    if wave and wave.started:
        # for normal Wave and BossWave
        if hasattr(wave, "update_spawn"):
            new_enemies = wave.update_spawn()
            if new_enemies:
                enemies.extend(new_enemies)
        # only for SpawnWave
        if hasattr(wave, "update"):
            enemies.extend(wave.update())

def update_wave_completion(game_state):
    level = game_state.level
    enemies = game_state.enemies

    wave = level.get_current_wave()
    if wave and wave.started:
        wave_finished = False
        if isinstance(wave, SpawnWave):
            wave_finished = wave.all_spawners_finished() and len(enemies) == 0
        else:
            wave_finished = len(enemies) == 0

        if wave_finished:
            wave.completed = True
            level.current_wave += 1
            level.camera_locked = False

            all_waves_done = level.current_wave >= len(level.waves)
            if all_waves_done and player_is_in_exit_rect(game_state.player, level.exit_rect):
                if not game_state.stage_clear_manager.active:
                    game_state.stage_clear_manager.activate(game_state.player)

            #exit_x = level.world_width - 180
            #if level.current_wave >= len(level.waves) and game_state.player.x >= exit_x:
            #    game_state.stage_clear_manager.activate(game_state.player)
