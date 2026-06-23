import pygame

from game.settings import (
    EXTERNAL_HEIGHT,
    EXTERNAL_WIDTH,
    FIT_WINDOW_TO_DISPLAY,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)


def get_window_size():
    if not FIT_WINDOW_TO_DISPLAY:
        return (SCREEN_WIDTH, SCREEN_HEIGHT)

    display_info = pygame.display.Info()
    display_w = display_info.current_w or EXTERNAL_WIDTH
    display_h = display_info.current_h or EXTERNAL_HEIGHT

    max_window_w = min(EXTERNAL_WIDTH, display_w)
    max_window_h = min(EXTERNAL_HEIGHT, display_h)
    scale = min(max_window_w / SCREEN_WIDTH, max_window_h / SCREEN_HEIGHT)
    scale = min(1.0, scale)

    return (
        max(1, int(SCREEN_WIDTH * scale)),
        max(1, int(SCREEN_HEIGHT * scale)),
    )


def present_screen(screen, window):
    if screen.get_size() == window.get_size():
        window.blit(screen, (0, 0))
    else:
        scaled = pygame.transform.smoothscale(screen, window.get_size())
        window.blit(scaled, (0, 0))

    pygame.display.flip()
