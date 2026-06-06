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
            # Wave 1: simple warm-up, teaches arena lock.
            Wave(
                trigger_x=900,
                enemy_types=[
                    "normal",
                    "normal"
                ]
            ),

            # Wave 2: one fast enemy adds pressure without overwhelming.
            Wave(
                trigger_x=2100,
                enemy_types=[
                    "normal",
                    "fast"
                ]
            ),

            # Wave 3: first medium mixed group.
            Wave(
                trigger_x=3400,
                enemy_types=[
                    "normal",
                    "normal",
                    "fast"
                ]
            ),

            # Wave 4: introduce heavy enemy with only light support.
            Wave(
                trigger_x=4700,
                enemy_types=[
                    "heavy",
                    "normal"
                ]
            ),

            # Wave 5: introduce dinosaurs after the player has seen heavy enemies.
            Wave(
                trigger_x=5900,
                enemy_types=[
                    "raptor",
                    "normal",
                    "fast"
                ]
            ),

            # Wave 6: reinforcement wave, moderate count but delayed spawns.
            SpawnWave(
                trigger_x=7100,
                spawners=[
                    EnemySpawner(
                        7600,
                        600,
                        "normal",
                        3,
                        120
                    ),
                    EnemySpawner(
                        7900,
                        640,
                        "fast",
                        2,
                        180
                    )
                ]
            ),

            # Wave 7: boss finale, far enough after reinforcements to recover.
            BossWave(8600)
        ]

    def get_current_wave(self):
        if self.current_wave >= len(self.waves):
            return None

        return self.waves[self.current_wave]
    
    def draw_props(self, screen, camera_x, layer):
        for prop in self.props:
            if prop.layer == layer:
                prop.draw(screen, camera_x)
