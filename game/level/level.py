from game.level.background import Background
from game.level.prop import Prop
from game.level.wave import *
from game.level.spawner import EnemySpawner

# background image, far layer, ground layer foreground layer
class Level:
    def __init__(self):
        self.background = Background(
            "game/assets/backgrounds/stage1/stage1_far.png",
            "game/assets/backgrounds/stage1/stage1_mid.png",
            "game/assets/backgrounds/stage1/stage1_front.png")
        
        self.props = [
                Prop(
                    700,
                    720,
                    "game/assets/props/car_wreck.png",
                    layer="back",
                    scale=1.5
                ),

                Prop(
                    2200,
                    700,
                    "game/assets/props/dino_bones.png",
                    layer="back",
                    scale=1.5
                ),

                Prop(
                    3900,
                    760,
                    "game/assets/props/barrel_green.png",
                    layer="front",
                    scale=1.3
                ),

                Prop(
                    5700,
                    760,
                    "game/assets/props/barrel_red.png",
                    layer="front",
                    scale=1.3
                ),

                Prop(
                    7200,
                    760,
                    "game/assets/props/bush.png",
                    layer="front",
                    scale=1.4
                ),
            ]

        self.current_wave = 0
        # used by wave battles
        self.camera_locked = False
        self.lock_x = None
        
        self.waves = [
            # first wave
            Wave(
                trigger_x=800,
                enemy_types=[
                    "normal",
                    "normal",
                    "normal"
                ]
            ),
            # second wave
            Wave(
                trigger_x=1500,
                enemy_types=[
                    "normal",
                    "fast",
                    "fast"
                ]
            ),
            # third wave
            Wave(
                trigger_x=4300,
                enemy_types=[
                    "heavy",
                    "normal",
                    "fast"
                ]
            ),
            # fourth wave: introduce the dinosaur enemy
            Wave(
                trigger_x=5300,
                enemy_types=[
                    "raptor",
                    "normal",
                    "raptor"
                ]
            ),
            BossWave(6200),
            SpawnWave(
                trigger_x=6500,
                spawners=[
                    EnemySpawner(
                        6800,
                        600,
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
    
    def draw_props(self, screen, camera_x, layer):
        for prop in self.props:
            if prop.layer == layer:
                prop.draw(screen, camera_x)
