import pygame
from game.animation.asset_loader import AssetLoader
from game.animation.file_utils import file_exists

class AssetManager:
    _image_cache = {}
    _animation_cache = {}
    
    @classmethod
    def load_image(cls, path, alpha=True):
        key = (path, alpha)
        if key in cls._image_cache:
            return cls._image_cache[key]
        if not file_exists(path):
            return None
        
        image = pygame.image.load(path)
        if alpha:
            image = image.convert_alpha()
        else:
            image = image.convert()
            
        cls._image_cache[key] = image
        return image
    
    @classmethod
    def load_animation(cls, config, fallback_frame_factory):
        path = config["file"]
        frame_width = config["frame_width"]
        frame_height = config["frame_height"]
        frame_count = config["frame_count"]
        key = (path, frame_width, frame_height, frame_count)
        if key in cls._animation_cache:
            return cls._animation_cache[key]
        if file_exists(path):
            # frames are list of pygame.Surface
            frames = AssetLoader.load_animation(path, frame_width, frame_height, frame_count)
        else:
            frames = fallback_frame_factory()
        cls._animation_cache[key] = frames
        return frames
    
    @classmethod
    def clear_cache(cls):
        cls._image_cache.clear()
        cls._animation_cache.clear()
