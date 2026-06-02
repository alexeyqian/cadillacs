import pygame

def create_player_frames():
    frames = []
    colors = [(220, 40, 40), (255, 60, 60), (255, 100, 100)]
    for color in colors:
        image = pygame.Surface((50, 80), pygame.SRCALPHA)
        pygame.draw.rect(image, color, (0,0,50,80))
        frames.append(image)
    return frames

