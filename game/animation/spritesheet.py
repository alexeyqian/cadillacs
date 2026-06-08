import pygame

class SpriteSheet:
    def __init__(self, filename):
        self.sheet = pygame.image.load(filename).convert_alpha()
        self.sheet_width, self.sheet_height = self.sheet.get_size()

    # copy one rectangle area from sprite sheet into new created surface
    # the returned surface contains single extracted frame
    def get_frame(self, x, y, width, height):
        image = pygame.Surface((width, height), pygame.SRCALPHA)
        image.blit(self.sheet, (0,0), (x, y, width, height))
        return image
        # more performance way, return sub view, no copy
        # return self.sheet.subsurface((x,y,width, height))

    # return a list of pygame.Surfaces
    def load_row(self, y, frame_width, frame_height, frame_count):
        """
        Load a row of frames from the sprite sheet. If the requested frame_count
        exceeds the number of frames actually present in the sheet (based on
        sheet width and frame_width), this method will clamp to the available
        frames to avoid returning empty/transparent frames.
        """
        frames = []
        if frame_width <= 0:
            return frames

        # compute how many frames actually fit in the sheet horizontally
        max_count = self.sheet_width // frame_width
        if max_count <= 0:
            return frames

        # clamp the requested frame_count to available frames
        actual_count = frame_count if frame_count is not None else max_count
        actual_count = min(actual_count, max_count)

        for i in range(actual_count):
            frame = self.get_frame(i * frame_width, y, frame_width, frame_height)
            frames.append(frame)

        return frames


