from game.animation.spritesheet import SpriteSheet

class AssetLoader:
    @staticmethod
    def load_animation(filename, frame_width, frame_height, frame_count):
        sheet = SpriteSheet(filename)
        return sheet.load_row(0, frame_width, frame_height, frame_count)