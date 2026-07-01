import os
import pygame

from game.settings import FPS
from game.bootstrap import create_display, create_game_state
from game.display import present_screen
from game.system_event_handler import handle_system_events

from game.level.stage_loader import advance_to_next_stage
from game.systems.gameplay_system import update_gameplay
from game.systems.bounds_system import BoundsSystem

from main_draw import main_draw

os.environ["SDL_VIDEO_WINDOW_POS"] = "0,0"

def main():
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()
    pygame.mixer.set_num_channels(16)

    window, screen = create_display()
    clock = pygame.time.Clock()
    game_state = create_game_state(screen, clock)
    #game_state.sound_manager.play_bgm("stage1")

    while game_state.running:
        # 0. System event check, such as: show menu, pause/resume, debug etc
        handle_system_events(game_state)
        # above function might set game_state.running to False
        if not game_state.running:
            break

        keys = pygame.key.get_pressed()

        # 0. Pre-gameplay check, 
        # including lifecycle guard, decide if player/entity can participate this frame.
        # 0.1 player death check
        if (game_state.player.state == game_state.player.DEAD
            and game_state.player.lifecycle_state.lives <= 0
            and game_state.credits > 0):
            game_state.continue_active = True
        # continue screen active check and update
        if game_state.continue_active:
            update_continue(game_state, keys)
            main_draw(game_state)
            present_screen(screen, window)
            clock.tick(FPS)
            continue

        # 0.2 end of current stage check
        if game_state.stage_clear_manager.active:
            game_state.stage_clear_manager.update()
            game_state.stage_clear_manager.apply_bonus(game_state.score_manager)
            if game_state.stage_clear_manager.timer <= 0:
                game_state.running = advance_to_next_stage(game_state)
                continue

        # 2. gameplay and camera update
        # info: advance timers happens at each component's beginning of update function
        update_gameplay(game_state, keys)
        game_state.camera.update(game_state.player, game_state.level)
        BoundsSystem.apply_player_camera(game_state)

        # 3. render and clock tick
        main_draw(game_state)
        present_screen(screen, window)
        clock.tick(FPS)

    pygame.quit()

def update_continue(game_state, keys):
    if game_state.continue_timer > 0:
        game_state.continue_timer -= 1
    if game_state.continue_timer <= 0:
        game_state.continue_active = False

    if keys[pygame.K_c]:
        if game_state.credits <= 0:
            return
        game_state.credits -= 1
        player = game_state.player
        player.lifecycle_state.lives = 3
        player.health.hp = player.health.max_hp
        player.state_machine.change_to(player, player.IDLE)
        player.x = 960
        player.y = 540

        game_state.continue_timer = 600
        game_state.continue_active = False
        # todo: add limits for continue times
        game_state.continue_used += 1

if __name__ == "__main__":
    main()
