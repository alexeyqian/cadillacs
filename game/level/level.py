from game.level.wave import Wave
from game.entities.boss_enemy import BossEnemy

class BossWave:
    def __init__(self, trigger_x):
        self.trigger_x = trigger_x
        self.started = False
        self.completed = False
    def spawn(self):
        self.started = True
        return [BossEnemy(2350,320)]

class Level:
    def __init__(self):
        self.current_wave = 0
        self.camera_locked = False
        self.lock_x = None
        self.waves = [
            Wave(
                500,
                [
                    (700,300),
                    (750,350)
                ]
            ),

            Wave(
                1300,
                [
                    (1500,300),
                    (1600,350),
                    (1700,400)
                ]
            ),

            Wave(
                1800,
                [
                    (2000,300),
                    (2100,350),
                    (2200,400),
                    (2300,350)
                ]
            ),
            BossWave(2300)
        ]

    def get_current_wave(self):
        if self.current_wave >= len(self.waves):
            return None

        return self.waves[self.current_wave]

