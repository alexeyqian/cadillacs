# frame_rect format: (x, y, width, height) -  x, y is the left top location in the png file
# offset is derived from the frame size: (0, 0) means the character's bottom-center anchor.
MUSTAPHA_DEFAULT_FRAME_SIZE = (256, 256)
MUSTAPHA_DEFAULT_OFFSET = (-128, -256)

MUSTAPHA_ANIMATIONS = {
    "idle": {
        "file": "assets/player/mustapha_walk_3x.png",
        "frames_count": 1,
        "frame_width": 256,
        "frame_height": 256,
    },
    "walk": {
        "file": "assets/player/mustapha_walk_3x.png",
        "frames_count": 4,
        "frame_width": 256,
        "frame_height": 256,
    },
    "run": {
        "file": "assets/player/mustapha_run_3x.png",
        "frames_count": 9,
        "frame_width": 384,
        "frame_height": 384,
    },
    "jump": {
        "file": "assets/player/mustapha_jump_3x.png",
        "frames_count": 4,
        "frame_width": 384,
        "frame_height": 384,
    },
    "hit": {
        "file": "assets/player/mustapha_hit_3x.png",
        "frames_count": 1,
        "frame_width": 256,
        "frame_height": 256,
    },
    "dead": {
        "file": "assets/player/mustapha_dead_3x.png",
        "frames_count": 1,
        "frame_width": 384,
        "frame_height": 384,
    },
    "attack": {
        "file": "assets/player/mustapha_attack_3x.png",
        "frames_count": 3,
        "frame_width": 384,
        "frame_height": 384,
    },
    "attack2": {
        "file": "assets/player/mustapha_attack_3x.png",
        "frames_count": 3,
        "frame_width": 384,
        "frame_height": 384,
    },
    "attack3": {
        "file": "assets/player/mustapha_attack_3x.png",
        "frames_count": 3,
        "frame_width": 384,
        "frame_height": 384,
    },
    "run_attack": {
        "file": "assets/player/mustapha_run_attack_3x.png",
        "frames_count": 3,
        "frame_width":384,
        "frame_height":384,
        "scale": 1
    },
    "jump_attack": {
        "file": "assets/player/mustapha_run_attack_3x.png",
        "frames_count": 2,
        "frames": [
            {
                "frame_rect": (0, 0, 120, 92),
                "offset": (-60, -150),
            },
            {
                "frame_rect": (120, 0, 223, 92),
                "offset": (-110, -150),
            }
        ]
    },
    "grab": {
        "file": "assets/player/mustapha_grab.png",
        "frames_count": 1,
        "frames": [
            {
                "frame_rect": (0, 0, 123, 162),
                "offset": (-40, -162),
            }
        ]
    },
    "throw": {
        "file": "assets/player/mustapha_throw.png",
        "frames_count": 1,
        "frames": [
            {
                "frame_rect": (0, 0, 153, 162),
                "offset": (-40, -162),
            }
        ]
    },
    "grab_knee": {
        "file": "assets/player/mustapha_grab_knee.png",
        "frames_count": 2,
        "frames": [
            {
                "frame_rect": (0, 0, 123, 165),
                "offset": (-40, -165),
            },
            {
                "frame_rect": (123, 0, 88, 165),
                "offset": (-35, -165),
            }
        ]
    },
}

for config in MUSTAPHA_ANIMATIONS.values():
    if "scale" not in config:
        config["scale"] = 1

    if "frame_width" in config and "frame_height" in config:
        config["default_frame_size"] = (config["frame_width"], config["frame_height"])
    elif "frames" not in config:
        config["default_frame_size"] = MUSTAPHA_DEFAULT_FRAME_SIZE

    if "frames" not in config:
        frame_width, frame_height = config["default_frame_size"]
        config["default_offset"] = (-frame_width / 2, -frame_height)

MUSTAPHA_ANIM_FPS = {
    "idle": 6,
    "walk": 10,
    "run": 6,
    "jump": 10,
    "attack": 12,
    "attack2": 12,
    "attack3": 12,
    "run_attack": 6,
    "jump_attack": 6,
    "grab": 6,
    "throw": 6,
    "grab_knee": 6,
    "hit": 6,
    "dead": 999,
}
