import pygame

class SpriteSheet:
    def __init__(self, filename):
        self.sheet = pygame.image.load(filename).convert_alpha()

    def get_frame(self, x, y, width, height):
        image = pygame.Surface((width, height), pygame.SRCALPHA)
        image.blit(self.sheet, (0,0), (x, y, width, height))
        return image

    def load_row(self, y, frame_width, frame_height, frame_count):
        frames = []
        for i in range(frame_count):
            frame = self.get_frame(i*frame_width,y,frame_width, frame_height)
            frames.append(frame)

        return frames


