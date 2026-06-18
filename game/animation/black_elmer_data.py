# frame_rect format: (x, y, width, height) -  x, y is the left top location in the png file
# offset format: (x, y) - x, y  = (0,0) - (feet_center_x, feet_center_y)
BLACK_ELMER_ANIMATIONS = {
    "idle": {
        "file": "assets/enemies/black_elmer_idle.png",
        "frames_count": 9,
        "frames": [
            {"frame_rect": (0, 0, 56, 90), "offset": (-28, -90)},
            {"frame_rect": (56, 0, 62, 90), "offset": (-31, -90)},
            {"frame_rect": (118, 0, 62, 90), "offset": (-31, -90)},
            {"frame_rect": (180, 0, 62, 90), "offset": (-31, -90)},
            {"frame_rect": (242, 0, 62, 90), "offset": (-31, -90)},
            {"frame_rect": (304, 0, 62, 90), "offset": (-31, -90)},
            {"frame_rect": (366, 0, 62, 90), "offset": (-31, -90)},
            {"frame_rect": (428, 0, 55, 90), "offset": (-28, -90)},
            {"frame_rect": (483, 0, 56, 90), "offset": (-28, -90)},
        ]
    },
    "walk": {
        "file": "assets/enemies/black_elmer_walk.png",
        "frames_count": 5,
        "frames": [
            {"frame_rect": (0, 0, 56, 84), "offset": (-28, -84)},
            {"frame_rect": (56, 0, 54, 84), "offset": (-27, -84)},
            {"frame_rect": (110, 0, 54, 84), "offset": (-27, -84)},
            {"frame_rect": (164, 0, 54, 84), "offset": (-27, -84)},
            {"frame_rect": (218, 0, 54, 84), "offset": (-27, -84)},
        ]
    },
    "run": {
        "file": "assets/enemies/black_elmer_run.png",
        "frames_count": 9,
        "frames": [
            {"frame_rect": (0, 0, 82, 76), "offset": (-41, -76)},
            {"frame_rect": (82, 0, 76, 76), "offset": (-38, -76)},
            {"frame_rect": (158, 0, 93, 76), "offset": (-47, -76)},
            {"frame_rect": (251, 0, 73, 76), "offset": (-37, -76)},
            {"frame_rect": (324, 0, 61, 76), "offset": (-31, -76)},
            {"frame_rect": (385, 0, 75, 76), "offset": (-38, -76)},
            {"frame_rect": (460, 0, 91, 76), "offset": (-46, -76)},
            {"frame_rect": (551, 0, 72, 76), "offset": (-36, -76)},
            {"frame_rect": (623, 0, 61, 76), "offset": (-31, -76)},
        ]
    },
    "attack": {
        "file": "assets/enemies/black_elmer_attack.png",
        "frames_count": 3,
        "frames": [
            {"frame_rect": (0, 0, 93, 85), "offset": (-47, -85)},
            {"frame_rect": (93, 0, 107, 85), "offset": (-54, -85)},
            {"frame_rect": (200, 0, 128, 85), "offset": (-64, -85)},
        ]
    },
    "leg_attack": {
        "file": "assets/enemies/black_elmer_leg_attack.png",
        "frames_count": 3,
        "frames": [
            {"frame_rect": (0, 0, 88, 81), "offset": (-44, -81)},
            {"frame_rect": (88, 0, 69, 81), "offset": (-35, -81)},
            {"frame_rect": (157, 0, 95, 81), "offset": (-48, -81)},
        ]
    },
    "jump": {
        "file": "assets/enemies/black_elmer_jump.png",
        "frames_count": 4,
        "frames": [
            {"frame_rect": (0, 0, 79, 120), "offset": (-40, -120)},
            {"frame_rect": (79, 0, 85, 120), "offset": (-43, -120)},
            {"frame_rect": (164, 0, 179, 120), "offset": (-90, -120)},
            {"frame_rect": (343, 0, 75, 120), "offset": (-38, -120)},
        ]
    },
    "hit": {
        "file": "assets/enemies/black_elmer_hit.png",
        "frames_count": 2,
        "frames": [
            {"frame_rect": (0, 0, 64, 75), "offset": (-32, -75)},
            {"frame_rect": (64, 0, 65, 75), "offset": (-33, -75)},
        ]
    },
    "dead": {
        "file": "assets/enemies/black_elmer_dead.png",
        "frames_count": 4,
        "frames": [
            {"frame_rect": (0, 0, 70, 84), "offset": (-35, -84)},
            {"frame_rect": (70, 0, 96, 84), "offset": (-48, -84)},
            {"frame_rect": (166, 0, 104, 84), "offset": (-52, -84)},
            {"frame_rect": (270, 0, 74, 84), "offset": (-37, -84)},
        ]
    },
    "dizzy": {
        "file": "assets/enemies/black_elmer_dizzy.png",
        "frames_count": 3,
        "frames": [
            {"frame_rect": (0, 0, 60, 70), "offset": (-30, -70)},
            {"frame_rect": (60, 0, 69, 70), "offset": (-35, -70)},
            {"frame_rect": (129, 0, 65, 70), "offset": (-33, -70)},
        ]
    },
}

BLACK_ELMER_ANIM_FPS = {
    "idle": 6,
    "walk": 6,
    "run": 10,
    "attack": 6,
    "leg_attack": 6,
    "jump": 8,
    "hit": 12,
    "dead": 10,
    "dizzy": 8,
}

