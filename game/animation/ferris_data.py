# frame_rect format: (x, y, width, height) -  x, y is the left top location in the png file
# offset format: (x, y) - x, y  = (0,0) - (feet_center_x, feet_center_y)
# hurt_rect format: (x, y, width, height) -   x, y is relative position inside the current frame
# attack_rect format: (x, y, width, height) - x, y is relative position inside the current frame
FERRIS_ANIMATIONS = {
    "idle": {
        "file": "assets/enemies/ferris_idle.png",
        "frames_count": 3,
        "frames": [
            {
                "frame_rect": (0, 0, 61, 75),
                "offset": (-30, -75),
                "hurt_rect": (7, 0, 43, 75),
                "attack_rect": None
            },
            {
                "frame_rect": (61, 0, 61, 75),
                "offset": (-30, -75),
                "hurt_rect": (7, 0, 43, 75),
                "attack_rect": None
            },
            {
                "frame_rect": (122, 0, 61, 75),
                "offset": (-30, -75),
                "hurt_rect": (7, 0, 43, 75),
                "attack_rect": None
            }
        ]
    },
    "walk": {
        "file": "assets/enemies/ferris_walk.png",
        "frames_count": 3,
        "frames": [
            {
                "frame_rect": (0, 0, 51, 81),
                "offset": (-21, -81),
                "hurt_rect": (7, 0, 43, 81),
                "attack_rect": None
            },
            {
                "frame_rect": (51, 0, 50, 81),
                "offset": (-21, -81),
                "hurt_rect": (7, 0, 43, 81),
                "attack_rect": None
            },
            {
                "frame_rect": (101, 0, 58, 81),
                "offset": (-24, -81),
                "hurt_rect": (7, 0, 43, 81),
                "attack_rect": None
            }
        ]
    },
    "attack": {
        "file": "assets/enemies/ferris_attack.png",
        "frames_count": 3,
        "frames": [
            {
                "frame_rect": (0, 0, 61, 78),
                "offset": (-30, -78),
                "hurt_rect": (15, 0, 43, 78),
                "attack_rect": None
            },
            {
                "frame_rect": (51, 0, 58, 78),
                "offset": (-30, -78),
                "hurt_rect": (21, 0, 43, 78),
                "attack_rect": None
            },
            {
                "frame_rect": (101, 0, 96, 78),
                "offset": (-30, -78),
                "hurt_rect": (25, 0, 43, 78),
                "attack_rect": None
            }
        ]
    },
}