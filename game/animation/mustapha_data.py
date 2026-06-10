MUSTAPHA_ANIMATIONS = {
    "idle": {
        "frames_count": 6,
        # Format: (frame tuple, hurt box tuple, hit box tuple)
        # tuple layout: (offset_x, offset_y, width, height)
        "frames": [
            ((0, 0, 100, 182), (-20, -90, 40, 85), None),
            ((100, 0, 100, 182), (-20, -90, 40, 85), None),
            ((210, 0, 110, 182), (-21, -91, 42, 86), None),
            ((350, 0, 140, 182), (-20, -90, 40, 85), None)
            ((480, 0, 130, 182), (-20, -90, 40, 85), None)
            ((610, 0, 100, 182), (-20, -90, 40, 85), None)
        ]
    },
    "walk": {
        "frames_count": 6,
        "frames": [
            ((0, 0, 100, 182), (-20, -90, 40, 85), None),
            ((100, 0, 100, 182), (-20, -90, 40, 85), None),
            ((210, 0, 110, 182), (-21, -91, 42, 86), None),
            ((350, 0, 140, 182), (-20, -90, 40, 85), None)
            ((480, 0, 130, 182), (-20, -90, 40, 85), None)
            ((610, 0, 100, 182), (-20, -90, 40, 85), None)
        ]
    },
}

# The universal grounding anchor shared globally across Mustapha's actions
#GLOBAL_BASE_RECT_DIM = (-15, -10, 30, 10)
