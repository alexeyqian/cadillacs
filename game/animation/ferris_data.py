# frame_rect format: (x, y, width, height) -  x, y is the left top location in the png file
# offset format: (x, y) - x, y  = (0,0) - (feet_center_x, feet_center_y)
FERRIS_ANIMATIONS = {
    "idle": {
        "file": "assets/enemies/ferris_idle.png",
        "frames_count": 3,
        "frames": [
            {
                "frame_rect": (0, 0, 61, 75),
                "offset": (-30, -75),
            },
            {
                "frame_rect": (61, 0, 61, 75),
                "offset": (-30, -75),
            },
            {
                "frame_rect": (122, 0, 61, 75),
                "offset": (-30, -75),
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
            },
            {
                "frame_rect": (51, 0, 50, 81),
                "offset": (-21, -81),
            },
            {
                "frame_rect": (101, 0, 58, 81),
                "offset": (-24, -81),
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
            },
            {
                "frame_rect": (51, 0, 58, 78),
                "offset": (-30, -78),
            },
            {
                "frame_rect": (101, 0, 96, 78),
                "offset": (-30, -78),
            }
        ]
    },
    "hit": {
        "file": "assets/enemies/ferris_hit.png",
        "frames_count": 3,
        "frames": [
            {
                "frame_rect": (0, 0, 56, 78),
                "offset": (-28, -78),
            },
            {
                "frame_rect": (56, 0, 66, 78),
                "offset": (-33, -78),
            },
            {
                "frame_rect": (122, 0, 56, 78),
                "offset": (-28, -78),
            }
        ]
    },
    "dead": {
        "file": "assets/enemies/ferris_dead.png",
        "frames_count": 2,
        "frames": [
            {
                "frame_rect": (0, 0, 111, 36),
                "offset": (-50, -36),
            },
            {
                "frame_rect": (111, 0, 125, 36),
                "offset": (-50, -36),
            }
        ]
    },
}

FERRIS_ANIM_FPS = {
    "idle": 6,
    "walk": 6,
    "attack": 6,
    "hit": 10,
    "dead": 12,
}
