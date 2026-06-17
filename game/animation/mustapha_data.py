# frame_rect format: (x, y, width, height) -  x, y is the left top location in the png file
# offset format: (x, y) - x, y  = (0,0) - (feet_center_x, feet_center_y)
# hurt_rect format: (x, y, width, height) -   x, y is relative position inside the current frame
# attack_rect format: (x, y, width, height) - x, y is relative position inside the current frame
MUSTAPHA_ANIMATIONS = {
    "idle": {
        "file": "assets/player/mustapha_idle.png",
        "frames_count": 6,
        "frames": [
            {
                "frame_rect": (0, 0, 94, 178),
                "offset": (-50, -178),
                "hurt_rect": (30, 10, 4, 110),
                "attack_rect": None
            },
            {
                "frame_rect": (94, 0, 96, 178),
                "offset": (-50, -178),
                "hurt_rect": (30, 10, 45, 110),
                "attack_rect": None
            },
            {
                "frame_rect": (190, 0, 119, 178),
                "offset": (-50, -178),
                "hurt_rect": (30, 10, 45, 110),
                "attack_rect": None
            },
            {
                "frame_rect": (309, 0, 120, 178),
                "offset": (-50, -178),
                "hurt_rect": (30, 10, 45, 110),
                "attack_rect": None
            },
            {
                "frame_rect": (429, 0, 119, 178),
                "offset": (-50, -178),
                "hurt_rect": (30, 10, 45, 110),
                "attack_rect": None
            },
            {
                "frame_rect": (548, 0, 98, 178),
                "offset": (-50, -178),
                "hurt_rect": (30, 10, 45, 110),
                "attack_rect": None
            }
        ]
    },
    "walk": {
        "file": "assets/player/mustapha_walk.png",
        "frames_count": 11,
        "frames": [
            {
                "frame_rect": (0,0,54,170),
                "offset": (-25, -170),
                "hurt_rect": (10, 0, 45, 110),
                "attack_rect": None
            },
            {
                "frame_rect": (54,0,56,170),
                "offset": (-25, -170),
                "hurt_rect": (10, 0, 45, 110),
                "attack_rect": None
            },
            {
                "frame_rect": (110,0,116,170),
                "offset": (-70, -170),
                "hurt_rect": (40, 0, 45, 110),
                "attack_rect": None
            },
            {
                "frame_rect": (226,0,94,170),
                "offset": (-50, -170),
                "hurt_rect": (25, 0, 45, 110),
                "attack_rect": None
            },
            {
                "frame_rect": (320,0,80,170),
                "offset": (-45, -170),
                "hurt_rect": (25, 0, 45, 110),
                "attack_rect": None
            },
            {
                "frame_rect": (400,0,54,170),
                "offset": (-25, -170),
                "hurt_rect": (5, 0, 45, 110),
                "attack_rect": None
            },
            {
                "frame_rect": (454,0,60,170),
                "offset": (-30, -170),
                "hurt_rect": (5, 0, 45, 110),
                "attack_rect": None
            },
            {
                "frame_rect": (514,0,95,170),
                "offset": (-45, -170),
                "hurt_rect": (25, 0, 45, 110),
                "attack_rect": None
            },
            {
                "frame_rect": (609,0,114,170),
                "offset": (-55, -170),
                "hurt_rect": (30, 0, 45, 110),
                "attack_rect": None
            },
            {
                "frame_rect": (723,0,92,170),
                "offset": (-40, -170),
                "hurt_rect": (25, 0, 45, 110),
                "attack_rect": None
            },
            {
                "frame_rect": (815,0,68,170),
                "offset": (-30, -170),
                "hurt_rect": (10, 0, 45, 110),
                "attack_rect": None
            },
        ]
    },
    "run": {
        "file": "assets/player/mustapha_run.png",
        "frames_count": 9,
        "frames": [
            {
                "frame_rect": (0, 0, 142, 153),
                "offset": (-55, -153),
                "hurt_rect": (55, 35, 70, 90),
                "attack_rect": None
            },
            {
                "frame_rect": (142, 0, 180, 153),
                "offset": (-55, -153),
                "hurt_rect": (90, 10, 70, 90),
                "attack_rect": None
            },
            {
                "frame_rect": (322, 0, 140, 153),
                "offset": (-50, -153),
                "hurt_rect": (60, 0, 70, 90),
                "attack_rect": None
            },
            {
                "frame_rect": (462, 0, 148, 153),
                "offset": (-60, -153),
                "hurt_rect": (70, 0, 70, 90),
                "attack_rect": None
            },
            {
                "frame_rect": (610, 0, 156, 153),
                "offset": (-64, -153),
                "hurt_rect": (80, 0, 70, 90),
                "attack_rect": None
            },
            {
                "frame_rect": (766, 0, 142, 153),
                "offset": (-20, -153),
                "hurt_rect": (45, 0, 70, 90),
                "attack_rect": None
            },
            {
                "frame_rect": (908, 0, 159, 153),
                "offset": (-60, -153),
                "hurt_rect": (70, 0, 70, 90),
                "attack_rect": None
            },
            {
                "frame_rect": (1067, 0, 172, 153),
                "offset": (-70, -153),
                "hurt_rect": (80, 0, 70, 90),
                "attack_rect": None
            }
        ]
    },
    "hit": {
        "file": "assets/player/mustapha_hit.png",
        "frames_count": 2,
        "frames": [
            {
                "frame_rect": (0, 0, 120, 160),
                "offset": (-60, -160),
                "hurt_rect": (0, 0, 45, 110),
                "attack_rect": None
            },
            {
                "frame_rect": (120, 0, 126, 160),
                "offset": (-70, -160),
                "hurt_rect": (35, 0, 45, 110),
                "attack_rect": None
            }
        ]
    },
    "dead": {
        "file": "assets/player/mustapha_dead.png",
        "frames_count": 2,
        "frames": [
            {
                "frame_rect": (0, 0, 221, 87),
                "offset": (-100, -87),
                "hurt_rect": (0, 0, 110, 45),
                "attack_rect": None
            },
            {
                "frame_rect": (221, 0, 220, 87),
                "offset": (-100, -87),
                "hurt_rect": (0, 60, 110, 45),
                "attack_rect": None
            }
        ]
    },
    "attack": {
        "file": "assets/player/mustapha_attack.png",
        "frames_count": 3,
        "frames": [
            {
                "frame_rect": (0, 0, 111, 168),
                "offset": (-60, -168),
                "hurt_rect": (40, 0, 45, 110),
                "attack_rect": None
            },
            {
                "frame_rect": (111, 0, 193, 168),
                "offset": (-63, -168),
                "hurt_rect": (40, 0, 45, 110),
                "counter_hurt_rect": (90, 18, 20, 20),
                "attack_rect": (110, 18, 60, 20)
            },
            {
                "frame_rect": (304, 0, 140, 168),
                "offset": (-76, -168),
                "hurt_rect": (56, 0, 45, 110),
                "attack_rect": None
            }
        ]
    },
    "run_attack": {
        "file": "assets/player/mustapha_run_attack.png",
        "frames_count": 2,
        "frames": [
            {
                "frame_rect": (0, 0, 120, 92),
                "offset": (-60, -150),
                "hurt_rect": (0, 0, 120, 92),
                "attack_rect": None
            },
            {
                "frame_rect": (120, 0, 223, 92),
                "offset": (-110, -150),
                "hurt_rect": (0, 20, 110, 45),
                "attack_rect": (130, 40, 80, 40)
            }
        ]
    },
    "jump": {
        "file": "assets/player/mustapha_jump.png",
        "frames_count": 4,
        "frames": [
            {#77,93,96,77
                "frame_rect": (0, 0, 77, 211),
                "offset": (-40, -211),
                "hurt_rect": (40, 0, 45, 110),
                "attack_rect": None
            },
            {
                "frame_rect": (77, 0, 93, 211),
                "offset": (-40, -211),
                "hurt_rect": (0, 0, 45, 90),
                "attack_rect": None
            },
            {
                "frame_rect": (170, 0, 96, 211),
                "offset": (-40, -211),
                "hurt_rect": (0, 0, 45, 50),
                "attack_rect": None
            },
            {
                "frame_rect": (266, 0, 77, 211),
                "offset": (-40, -211),
                "hurt_rect": (0, 0, 45, 90),
                "attack_rect": None
            }
        ]
    },
    "jump_attack": {
        "file": "assets/player/mustapha_run_attack.png",
        "frames_count": 2,
        "frames": [
            {
                "frame_rect": (0, 0, 120, 92),
                "offset": (-60, -150),
                "hurt_rect": (0, 0, 120, 92),
                "attack_rect": None
            },
            {
                "frame_rect": (120, 0, 223, 92),
                "offset": (-110, -150),
                "hurt_rect": (0, 20, 110, 45),
                "attack_rect": (130, 40, 80, 40)
            }
        ]
    },
    "grab": {
        "file": "assets/player/mustapha_grab.png",
        "frames_count": 1,
        "frames": [
            {
                "frame_rect": (0, 0, 123, 162),
                "offset": (-40, -162),
                "hurt_rect": (20, 0, 45, 110),
                "attack_rect": None
            }
        ]
    },
    "throw": {
        "file": "assets/player/mustapha_throw.png",
        "frames_count": 1,
        "frames": [
            {
                "frame_rect": (0, 0, 153, 162),
                "offset": (-40, -162),
                "hurt_rect": (20, 0, 45, 110),
                "attack_rect": None
            }
        ]
    },
    "grab_knee": {
        "file": "assets/player/mustapha_grab_knee.png",
        "frames_count": 2,
        "frames": [
            {
                "frame_rect": (0, 0, 123, 165),
                "offset": (-40, -165),
                "hurt_rect": (0, 0, 45, 110),
                "attack_rect": None
            },
            {
                "frame_rect": (123, 0, 88, 165),
                "offset": (-35, -165),
                "hurt_rect": (0, 10, 45, 110),
                "attack_rect": (60, 70, 30, 30),
            }
        ]
    },
}

