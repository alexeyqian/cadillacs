# frame_rect format: (x, y, width, height) -  x, y is the left top location in the png file
# offset format: (x, y) - x, y  = (0,0) - (feet_center_x, feet_center_y)
# hurt_rect format: (x, y, width, height) -   x, y is relative position inside the current frame
# attack_rect format: (x, y, width, height) - x, y is relative position inside the current frame
GNEISS_ANIMATIONS = {
    "idle": {
        "file": "assets/enemies/gneiss_idle.png",
        "frames_count": 3,
        "frames": [
            {
                "frame_rect": (0, 0, 61, 76),
                "offset": (-30, -76),
                "hurt_rect": (7, 0, 43, 76),
                "attack_rect": None
            },
            {
                "frame_rect": (61, 0, 61, 76),
                "offset": (-30, -76),
                "hurt_rect": (7, 0, 43, 76),
                "attack_rect": None
            },
            {
                "frame_rect": (122, 0, 61, 76),
                "offset": (-30, -76),
                "hurt_rect": (7, 0, 43, 76),
                "attack_rect": None
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
        "file": "assets/enemies/gneiss_attack.png",
        "frames_count": 3,
        "frames": [
            {
                "frame_rect": (0, 0, 61, 79),
                "offset": (-30, -79),
                "hurt_rect": (15, 0, 43, 79),
                "attack_rect": None
            },
            {
                "frame_rect": (61, 0, 80, 79),
                "offset": (-30, -79),
                "hurt_rect": (21, 0, 43, 79),
                "attack_rect": None
            },
            {
                "frame_rect": (141, 0, 96, 79),
                "offset": (-30, -79),
                "hurt_rect": (25, 0, 43, 79),
                "attack_rect": None
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
                "hurt_rect": (15, 0, 43, 78),
                "attack_rect": None
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
                "hurt_rect": (15, 0, 110, 36),
                "attack_rect": None
            },
            {
                "frame_rect": (112, 0, 125, 36),
                "offset": (-50, -36),
                "hurt_rect": (15, 0, 110, 36),
                "attack_rect": None
            }
        ]
    },
}

GNEISS_ANIM_FPS = {
    "idle": 6,
    "walk": 6,
    "attack": 6,
    "hit": 12,
    "dead": 12,
}
