import os
import pygame

SOUNDS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "assets", "sounds")

# Map sound event names to filenames under assets/sounds/
SOUND_FILES = {
    "hit":        "hit.wav",
    "dead":       "dead.wav",
    "attack":     "attack.wav",
    "walk":       "walk.wav",
    "player_hit": "player_hit.wav",
    "player_dead":"player_dead.wav",
}

BGM_FILES = {
    "stage1": "bgm_stage1.ogg",
}


class SoundManager:
    def __init__(self, sfx_volume=0.8, bgm_volume=0.5):
        self.sfx_volume = sfx_volume
        self.bgm_volume = bgm_volume
        self._sounds = {}
        self._walk_channel = None
        self._enabled = True
        self._load_sounds()

    def _load_sounds(self):
        for name, filename in SOUND_FILES.items():
            path = os.path.join(SOUNDS_DIR, filename)
            if os.path.exists(path):
                sound = pygame.mixer.Sound(path)
                sound.set_volume(self.sfx_volume)
                self._sounds[name] = sound

    def play(self, name):
        if not self._enabled:
            return
        sound = self._sounds.get(name)
        if sound:
            sound.play()

    def start_walk_loop(self):
        if not self._enabled:
            return
        sound = self._sounds.get("walk")
        if not sound:
            return
        if self._walk_channel and self._walk_channel.get_busy():
            return
        self._walk_channel = sound.play(-1)

    def stop_walk_loop(self):
        if self._walk_channel and self._walk_channel.get_busy():
            self._walk_channel.stop()
        self._walk_channel = None

    def play_bgm(self, name):
        if not self._enabled:
            return
        filename = BGM_FILES.get(name)
        if not filename:
            return
        path = os.path.join(SOUNDS_DIR, filename)
        if not os.path.exists(path):
            return
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(self.bgm_volume)
        pygame.mixer.music.play(-1)

    def stop_bgm(self):
        pygame.mixer.music.stop()

    def set_enabled(self, enabled):
        self._enabled = enabled
        if not enabled:
            self.stop_bgm()
            self.stop_walk_loop()
