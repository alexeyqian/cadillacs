from game.level.wave import *

class Level:
    def __init__(self):
        self.current_wave = 0
        # used by wave battles
        self.camera_locked = False
        self.lock_x = None
        self.waves = [
            # first wave
            Wave(
                trigger_x=500,
                enemy_types=[
                    "normal",
                    "normal",
                    "normal"
                ]
            ),
            # second wave
            Wave(
                trigger_x=1200,
                enemy_types=[
                    "normal",
                    "fast",
                    "fast"
                ]
            ),
            # third wave
            Wave(
                trigger_x=2000,
                enemy_types=[
                    "heavy",
                    "normal",
                    "fast"
                ]
            ),
            BossWave(2300)
        ]

    def get_current_wave(self):
        if self.current_wave >= len(self.waves):
            return None

        return self.waves[self.current_wave]

