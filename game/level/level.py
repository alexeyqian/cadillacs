from game.level.lane import LaneSystem
from game.level.background import Background
from game.level.wave import BossWave, SpawnInstruction, Wave
from game.managers.asset_manager import AssetManager


class Level:
    def __init__(self, stage_data):
        # Identity / geometry
        self.stage_id = stage_data["id"]
        self.stage_name = stage_data["name"]
        self.world_width = stage_data["world_width"]
        self.world_height = stage_data["world_height"]
        self.exit_rect = stage_data["exit_rect"]
        self.completion = stage_data["completion"]

        # Lane system (lane_top/bottom kept for direct access by wave spawning)
        self.lane_top = stage_data["lane_top"]
        self.lane_bottom = stage_data["lane_bottom"]
        self.lane_system = LaneSystem(self.lane_top, self.lane_bottom)

        # Presentation
        self.background = Background(stage_data["background"])

        # Water wading: world-x where water begins, plus the splash tile
        self.water_zone_start_x = stage_data.get("water_zone_start_x")
        self.water_zone_end_x = stage_data.get("water_zone_end_x")
        splash_path = stage_data.get("water_splash")
        self.water_splash = AssetManager.load_image(splash_path, alpha=True) if splash_path else None

        # Wave state
        self.current_wave = 0
        self.camera_locked = False
        self.lock_x = None
        self.waves = self._build_waves(stage_data["waves"])

    # --- Lane queries ---

    def get_lane_index(self, y):
        return self.lane_system.get_lane_index(y)

    def get_lane_center(self, lane_index):
        return self.lane_system.get_lane_center(lane_index)

    def get_lane_distance(self, y_a, y_b):
        return self.lane_system.get_lane_distance(y_a, y_b)

    def get_lane_bounds(self, lane_index):
        return self.lane_system.get_lane_bounds(lane_index)

    # --- Wave queries ---

    def get_current_wave(self):
        if self.current_wave >= len(self.waves):
            return None
        return self.waves[self.current_wave]

    # --- Private ---

    def _build_waves(self, wave_configs):
        waves = []
        for wave_config in wave_configs:
            if wave_config.get("kind") == "boss":
                waves.append(BossWave(trigger_x=wave_config["trigger_x"]))
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
                        enter_offset=spawn_config.get("enter_offset", -100),
                        min_player_distance=spawn_config.get("min_player_distance", 360),
                        capability_overrides=spawn_config.get("capability_overrides"),
                    ))

            waves.append(Wave(
                trigger_x=wave_config["trigger_x"],
                spawn_instructions=spawn_instructions,
                max_active=wave_config.get("max_active", 4),
            ))
        return waves
