import pygame

def create_enemy_frames():
    frames = []
    colors = [
        (40,40,220),
        (80,80,255),
        (120,120,255)
    ]

    for color in colors:
        image = pygame.Surface(
            (50,80),
            pygame.SRCALPHA
        )
        pygame.draw.rect(
            image,
            color,
            (0,0,50,80)
        )
        frames.append(image)

    return frames