import pygame

import game.settings as settings

def handle_system_events(game_state):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_state.running = False
            continue

        if event.type == pygame.KEYDOWN:
            _handle_keydown(game_state, event.key)



def _handle_keydown(game_state, key):
    if key == pygame.K_ESCAPE:
        game_state.running = False
    elif key == pygame.K_F1:
        settings.SHOW_COMBAT_BOXES = not settings.SHOW_COMBAT_BOXES
    elif key == pygame.K_p:
        _toggle_pause(game_state)
    elif key == pygame.K_5:
        # todo: insert coin as credit, only use for dev
        game_state.credits += 1
    if game_state.paused:
        _handle_pause_menu_key(game_state, key)


def _toggle_pause(game_state):
    # Pause/resume with P
    game_state.paused = not game_state.paused
    if game_state.paused:
        # initialize menu selection when entering pause
        game_state.pause_menu_index = 0


def _handle_pause_menu_key(game_state, key):
    # If paused, handle menu navigation and selection
    if key == pygame.K_UP:
        game_state.pause_menu_index = (
            (game_state.pause_menu_index - 1) % len(game_state.pause_menu_options)
        )
    elif key == pygame.K_DOWN:
        game_state.pause_menu_index = (
            (game_state.pause_menu_index + 1) % len(game_state.pause_menu_options)
        )
    elif key in (pygame.K_RETURN, pygame.K_KP_ENTER):
        _choose_pause_menu_item(game_state)


def _choose_pause_menu_item(game_state):
    choice = game_state.pause_menu_options[game_state.pause_menu_index]

    if choice == "Resume":
        game_state.paused = False
    elif choice == "Quit":
        game_state.running = False