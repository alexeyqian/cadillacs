# frame_rect format: (x, y, width, height) -  x, y is the left top location in the png file
# offset format: (x, y) - x, y  = (0,0) - (feet_center_x, feet_center_y)
GNEISS_ANIMATIONS = {
    "idle": {
        "file": "assets/enemies/gneiss_idle.png",
        "frames_count": 3,
        "frames": [
            {
                "frame_rect": (0, 0, 61, 76),
                "offset": (-30, -76),
            },
            {
                "frame_rect": (61, 0, 61, 76),
                "offset": (-30, -76),
            },
            {
                "frame_rect": (122, 0, 61, 76),
                "offset": (-30, -76),
            }
        ]
    },
    "walk": {
        "file": "assets/enemies/gneiss_walk.png",
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
        "file": "assets/enemies/gneiss_attack.png",
        "frames_count": 3,
        "frames": [
            {
                "frame_rect": (0, 0, 61, 76),
                "offset": (-30, -76),
            },
            {
                "frame_rect": (61, 0, 61, 76),
                "offset": (-30, -76),
            },
            {
                "frame_rect": (122, 0, 96, 76),
                "offset": (-30, -76),
            }
        ]
    },
    "hit": {
        "file": "assets/enemies/gneiss_hit.png",
        "frames_count": 1,
        "frames": [
            {
                "frame_rect": (0, 0, 66, 78),
                "offset": (-30, -78),
            }
        ]
    },
    "dead": {
        "file": "assets/enemies/gneiss_dead.png",
        "frames_count": 2,
        "frames": [
            {
                "frame_rect": (0, 0, 112, 36),
                "offset": (-50, -36),
            },
            {
                "frame_rect": (112, 0, 125, 36),
                "offset": (-50, -36),
            }
        ]
    },
}

GNEISS_ANIM_FPS = {
    "idle": 6,
    "walk": 6,
    "attack": 7,
    "hit": 12,
    "dead": 12,
}
