import pygame

from game.settings import SCREEN_HEIGHT, SCREEN_WIDTH

ASPECT = SCREEN_WIDTH / SCREEN_HEIGHT


def get_window_size():
    desktop_sizes = pygame.display.get_desktop_sizes()
    dw, dh = desktop_sizes[0] if desktop_sizes else (SCREEN_WIDTH, SCREEN_HEIGHT)
    if dw / dh > ASPECT:
        return (int(dh * ASPECT), dh)
    else:
        return (dw, int(dw / ASPECT))


def present_screen(screen, window):
    ww, wh = window.get_size()
    scaled = pygame.transform.smoothscale(screen, (ww, wh))
    window.fill((0, 0, 0))
    window.blit(scaled, (0, 0))
    pygame.display.flip()
