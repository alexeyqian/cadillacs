from game.level.wave import Wave

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
                2200,
                [
                    (2400,300),
                    (2500,350),
                    (2600,400),
                    (2700,350)
                ]
            )
        ]

    def get_current_wave(self):
        if self.current_wave >= len(self.waves):
            return None

        return self.waves[self.current_wave]

