# frame_rect format: (x, y, width, height) -  x, y is the left top location in the png file
# offset format: (x, y) - x, y  = (0,0) - (feet_center_x, feet_center_y)
WALTHER_ANIMATIONS = {
    "idle": {
        "file": "assets/enemies/walther_walk.png",
        "frames_count": 2,
        "frames": [
            {
                "frame_rect": (0, 0, 100, 105),
                "offset": (-50, -105),
            },
            {
                "frame_rect": (100, 0, 100, 105),
                "offset": (-50, -105),
            },
        ]
    },
    "walk": {
        "file": "assets/enemies/walther_walk.png",
        "frames_count": 6,
        "frames": [
            {
                "frame_rect": (0, 0, 100, 105),
                "offset": (-50, -105),
            },
            {
                "frame_rect": (100, 0, 100, 105),
                "offset": (-50, -105),
            },
            {
                "frame_rect": (200, 0, 100, 105),
                "offset": (-50, -105),
            },
            {
                "frame_rect": (300, 0, 100, 105),
                "offset": (-50, -105),
            },
            {
                "frame_rect": (400, 0, 100, 105),
                "offset": (-50, -105),
            },
            {
                "frame_rect": (500, 0, 100, 105),
                "offset": (-50, -105),
            },
        ]
    },
    "attack": {
        "file": "assets/enemies/walther_attack.png",
        "frames_count": 2,
        "frames": [
            {
                "frame_rect": (0, 0, 100, 105),
                "offset": (-50, -105),
            },
            {
                "frame_rect": (100, 0, 130, 105),
                "offset": (-50, -105),
            }
        ]
    },
    "hit": {
        "file": "assets/enemies/walther_hit.png",
        "frames_count": 1,
        "frames": [
            {
                "frame_rect": (0, 0, 100, 105),
                "offset": (-50, -105),
            }
        ]
    },
    "dead": {
        "file": "assets/enemies/walther_dead.png",
        "frames_count": 1,
        "frames": [
            {
                "frame_rect": (0, 0, 150, 50),
                "offset": (-75, -50),
            }
        ]
    },
}

WALTHER_ANIM_FPS = {
    "idle": 6,
    "walk": 6,
    "attack": 6,
    "hit": 6,
    "dead": 6,
}
