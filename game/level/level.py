from game.settings import *
from game.level.background import Background
from game.level.prop import Prop
from game.level.wave import *
from game.level.spawner import EnemySpawner

# background image, far layer, ground layer foreground layer
class Level:
    def __init__(self, stage_data):
        self.stage_id = stage_data["id"]
        self.stage_name = stage_data["name"]
        self.world_width = stage_data["world_width"]
        self.world_height = stage_data["world_height"]
        self.lane_top = stage_data["lane_top"]
        self.lane_bottom = stage_data["lane_bottom"]
        self.background = Background(stage_data["background"])
        
        self.e1s1_wave1_x = stage_data["wave_positions"][0]
        self.e1s1_wave2_x = stage_data["wave_positions"][1]
        self.e1s1_wave3_x = stage_data["wave_positions"][2]

        self.e1s2_wave1_x = stage_data["wave_positions"][0]
        self.e1s2_wave2_x = stage_data["wave_positions"][1]
        
        #self.background = Background(
        #    "game/assets/backgrounds/stage1/stage1_far.png",
        #    "game/assets/backgrounds/stage1/stage1_mid.png",
        #    "game/assets/backgrounds/stage1/stage1_front.png")

        #self.wave1_x = STAGE1_WAVE1_X
        #self.wave2_x = STAGE1_WAVE2_X
        #self.wave3_x = STAGE1_WAVE3_X
        
        self.prop1_x = self.e1s1_wave1_x -100
        self.prop2_x = self.e1s1_wave2_x -100
        self.prop3_x = self.e1s1_wave3_x -100
        self.prop4_x = self.e1s2_wave1_x -100
        self.prop5_x = self.e1s2_wave2_x -100
        
        # front ui decorations
        self.props = [
                Prop(
                    self.prop1_x,
                    LANE_BOTTOM,
                    "game/assets/props/car_wreck.png",
                    layer="back",
                    scale=1.5
                ),

                Prop(
                    self.prop2_x,
                    LANE_BOTTOM,
                    "game/assets/props/dino_bones.png",
                    layer="back",
                    scale=1.5
                ),

                Prop(
                    self.prop3_x,
                    LANE_BOTTOM,
                    "game/assets/props/barrel_green.png",
                    layer="front",
                    scale=1.3
                ),

                Prop(
                    self.prop4_x,
                    LANE_BOTTOM,
                    "game/assets/props/barrel_red.png",
                    layer="front",
                    scale=1.3
                ),

                Prop(
                    self.prop5_x,
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
            Wave(trigger_x=self.e1s1_wave1_x,
                enemy_types=["normal","normal""normal"]),
            Wave(trigger_x=self.e1s1_wave2_x,
                enemy_types=["normal","normal","fast"]),
            SpawnWave(
                trigger_x=self.e1s1_wave3_x,
                spawners=[EnemySpawner(self.e1s1_wave3_x, LANE_BOTTOM, "normal" ,3, 120),
                    EnemySpawner(self.e1s1_wave3_x, LANE_BOTTOM, "fast", 2, 180)]),

            Wave(trigger_x=self.e1s2_wave1_x,
                enemy_types=["normal", "normal", "fast", "heavy", "raptor"]),
            BossWave(self.e1s2_wave2_x)
        ]

    def get_current_wave(self):
        if self.current_wave >= len(self.waves):
            return None

        return self.waves[self.current_wave]
    
    def draw_props(self, screen, camera_x, layer):
        for prop in self.props:
            if prop.layer == layer:
                prop.draw(screen, camera_x)
