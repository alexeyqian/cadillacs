from game.level.lane import LaneSystem
from game.level.background import Background
from game.level.wave import BossWave, SpawnInstruction, Wave


# background image, far layer, ground layer foreground layer
class Level:
    def __init__(self, stage_data):
        self.stage_id = stage_data["id"]
        self.stage_name = stage_data["name"]
        self.world_width = stage_data["world_width"]
        self.world_height = stage_data["world_height"]
        self.lane_top = stage_data["lane_top"]
        self.lane_bottom = stage_data["lane_bottom"]
        self.lane_system = LaneSystem(self.lane_top, self.lane_bottom)
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

    def get_lane_index(self, y):
        return self.lane_system.get_lane_index(y)

    def get_lane_center(self, lane_index):
        return self.lane_system.get_lane_center(lane_index)

    def get_lane_distance(self, y_a, y_b):
        return self.lane_system.get_lane_distance(y_a, y_b)

    def get_lane_bounds(self, lane_index):
        return self.lane_system.get_lane_bounds(lane_index)

    def get_current_wave(self):
        if self.current_wave >= len(self.waves):
            return None

        return self.waves[self.current_wave]

    #def draw_props(self, screen, camera_x, layer):
    #    for prop in self.props:
    #        if prop.layer == layer:
    #            prop.draw(screen, camera_x)
