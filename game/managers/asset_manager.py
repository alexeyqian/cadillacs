import os
import pygame
from game.animation.asset_loader import AssetLoader

class AssetManager:
    _image_cache = {}
    _scaled_image_cache = {}
    _animation_cache = {}
    _sound_cache = {}
    _missing_assets = set()
    
    @classmethod
    def file_exists(cls, path):
        return path and os.path.exists(path)

    @classmethod
    def _missing_asset(cls, path, fallback_factory=None):
        if path:
            cls._missing_assets.add(path)
        return fallback_factory() if fallback_factory else None

    @classmethod
    def load_image(cls, path, alpha=True, fallback_factory=None):
        if not path:
            return fallback_factory() if fallback_factory else None

        key = (path, alpha)
        if key in cls._image_cache:
            return cls._image_cache[key]

        if not cls.file_exists(path):
            image = cls._missing_asset(path, fallback_factory)
            cls._image_cache[key] = image
            return image
        
        try:
            image = pygame.image.load(path)
            image = image.convert_alpha() if alpha else image.convert()
        except pygame.error:
            image = cls._missing_asset(path, fallback_factory)

        cls._image_cache[key] = image
        return image

    @classmethod
    def load_scaled_image(cls, path, size, alpha=True, smooth=False, fallback_factory=None):
        if not path:
            return fallback_factory() if fallback_factory else None

        key = (path, alpha, size)
        if key in cls._scaled_image_cache:
            return cls._scaled_image_cache[key]

        image = cls.load_image(path, alpha=alpha, fallback_factory=fallback_factory)
        if image is None:
            cls._scaled_image_cache[key] = None
            return None

        scaler = pygame.transform.smoothscale if smooth else pygame.transform.scale
        scaled = scaler(image, size)
        cls._scaled_image_cache[key] = scaled
        return scaled

    @classmethod
    def load_animation(cls, config, fallback_frame_factory):
        if not config:
            return fallback_frame_factory()

        path = config["file"]
        frame_width = config["frame_width"]
        frame_height = config["frame_height"]
        frame_count = config["frame_count"]
        start_frame = config.get("start_frame", 0)
        key = (path, frame_width, frame_height, frame_count, start_frame)
        if key in cls._animation_cache:
            return cls._animation_cache[key]

        if path and  cls.file_exists(path):
            try:
                # frames are list of pygame.Surface
                frames = AssetLoader.load_animation(
                    path, frame_width, frame_height, frame_count, start_frame)
            except pygame.error:
                cls._missing_asset(path)
                frames = fallback_frame_factory()
        else:
            cls._missing_asset(path)
            frames = fallback_frame_factory()

        if not frames:
            frames = fallback_frame_factory()

        cls._animation_cache[key] = frames
        return frames

    @classmethod
    def load_sound(cls, path):
        if not path:
            return None
        if path in cls._sound_cache:
            return cls._sound_cache[path]

        if not cls.file_exists(path):
            sound = cls._missing_asset(path)
            cls._sound_cache[path] = sound
            return sound

        try:
            sound = pygame.mixer.Sound(path)
        except pygame.error:
            cls._missing_asset(path)
            sound = None

        cls._sound_cache[path] = sound
        return sound

    @classmethod
    def get_missing_assets(cls):
        return sorted(cls._missing_assets)

    @classmethod
    def get_cache_stats(cls):
        return {
            "images": len(cls._image_cache),
            "scaled_images": len(cls._scaled_image_cache),
            "animations": len(cls._animation_cache),
            "sounds": len(cls._sound_cache),
            "missing_assets": len(cls._missing_assets),
        }

    @classmethod
    def clear_cache(cls):
        cls._image_cache.clear()
        cls._scaled_image_cache.clear()
        cls._animation_cache.clear()
        cls._sound_cache.clear()
        cls._missing_assets.clear()
