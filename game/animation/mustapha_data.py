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
                "frame_rect": (0, 0, 98, 178),
                "offset": (-50, -178),
                "hurt_rect": (30, 10, 4, 110),
                "attack_rect": None
            },
            {
                "frame_rect": (98, 0, 98, 178),
                "offset": (-50, -178),
                "hurt_rect": (30, 10, 45, 110),
                "attack_rect": None
            },
            {
                "frame_rect": (196, 0, 120, 178),
                "offset": (-50, -178),
                "hurt_rect": (30, 10, 45, 110),
                "attack_rect": None
            },
            {
                "frame_rect": (316, 0, 120, 178),
                "offset": (-50, -178),
                "hurt_rect": (30, 10, 45, 110),
                "attack_rect": None
            },
            {
                "frame_rect": (436, 0, 120, 178),
                "offset": (-50, -178),
                "hurt_rect": (30, 10, 45, 110),
                "attack_rect": None
            },
            {
                "frame_rect": (556, 0, 120, 178),
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
    "attack": {
        "file": "assets/player/mustapha_attack.png",
        "frames_count": 2,
        "frames": [
            {
                "frame_rect": (0, 0, 111, 168),
                "offset": (-60, -168),
                "hurt_rect": (40, 0, 45, 110),
                "attack_rect": None
            },
            {
                "frame_rect": (111, 0, 193, 168),
                "offset": (-110, -168),
                "hurt_rect": (116, 0, 45, 110),
                "attack_rect": (140, 20, 50, 20)
            }
        ]
    }
}
