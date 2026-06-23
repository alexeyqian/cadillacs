import pygame

from game.settings import (
    EXTERNAL_HEIGHT,
    EXTERNAL_WIDTH,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)



def get_window_size():
    # Use configured external dimensions directly.
    # pygame.display.Info() returns the usable desktop area on macOS,
    # which excludes the Dock and menu bar, causing the window to be
    # shorter than the actual screen. EXTERNAL_WIDTH/HEIGHT are the
    # true monitor resolution and should be trusted.
    max_window_w = EXTERNAL_WIDTH
    max_window_h = EXTERNAL_HEIGHT
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
