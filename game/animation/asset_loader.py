from game.animation.spritesheet import SpriteSheet

class AssetLoader:
    @staticmethod
    def load_animation(filename, frame_width, frame_height, frame_count, start_frame=0):
        sheet = SpriteSheet(filename)
        if start_frame:
            return sheet.load_row_range(
                0, frame_width, frame_height, start_frame, frame_count)
        return sheet.load_row(0, frame_width, frame_height, frame_count)