MUSTAPHA_ANIMATIONS["attack_1"] = {
    "file": "assets/player/mustapha_attack_1.png",
    "frames_count": 3,
    "frames": [
        {
            "frame_rect": (0, 0, 111, 168),
            "offset": (-60, -168),
            "hurt_rect": (40, 0, 45, 110),
            "attack_rect": None
        },
        {
            "frame_rect": (111, 0, 193, 168),
            "offset": (-63, -168),
            "hurt_rect": (40, 0, 45, 110),
            "counter_hurt_rect": (90, 18, 20, 20),
            "attack_rect": (110, 18, 60, 20)
        },
        {
            "frame_rect": (304, 0, 140, 168),
            "offset": (-76, -168),
            "hurt_rect": (56, 0, 45, 110),
            "attack_rect": None
        }
    ]
}
MUSTAPHA_ANIMATIONS["attack_2"] = {
    "file": "assets/player/mustapha_attack_2.png",
    "frames_count": 3,
    "frames": [
        {
            "frame_rect": (0, 0, 111, 168),
            "offset": (-60, -168),
            "hurt_rect": (40, 0, 45, 110),
            "attack_rect": None
        },
        {
            "frame_rect": (111, 0, 200, 168),
            "offset": (-66, -168),
            "hurt_rect": (42, 0, 45, 110),
            "counter_hurt_rect": (94, 18, 24, 20),
            "attack_rect": (114, 18, 68, 20)
        },
        {
            "frame_rect": (311, 0, 146, 168),
            "offset": (-82, -168),
            "hurt_rect": (62, 0, 45, 110),
            "attack_rect": None
        }
    ]
}
MUSTAPHA_ANIMATIONS["attack_3"] = {
    "file": "assets/player/mustapha_attack_3.png",
    "frames_count": 3,
    "frames": [
        {
            "frame_rect": (0, 0, 118, 168),
            "offset": (-67, -168),
            "hurt_rect": (47, 0, 45, 110),
            "attack_rect": None
        },
        {
            "frame_rect": (118, 0, 214, 168),
            "offset": (-72, -168),
            "hurt_rect": (46, 0, 48, 110),
            "counter_hurt_rect": (100, 18, 28, 24),
            "attack_rect": (122, 18, 78, 24)
        },
        {
            "frame_rect": (332, 0, 154, 168),
            "offset": (-90, -168),
            "hurt_rect": (70, 0, 45, 110),
            "attack_rect": None
        }
    ]
}

MUSTAPHA_ANIM_FPS = {
    "idle": 6,
    "walk": 6,
    "run": 6,
    "jump": 6,
    "attack": 12,
    "attack_1": 12,
    "attack_2": 12,
    "attack_3": 12,
    "run_attack": 6,
    "jump_attack": 6,
    "grab": 6,
    "throw": 6,
    "grab_knee": 6,
    "hit": 6,
    "dead": 999,
}
