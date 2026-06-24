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
    # Armed walk — same sheet as unarmed until dedicated art is added.
    # Replace "file" with a weapon-carrying walk sheet when available.
    "walk_armed": {
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
    "attack": {
        "file": "assets/player/mustapha_attack_3x.png",
        "frames_count": 3,
        "frame_width": 384,
        "frame_height": 384,
        "hitbox": (64, -256, 128, 100),
        "frame_durations": (3,10,5)
    },
    "attack2": {
        "file": "assets/player/mustapha_attack2_3x.png",
        "frames_count": 3,
        "frame_width": 384,
        "frame_height": 384,
        "frame_durations": (4,10,6),
        "hitbox": (64, -192, 128, 100),
    },
    "attack3": {
        "file": "assets/player/mustapha_attack3_3x.png",
        "frames_count": 3,
        "frame_width": 384,
        "frame_height": 384,
        "frame_durations": (5,10,8),
        "hitbox": (64, -192, 128, 100),
    },
    # Weapon attacks — replace files with dedicated sheets when art is ready.
    "ATTACK_KNIFE": {
        "file": "assets/player/mustapha_attack_3x.png",
        "frames_count": 3,
        "frame_width": 384,
        "frame_height": 384,
        "hitbox": (64, -256, 160, 100),
        "frame_durations": (2, 10, 4),
    },
    "ATTACK_PISTOL": {
        "file": "assets/player/mustapha_attack_3x.png",
        "frames_count": 3,
        "frame_width": 384,
        "frame_height": 384,
        "hitbox": (64, -256, 128, 100),
        "frame_durations": (3, 8, 5),
    },
    "run_attack": {
        "file": "assets/player/mustapha_run_attack_3x.png",
        "frames_count": 3,
        "frame_width":384,
        "frame_height":384,
        "hitbox": (50, -230, 128, 100),
        "frame_durations": (4,15,6)
    },
    "jump_attack": {
        "not_used": True,
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
        "file": "assets/player/mustapha_grab_3x.png",
        "frames_count": 1,
        "frame_width":256,
        "frame_height":256,
    },
    "grab_knee": {
        "file": "assets/player/mustapha_grab_knee_3x.png",
        "frames_count": 3,
        "frame_width":256,
        "frame_height":256,
        "hitbox": (64, -180, 64, 100),
        "frame_durations": (6,4,4)
    },
    "throw": {
        "file": "assets/player/mustapha_throw_3x.png",
        "frames_count": 2,
        "frame_width":256,
        "frame_height":256,
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

