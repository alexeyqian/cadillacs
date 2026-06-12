# frame_rect format: (x, y, width, height) -  x, y is the left top location in the png file
# offset format: (x, y) - x, y  = (0,0) - (feet_center_x, feet_center_y)
# hurt_rect format: (x, y, width, height) -   x, y is relative position inside the current frame
# attack_rect format: (x, y, width, height) - x, y is relative position inside the current frame
FERRIS_ANIMATIONS = {
    "idle": {
        "file": "assets/player/ferris_idle.png",
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
}