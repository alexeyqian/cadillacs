from game.level.background import Background
from game.level.wave import *
from game.level.spawner import EnemySpawner

# background image, far layer, ground layer foreground layer
class Level:
    def __init__(self):
        self.background = Background()
        self.background.load(
            "game/assets/backgrounds/stage1/stage1_far.png",
            "game/assets/backgrounds/stage1/stage1_mid.png",
            "game/assets/backgrounds/stage1/stage1_front.png"
        )

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
            # fourth wave: introduce the dinosaur enemy
            Wave(
                trigger_x=2200,
                enemy_types=[
                    "raptor",
                    "normal",
                    "raptor"
                ]
            ),
            BossWave(2300),
            SpawnWave(
                trigger_x=2400,
                spawners=[
                    EnemySpawner(
                        2800,
                        350,
                        "normal",
                        5,
                        120
                    )
                ]
            )
        ]

    def get_current_wave(self):
        if self.current_wave >= len(self.waves):
            return None

        return self.waves[self.current_wave]
