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
                "trigger_x": 2700,
                "spawners": [
                    {
                        "enemy_type": "normal",
                        "x": 2700,
                        "y": 760,
                        "total_count": 3,
                        "spawn_delay": 120,
                    },
                    {
                        "enemy_type": "fast",
                        "x": 2760,
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
            {"type": "pistol", "x": 2650, "y": 980},
        ],

        "objects": [
            {"kind": "breakable", "x": 880, "y": 1030},
            {"kind": "breakable", "x": 1780, "y": 1030},
            {"kind": "barrel", "x": 1740, "y": 1030},
            {"kind": "breakable", "x": 2680, "y": 1030},
        ],
        "completion": "clear_waves_then_exit",
        # Stage 1 rooftop, exit near far right door/edge
        "exit_rect": (3150, 470, 160, 360)
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
                "trigger_x": 2700,
                "spawners": [
                    {
                        "enemy_type": "normal",
                        "x": 2700,
                        "y": 760,
                        "total_count": 3,
                        "spawn_delay": 120,
                    },
                    {
                        "enemy_type": "fast",
                        "x": 2760,
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
            {"type": "pistol", "x": 2650, "y": 980},
        ],

        "objects": [
            {"kind": "breakable", "x": 880, "y": 1030},
            {"kind": "breakable", "x": 1780, "y": 1030},
            {"kind": "barrel", "x": 1740, "y": 1030},
            {"kind": "breakable", "x": 2680, "y": 1030},
        ],
        "completion": "clear_waves_then_exit",
        # Stage 2 hallway, exit near right staircase/edge
        "exit_rect": (2950, 650, 150, 260)
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
        "waves": [],
        "weapons": [],
        "objects": [],
        "completion": "reach_exit",
        # Stage 3 transition, exit near right edge
        "exit_rect": (520, 760, 120, 180),
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
                "trigger_x": 2700,
            },
        ],

        "weapons": [
            {"type": "knife", "x": 850, "y": 980},
            {"type": "bat", "x": 1750, "y": 980},
            {"type": "pistol", "x": 2650, "y": 980},
        ],

        "objects": [
            {"kind": "breakable", "x": 880, "y": 1030},
            {"kind": "breakable", "x": 1780, "y": 1030},
            {"kind": "barrel", "x": 1740, "y": 1030},
            {"kind": "breakable", "x": 2680, "y": 1030},
        ],
            "completion": "clear_waves_then_exit",
            # Stage 4 arena, exit near far right after boss
            "exit_rect": (2920, 620, 140, 300),
        },
]