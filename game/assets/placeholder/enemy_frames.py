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

def create_raptor_frames():
    frames = []
    colors = [
        (30, 120, 80),
        (40, 155, 95),
        (55, 185, 115),
        (40, 155, 95),
    ]

    for i, color in enumerate(colors):
        image = pygame.Surface(
            (70, 60),
            pygame.SRCALPHA
        )

        body_y = 24
        leg_offset = i % 2

        # body and head
        pygame.draw.ellipse(image, color, (12, body_y, 38, 22))
        pygame.draw.ellipse(image, color, (45, body_y - 8, 20, 18))

        # tail
        pygame.draw.polygon(
            image,
            color,
            [(14, body_y + 8), (0, body_y + 2), (14, body_y + 15)]
        )

        # legs
        pygame.draw.line(image, (20, 80, 50),
            (24, body_y + 18), (20 - leg_offset * 4, 56), 4)
        pygame.draw.line(image, (20, 80, 50),
            (40, body_y + 18), (48 + leg_offset * 4, 56), 4)

        # eye and mouth
        pygame.draw.circle(image, (255, 240, 80), (58, body_y - 1), 2)
        pygame.draw.line(image, (10, 40, 30),
            (55, body_y + 7), (66, body_y + 9), 2)

        frames.append(image)

    return frames
