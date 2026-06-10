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
        self.wave_positions = stage_data["wave_positions"]
        self.boss_position = stage_data["boss_position"]

        self.current_wave = 0
        # used by wave battles
        self.camera_locked = False
        self.lock_x = None

        self.waves = []

        if len(self.wave_positions) >= 1:
            self.waves.append(Wave(
                trigger_x=self.wave_positions[0],
                enemy_types=["normal", "normal", "normal"]
            ))

        if len(self.wave_positions) >= 2:
            self.waves.append(Wave(
                trigger_x=self.wave_positions[1],
                enemy_types=["normal", "normal", "fast", "heavy"]
            ))

        if len(self.wave_positions) >= 3:
            self.waves.append(SpawnWave(
                trigger_x=self.wave_positions[2],
                spawners=[
                    EnemySpawner(self.wave_positions[2], self.lane_bottom, "normal", 3, 120),
                    EnemySpawner(self.wave_positions[2], self.lane_bottom, "fast", 2, 180),
                ]
            ))

        if self.boss_position:
            self.waves.append(BossWave(self.boss_position))

        #self.prop1_x = self.e1s1_wave1_x -100
        #self.prop2_x = self.e1s1_wave2_x -100
        #self.prop3_x = self.e1s1_wave3_x -100
        #self.prop4_x = self.e1s2_wave1_x -100
        #self.prop5_x = self.e1s2_wave2_x -100
        
        # front ui decorations
        #self.props = [
        #        Prop(self.prop1_x,LANE_BOTTOM,
        #            "game/assets/props/car_wreck.png",layer="back",scale=1.5),
        #        Prop(self.prop2_x,LANE_BOTTOM,
        #            "game/assets/props/dino_bones.png",layer="back",scale=1.5),
        #        Prop(self.prop3_x,LANE_BOTTOM,
        #            "game/assets/props/barrel_green.png",layer="front",scale=1.3),
        #        Prop(self.prop4_x,LANE_BOTTOM,
        #            "game/assets/props/barrel_red.png",layer="front",scale=1.3),
        #        Prop(self.prop5_x,LANE_BOTTOM,
        #            "game/assets/props/bush.png",layer="front",scale=1.4),]

    def get_current_wave(self):
        if self.current_wave >= len(self.waves):
            return None

        return self.waves[self.current_wave]
    
    #def draw_props(self, screen, camera_x, layer):
    #    for prop in self.props:
    #        if prop.layer == layer:
    #            prop.draw(screen, camera_x)
