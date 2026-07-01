import pygame


class PlayerInput:
    def __init__(self, keys):
        self.left = keys[pygame.K_LEFT] or keys[pygame.K_a]
        self.right = keys[pygame.K_RIGHT] or keys[pygame.K_d]
        self.up = keys[pygame.K_UP] or keys[pygame.K_w]
        self.down = keys[pygame.K_DOWN] or keys[pygame.K_s]

        self.jump = keys[pygame.K_k] or keys[pygame.K_SPACE]
        self.attack = keys[pygame.K_j]
        # todo: add auto drop
        self.drop = keys[pygame.K_q]
