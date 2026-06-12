# frame_rec format: (x, y, width, height) -  x, y is the left top location in the png file
# offset format: (x, y) - x, y  = (0,0) - (feet_center_x, feet_center_y)
# hurt_rec format: (x, y, width, height) -   x, y is relative position inside the current frame
# attack_rec format: (x, y, width, height) - x, y is relative position inside the current frame
MUSTAPHA_ANIMATIONS = {
    "idle": {
        "file": "assets/player/mustapha_idle.png",
        "frames_count": 6,
        "frames": [
            {
                "frame_rec": (0, 0, 98, 178),
                "offset": (-50, -178),
                "hurt_rec": (30, 10, 4, 110),
                "attack_rec": None
            },
            {
                "frame_rec": (98, 0, 98, 178),
                "offset": (-50, -178),
                "hurt_rec": (30, 10, 45, 110),
                "attack_rec": None
            },
            {
                "frame_rec": (196, 0, 120, 178),
                "offset": (-50, -178),
                "hurt_rec": (30, 10, 45, 110),
                "attack_rec": None
            },
            {
                "frame_rec": (316, 0, 120, 178),
                "offset": (-50, -178),
                "hurt_rec": (30, 10, 45, 110),
                "attack_rec": None
            },
            {
                "frame_rec": (436, 0, 120, 178),
                "offset": (-50, -178),
                "hurt_rec": (30, 10, 45, 110),
                "attack_rec": None
            },
            {
                "frame_rec": (556, 0, 120, 178),
                "offset": (-50, -178),
                "hurt_rec": (30, 10, 45, 110),
                "attack_rec": None
            }
        ]
    },
    "walk": {
        "file": "assets/player/mustapha_walk.png",
        "frames_count": 11,
        "frames": [
            {
                "frame_rec": (0,0,54,170),
                "offset": (-25, -170),
                "hurt_rect": (10, 0, 45, 110),
                "attack_rec": None
            },
            {
                "frame_rec": (54,0,56,170),
                "offset": (-25, -170),
                "hurt_rect": (10, 0, 45, 110),
                "attack_rec": None
            },
            {
                "frame_rec": (110,0,116,170),
                "offset": (-170, -170),
                "hurt_rect": (140, 0, 45, 110),
                "attack_rec": None
            },
            {
                "frame_rec": (226,0,94,170),
                "offset": (-50, -170),
                "hurt_rect": (25, 0, 45, 110),
                "attack_rec": None
            },
            {
                "frame_rec": (320,0,80,170),
                "offset": (-45, -170),
                "hurt_rect": (25, 0, 45, 110),
                "attack_rec": None
            },
            {
                "frame_rec": (400,0,54,170),
                "offset": (-25, -170),
                "hurt_rect": (5, 0, 45, 110),
                "attack_rec": None
            },
            {
                "frame_rec": (454,0,60,170),
                "offset": (-30, -170),
                "hurt_rect": (5, 0, 45, 110),
                "attack_rec": None
            },
            {
                "frame_rec": (514,0,95,170),
                "offset": (-45, -170),
                "hurt_rect": (25, 0, 45, 110),
                "attack_rec": None
            },
            {
                "frame_rec": (609,0,114,170),
                "offset": (-55, -170),
                "hurt_rect": (30, 0, 45, 110),
                "attack_rec": None
            },
            {
                "frame_rec": (723,0,92,170),
                "offset": (-40, -170),
                "hurt_rect": (25, 0, 45, 110),
                "attack_rec": None
            },
            {
                "frame_rec": (815,0,68,170),
                "offset": (-30, -170),
                "hurt_rect": (10, 0, 45, 110),
                "attack_rec": None
            },
        ]
    },
    "attack": {
        "file": "assets/player/mustapha_attack.png",
        "frames_count": 2,
        "frames": [
            {
                "frame_rec": (0, 0, 111, 168),
                "offset": (-60, -168),
                "hurt_rec": (40, 0, 45, 110),
                "attack_rec": None
            },
            {
                "frame_rec": (111, 0, 193, 168),
                "offset": (-110, -168),
                "hurt_rec": (116, 0, 45, 110),
                "attack_rec": (200, 20, 50, 20)
            }
        ]
    }
}
