# frame_rect format: (x, y, width, height) -  x, y is the left top location in the png file
# offset format: (x, y) - x, y  = (0,0) - (feet_center_x, feet_center_y)
MUSTAPHA_ANIMATIONS = {
    "idle": {
        "file": "assets/player/mustapha_idle.png",
        "frames_count": 6,
        "frames": [
            {
                "frame_rect": (0, 0, 94, 178),
                "offset": (-50, -178),
            },
            {
                "frame_rect": (94, 0, 96, 178),
                "offset": (-50, -178),
            },
            {
                "frame_rect": (190, 0, 119, 178),
                "offset": (-50, -178),
            },
            {
                "frame_rect": (309, 0, 120, 178),
                "offset": (-50, -178),
            },
            {
                "frame_rect": (429, 0, 119, 178),
                "offset": (-50, -178),
            },
            {
                "frame_rect": (548, 0, 98, 178),
                "offset": (-50, -178),
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
            },
            {
                "frame_rect": (54,0,56,170),
                "offset": (-25, -170),
            },
            {
                "frame_rect": (110,0,116,170),
                "offset": (-70, -170),
            },
            {
                "frame_rect": (226,0,94,170),
                "offset": (-50, -170),
            },
            {
                "frame_rect": (320,0,80,170),
                "offset": (-45, -170),
            },
            {
                "frame_rect": (400,0,54,170),
                "offset": (-25, -170),
            },
            {
                "frame_rect": (454,0,60,170),
                "offset": (-30, -170),
            },
            {
                "frame_rect": (514,0,95,170),
                "offset": (-45, -170),
            },
            {
                "frame_rect": (609,0,114,170),
                "offset": (-55, -170),
            },
            {
                "frame_rect": (723,0,92,170),
                "offset": (-40, -170),
            },
            {
                "frame_rect": (815,0,68,170),
                "offset": (-30, -170),
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
            },
            {
                "frame_rect": (142, 0, 180, 153),
                "offset": (-55, -153),
            },
            {
                "frame_rect": (322, 0, 140, 153),
                "offset": (-50, -153),
            },
            {
                "frame_rect": (462, 0, 148, 153),
                "offset": (-60, -153),
            },
            {
                "frame_rect": (610, 0, 158, 153),
                "offset": (-64, -153),
            },
            {
                "frame_rect": (768, 0, 156, 153),
                "offset": (-20, -153),
            },
            {
                "frame_rect": (924, 0, 143, 153),
                "offset": (-60, -153),
            },
            {
                "frame_rect": (1067, 0, 158, 153),
                "offset": (-70, -153),
            },
            {
                "frame_rect": (1225, 0, 172, 153),
                "offset": (-70, -153),
            }
        ]
    },
    "hit": {
        "file": "assets/player/mustapha_hit.png",
        "frames_count": 1,
        "frames": [
            {
                "frame_rect": (0, 0, 126, 160),
                "offset": (-60, -160),
            }
        ]
    },
    "dead": {
        "file": "assets/player/mustapha_dead.png",
        "frames_count": 2,
        "frames": [
            {
                "frame_rect": (0, 0, 210, 87),
                "offset": (-100, -87),
            },
            {
                "frame_rect": (210, 0, 220, 87),
                "offset": (-100, -87),
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
            },
            {
                "frame_rect": (111, 0, 193, 168),
                "offset": (-63, -168),
            },
            {
                "frame_rect": (304, 0, 111, 168),
                "offset": (-76, -168),
            }
        ]
    },
    "run_attack": {
        "file": "assets/player/mustapha_run_attack.png",
        "frames_count": 3,
        "frames": [
            {
                "frame_rect": (0, 0, 120, 92),
                "offset": (-60, -150),
            },
            {
                "frame_rect": (120, 0, 223, 92),
                "offset": (-110, -150),
            },
            {
                "frame_rect": (343, 0, 120, 92),
                "offset": (-60, -150),
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
            },
            {
                "frame_rect": (77, 0, 93, 211),
                "offset": (-40, -211),
            },
            {
                "frame_rect": (170, 0, 96, 211),
                "offset": (-40, -211),
            },
            {
                "frame_rect": (266, 0, 77, 211),
                "offset": (-40, -211),
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
            },
            {
                "frame_rect": (120, 0, 223, 92),
                "offset": (-110, -150),
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
            },
            {
                "frame_rect": (123, 0, 88, 165),
                "offset": (-35, -165),
            }
        ]
    },
}

# todo: use different animation in future
MUSTAPHA_ANIMATIONS["attack_1"] = MUSTAPHA_ANIMATIONS["attack"]
MUSTAPHA_ANIMATIONS["attack_2"] = MUSTAPHA_ANIMATIONS["attack"]
MUSTAPHA_ANIMATIONS["attack_3"] = MUSTAPHA_ANIMATIONS["attack"]

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
