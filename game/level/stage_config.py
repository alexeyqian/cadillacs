EPISODE_1_STAGES = [
    {
        "id": "episode_1_stage_1_rooftop",
        "name": "Rooftop Approach",
        "background": "assets/backgrounds/episode_1/episode_1_stage_1_rooftop.png",
        "world_width": 3338,
        "world_height": 1080,
        "player_start": (160, 620),
        "lane_top": 520,
        "lane_bottom": 820,
        "waves": [
            {
                "kind": "normal",
                "trigger_x": 900,
                "enemy_types": ["ferris", "ferris", "ferris"],
            },
            {
                "kind": "normal",
                "trigger_x": 1800,
                "enemy_types": ["ferris", "gneiss", "black_elmer"],
            },
            {
                "kind": "spawn",
                "trigger_x": 2700,
                "spawners": [
                    {
                        "enemy_type": "gneiss",
                        "x": 2780,
                        "y": 760,
                        "total_count": 3,
                        "spawn_delay": 120,
                    },
                    {
                        "enemy_type": "black_elmer",
                        "x": 2760,
                        "y": 760,
                        "total_count": 2,
                        "spawn_delay": 180,
                    },
                ],
            },
        ],

        "weapons": [
            {"type": "knife", "x": 850, "y": 760},
            {"type": "bat", "x": 1750, "y": 760},
            {"type": "pistol", "x": 2260, "y": 760},
        ],

        "objects": [
            {"kind": "breakable", "x": 880, "y": 760},
            {"kind": "breakable", "x": 1780, "y": 760},
            {"kind": "barrel", "x": 1740, "y": 760},
            {"kind": "breakable", "x": 2320, "y": 760},
        ],
        "completion": "clear_waves_then_exit",
        # Stage 1 rooftop, exit near far right door/edge
        "exit_rect": (2700, 340, 100, 260)
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
                "kind": "ferris",
                "trigger_x": 900,
                "enemy_types": ["ferris", "ferris", "ferris"],
            },
            {
                "kind": "normal",
                "trigger_x": 1800,
                "enemy_types": ["ferris", "gneiss", "gneiss"],
            },
            {
                "kind": "spawn",
                "trigger_x": 2250,
                "spawners": [
                    {
                        "enemy_type": "ferris",
                        "x": 2320,
                        "y": 760,
                        "total_count": 3,
                        "spawn_delay": 120,
                    },
                    {
                        "enemy_type": "black_elmer",
                        "x": 2400,
                        "y": 760,
                        "total_count": 2,
                        "spawn_delay": 180,
                    },
                ],
            },
        ],

        "weapons": [
            {"type": "knife", "x": 850, "y": 760},
            {"type": "bat", "x": 1750, "y": 760},
            {"type": "pistol", "x": 2220, "y": 760},
        ],

        "objects": [
            {"kind": "breakable", "x": 880, "y": 760},
            {"kind": "breakable", "x": 1780, "y": 760},
            {"kind": "barrel", "x": 1740, "y": 760},
            {"kind": "breakable", "x": 2280, "y": 760},
        ],
        "completion": "clear_waves_then_exit",
        # Stage 2 hallway, exit near right staircase/edge
        "exit_rect": (2800, 650, 150, 420)
    },
    {
        "id": "episode_1_stage_3_transition",
        "name": "Ruined Building",
        "background": "assets/backgrounds/episode_1/episode_1_stage_3_transition.png",
        "world_width": 652,
        "world_height": 1080,
        "player_start": (120, 790),
        "lane_top": 760,
        "lane_bottom": 1080,
        "waves": [],
        "weapons": [],
        "objects": [],
        "completion": "reach_exit",
        # Stage 3 transition, exit near right edge
        "exit_rect": (900, 760, 120, 320),
    },
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
                "kind": "normal",
                "trigger_x": 900,
                "enemy_types": ["ferris", "ferris", "ferris"],
            },
            {
                "kind": "normal",
                "trigger_x": 1700,
                "enemy_types": ["gneiss", "gneiss", "black_elmer"],
            },
            {
                "kind": "boss",
                "trigger_x": 2250,
            },
        ],

        "weapons": [
            {"type": "knife", "x": 850, "y": 760},
            {"type": "bat", "x": 1750, "y": 760},
            {"type": "pistol", "x": 2220, "y": 760},
        ],

        "objects": [
            {"kind": "breakable", "x": 880, "y": 760},
            {"kind": "breakable", "x": 1780, "y": 760},
            {"kind": "barrel", "x": 1740, "y": 760},
            {"kind": "breakable", "x": 2280, "y": 760},
        ],
        "completion": "clear_waves_then_exit",
        # Stage 4 arena, exit near far right after boss
        "exit_rect": (2500, 620, 140, 460),
    },
]
