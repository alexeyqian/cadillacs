EPISODE_1_STAGES = [
    {
        "id": "episode_1_stage_1_rooftop",
        "name": "Rooftop Approach",
        "background": "assets/backgrounds/episode_1/episode_1_stage_1_rooftop.png",
        "world_width": 3338,
        "world_height": 1080,
        "player_start": (160, 620),
        "lane_top": 470,
        "lane_bottom": 800,
        "walkable_polygon": [
            (0, 520),
            (3338, 470),
            (3338, 800),
            (0, 820),
        ],
        "waves": [
            {
                "kind": "normal",
                "trigger_x": 900,
                "enemy_types": ["normal", "normal", "normal"],
            },
            {
                "kind": "normal",
                "trigger_x": 1800,
                "enemy_types": ["normal", "fast", "heavy"],
            },
            {
                "kind": "spawn",
                "trigger_x": 2300,
                "spawners": [
                    {
                        "enemy_type": "normal",
                        "x": 2380,
                        "y": 760,
                        "total_count": 3,
                        "spawn_delay": 120,
                    },
                    {
                        "enemy_type": "fast",
                        "x": 2460,
                        "y": 760,
                        "total_count": 2,
                        "spawn_delay": 180,
                    },
                ],
            },
        ],

        "weapons": [
            {"type": "knife", "x": 850, "y": 980},
            {"type": "bat", "x": 1750, "y": 980},
            {"type": "pistol", "x": 2260, "y": 980},
        ],

        "objects": [
            {"kind": "breakable", "x": 880, "y": 1030},
            {"kind": "breakable", "x": 1780, "y": 1030},
            {"kind": "barrel", "x": 1740, "y": 1030},
            {"kind": "breakable", "x": 2320, "y": 1030},
        ],
        "completion": "clear_waves_then_exit",
        # Stage 1 rooftop, exit near far right door/edge
        "exit_rect": (3150, 470, 160, 500)
    },
    {
        "id": "episode_1_stage_2_hallway",
        "name": "Mansion Hallway",
        "background": "assets/backgrounds/episode_1/episode_1_stage_2_hallway.png",
        "world_width": 3132,
        "world_height": 1080,
        "player_start": (160, 720),
        "lane_top": 650,
        "lane_bottom": 850,
        "walkable_polygon": [
            (0, 650),
            (3132, 650),
            (3132, 850),
            (0, 850),
        ],
        "waves": [
            {
                "kind": "normal",
                "trigger_x": 900,
                "enemy_types": ["normal", "normal", "normal"],
            },
            {
                "kind": "normal",
                "trigger_x": 1800,
                "enemy_types": ["normal", "fast", "heavy"],
            },
            {
                "kind": "spawn",
                "trigger_x": 2250,
                "spawners": [
                    {
                        "enemy_type": "normal",
                        "x": 2320,
                        "y": 760,
                        "total_count": 3,
                        "spawn_delay": 120,
                    },
                    {
                        "enemy_type": "fast",
                        "x": 2400,
                        "y": 760,
                        "total_count": 2,
                        "spawn_delay": 180,
                    },
                ],
            },
        ],

        "weapons": [
            {"type": "knife", "x": 850, "y": 980},
            {"type": "bat", "x": 1750, "y": 980},
            {"type": "pistol", "x": 2220, "y": 980},
        ],

        "objects": [
            {"kind": "breakable", "x": 880, "y": 1030},
            {"kind": "breakable", "x": 1780, "y": 1030},
            {"kind": "barrel", "x": 1740, "y": 1030},
            {"kind": "breakable", "x": 2280, "y": 1030},
        ],
        "completion": "clear_waves_then_exit",
        # Stage 2 hallway, exit near right staircase/edge
        "exit_rect": (2950, 650, 150, 420)
    },
    {
        "id": "episode_1_stage_3_transition",
        "name": "Ruined Building",
        "background": "assets/backgrounds/episode_1/episode_1_stage_3_transition.png",
        "world_width": 652,
        "world_height": 1080,
        "player_start": (120, 790),
        "lane_top": 760,
        "lane_bottom": 900,
        "walkable_polygon": [
            (0, 760),
            (652, 760),
            (652, 900),
            (0, 900),
        ],
        "waves": [],
        "weapons": [],
        "objects": [],
        "completion": "reach_exit",
        # Stage 3 transition, exit near right edge
        "exit_rect": (520, 760, 120, 320),
    },
    {
        "id": "episode_1_stage_4_ruined_arena",
        "name": "Ruined Arena",
        "background": "assets/backgrounds/episode_1/episode_1_stage_4_ruined_arena.png",
        "world_width": 3086,
        "world_height": 1080,
        "player_start": (160, 720),
        "lane_top": 620,
        "lane_bottom": 900,
        "walkable_polygon": [
            (0, 650),
            (3086, 620),
            (3086, 900),
            (0, 900),
        ],
        "waves": [
            {
                "kind": "normal",
                "trigger_x": 900,
                "enemy_types": ["normal", "fast", "normal"],
            },
            {
                "kind": "normal",
                "trigger_x": 1700,
                "enemy_types": ["heavy", "fast", "raptor"],
            },
            {
                "kind": "boss",
                "trigger_x": 2250,
            },
        ],

        "weapons": [
            {"type": "knife", "x": 850, "y": 980},
            {"type": "bat", "x": 1750, "y": 980},
            {"type": "pistol", "x": 2220, "y": 980},
        ],

        "objects": [
            {"kind": "breakable", "x": 880, "y": 1030},
            {"kind": "breakable", "x": 1780, "y": 1030},
            {"kind": "barrel", "x": 1740, "y": 1030},
            {"kind": "breakable", "x": 2280, "y": 1030},
        ],
        "completion": "clear_waves_then_exit",
        # Stage 4 arena, exit near far right after boss
        "exit_rect": (2920, 620, 140, 460),
    },
]
