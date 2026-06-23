# frame_rect format: (x, y, width, height) -  x, y is the left top location in the png file
# offset format: (x, y) - x, y  = (0,0) - (feet_center_x, feet_center_y)
GNEISS_ANIMATIONS = {
    "idle": {
        "file": "assets/enemies/gneiss_walk_3x.png",
        "frames_count": 1,
        "frame_width": 256,
        "frame_height": 256,
    },
    "walk": {
        "file": "assets/enemies/gneiss_walk_3x.png",
        "frames_count": 7,
        "frame_width": 256,
        "frame_height": 256,
    },
    "attack": {
        "file": "assets/enemies/gneiss_attack_3x.png",
        "frames_count": 3,
        "frame_width": 384,
        "frame_height": 384,
        "hitbox": (96, -200, 96, 50),
        "frame_durations": (4,8,6)
    },
    "hit": {
        "file": "assets/enemies/gneiss_hit_3x.png",
        "frames_count": 1,
        "frame_width": 256,
        "frame_height": 256,
    },
    "dead": {
        "file": "assets/enemies/gneiss_dead_3x.png",
        "frames_count": 1,
        "frame_width": 384,
        "frame_height": 384,
    },
}
