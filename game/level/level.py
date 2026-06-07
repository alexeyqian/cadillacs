from game.settings import *
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
                    SCREEN_WIDTH-100,
                    LANE_BOTTOM,
                    "game/assets/props/car_wreck.png",
                    layer="back",
                    scale=1.5
                ),

                Prop(
                    (SCREEN_WIDTH-100)*2,
                    LANE_BOTTOM,
                    "game/assets/props/dino_bones.png",
                    layer="back",
                    scale=1.5
                ),

                Prop(
                    (SCREEN_WIDTH-100)*3,
                    LANE_BOTTOM,
                    "game/assets/props/barrel_green.png",
                    layer="front",
                    scale=1.3
                ),

                Prop(
                    (SCREEN_WIDTH-100)*4,
                    LANE_BOTTOM,
                    "game/assets/props/barrel_red.png",
                    layer="front",
                    scale=1.3
                ),

                Prop(
                    (SCREEN_WIDTH-100)*5,
                    LANE_BOTTOM,
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
                trigger_x=SCREEN_WIDTH-10,
                enemy_types=[
                    "normal",
                    "normal"
                ]
            ),

            # Wave 2: one fast enemy adds pressure without overwhelming.
            Wave(
                trigger_x=(SCREEN_WIDTH-10)*2,
                enemy_types=[
                    "normal",
                    "fast"
                ]
            ),

            # Wave 3: first medium mixed group.
            Wave(
                trigger_x=(SCREEN_WIDTH-10)*3,
                enemy_types=[
                    "normal",
                    "normal",
                    "fast"
                ]
            ),

            # Wave 4: introduce heavy enemy with only light support.
            Wave(
                trigger_x=(SCREEN_WIDTH-10)*4,
                enemy_types=[
                    "heavy",
                    "normal"
                ]
            ),

            # Wave 5: introduce dinosaurs after the player has seen heavy enemies.
            Wave(
                trigger_x=(SCREEN_WIDTH-10)*5,
                enemy_types=[
                    "raptor",
                    "normal",
                    "fast"
                ]
            ),

            # Wave 6: reinforcement wave, moderate count but delayed spawns.
            SpawnWave(
                trigger_x=(SCREEN_WIDTH-10)*6,
                spawners=[
                    EnemySpawner(
                        (SCREEN_WIDTH-10)*6,
                        LANE_BOTTOM,
                        "normal",
                        3,
                        120
                    ),
                    EnemySpawner(
                        (SCREEN_WIDTH-10)*6+20,
                        LANE_BOTTOM,
                        "fast",
                        2,
                        180
                    )
                ]
            ),

            # Wave 7: boss finale, far enough after reinforcements to recover.
            BossWave((SCREEN_WIDTH-10)*7)
        ]

    def get_current_wave(self):
        if self.current_wave >= len(self.waves):
            return None

        return self.waves[self.current_wave]
    
    def draw_props(self, screen, camera_x, layer):
        for prop in self.props:
            if prop.layer == layer:
                prop.draw(screen, camera_x)
