EPISODE_1_STAGES = [
    {
        "id": "episode_1_stage_1_rooftop",
        "name": "Rooftop Approach",
        "background": "assets/backgrounds/episode_1/episode_1_stage_1_rooftop.png",
        "world_width": 3338,
        "world_height": 1080,
        "player_start": (160, 620),
        "lane_top": 520,
        "lane_bottom": 830,
        "waves": [
            {
                "trigger_x": 1000,
                "max_active": 3,
                "spawns": [
                    {
                        "enemy_type": "ferris",
                        "count": 2
                    }
                ],
            },
            {
                "trigger_x": 2000,
                "max_active": 4,
                "spawns": [
                    {
                        "enemy_type": "ferris",
                        "count": 2
                    },
                    {
                        "enemy_type": "gneiss",
                        "side": "left",
                        "count": 2
                    }
                ],
            },
            {
                "trigger_x": 3000,
                "max_active": 4,
                "spawns": [
                    {
                        "enemy_type": "gneiss",
                        "count": 2
                    },
                    {
                        "enemy_type": "black_elmer",
                        "side": "left",
                        "count": 1
                    },
                ],
            },
        ],
        "weapons": [
            #{"type": "knife", "x": 850, "y": 500},
            #{"type": "bat", "x": 1750, "y": 500},
            #{"type": "pistol", "x": 2260, "y": 500},
        ],
        "objects": [
            # for wave 2
            {"kind": "breakable", "x": 2000, "y": 500, "loot_type":"health"},
            # for wave 3
            {"kind": "breakable", "x": 3000, "y": 500, "loot_type":"health"},
            #{"kind": "barrel", "x": 1740, "y": 760},
        ],
        "completion": "clear_waves_then_exit",
        "exit_rect": (2700, 340, 100, 260),
    },
    {
        "id": "episode_1_stage_2_hallway",
        "name": "Mansion Hallway",
        "background": "assets/backgrounds/episode_1/episode_1_stage_2_hallway.png",
        "world_width": 3132,
        "world_height": 1080,
        "player_start": (160, 720),
        "lane_top": 650,
        "lane_bottom": 1080,
        "waves": [
            {
                "trigger_x": 1000,
                "max_active": 4,
                "spawns": [
                    {
                        "enemy_type": "ferris",
                        "count": 2
                    },
                ],
            },
            {
                "trigger_x": 2000,
                "max_active": 4,
                "spawns": [
                    {
                        "enemy_type": "gneiss",
                        "count": 3
                    },
                ],
            },
            {
                "trigger_x": 2800,
                "max_active": 4,
                "spawns": [
                    {
                        "enemy_type": "gneiss",
                        "count": 2
                    },
                    {
                        "enemy_type": "black_elmer",
                        "count": 2
                    },
                ],
            },
        ],
        "weapons": [
            #{"type": "knife", "x": 850, "y": 760},
            #{"type": "bat", "x": 1750, "y": 760},
            #{"type": "pistol", "x": 2220, "y": 760},
        ],
        "objects": [
            {"kind": "breakable", "x": 1800, "y": 800, "loot_type":"health"},
            {"kind": "breakable", "x": 2500, "y": 800, "loot_type":"health"},
        ],
        "completion": "clear_waves_then_exit",
        "exit_rect": (2800, 650, 150, 420),
    },
    #{
    #    "id": "episode_1_stage_3_transition",
    #    "name": "Ruined Building",
    #    "background": "assets/backgrounds/episode_1/episode_1_stage_3_transition.png",
    #    "world_width": 652,
    #    "world_height": 1080,
    #    "player_start": (120, 790),
    #    "lane_top": 760,
    #    "lane_bottom": 1080,
    #    "waves": [],
    #    "weapons": [],
    #    "objects": [],
    #    "completion": "reach_exit",
    #    "exit_rect": (900, 760, 120, 320),
    #},
    {
        "id": "episode_1_stage_4_ruined_arena",
        "name": "Ruined Arena",
        "background": "assets/backgrounds/episode_1/episode_1_stage_4_ruined_arena.png",
        "world_width": 3086,
        "world_height": 1080,
        "player_start": (160, 720),
        "lane_top": 620,
        "lane_bottom": 1080,
        "waves": [
            {
                "trigger_x": 1000,
                "max_active": 3,
                "spawns": [
                    {
                        "enemy_type": "gneiss",
                        "count": 3
                    },
                ],
            },
            {
                "trigger_x": 2000,
                "max_active": 3,
                "spawns": [
                    {
                        "enemy_type": "gneiss",
                        "count": 3
                    },
                ],
            },
            {
                "kind": "boss",
                "trigger_x": 2800,
            },
        ],
        "weapons": [
        ],
        "objects": [
            {"kind": "breakable", "x": 1800, "y": 800, "loot_type":"health"},
            {"kind": "breakable", "x": 2800, "y": 800, "loot_type":"health"},
        ],
        "completion": "clear_waves_then_exit",
        "exit_rect": (2500, 620, 140, 460),
    },
]
