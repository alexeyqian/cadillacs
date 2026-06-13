from game.settings import *
from game.level.background import Background
from game.level.prop import Prop
from game.level.wave import *

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
        self.wave_configs = stage_data["waves"]
        self.exit_rect = stage_data["exit_rect"]
        self.completion = stage_data["completion"]

        self.current_wave = 0
        # used by wave battles
        self.camera_locked = False
        self.lock_x = None

        self.waves = []

        for wave_config in self.wave_configs:
            kind = wave_config.get("kind")

            if kind == "boss":
                self.waves.append(BossWave(
                    trigger_x=wave_config["trigger_x"]
                ))
                continue

            spawn_instructions = []

            for spawn_config in wave_config["spawns"]:
                count = spawn_config.get("count", 1)

                for _ in range(count):
                    spawn_instructions.append(SpawnInstruction(
                        enemy_type=spawn_config["enemy_type"],
                        side=spawn_config.get("side", "right"),
                        delay_min=spawn_config.get("delay_min", 60),
                        delay_max=spawn_config.get("delay_max", 120),
                        y_min=spawn_config.get("y_min"),
                        y_max=spawn_config.get("y_max"),
                        enter_offset=spawn_config.get("enter_offset", 80),
                        min_player_distance=spawn_config.get("min_player_distance", 360),
                    ))

            self.waves.append(Wave(
                trigger_x=wave_config["trigger_x"],
                spawn_instructions=spawn_instructions,
                max_active=wave_config.get("max_active", 4),
            ))


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
