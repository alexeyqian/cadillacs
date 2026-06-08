from pathlib import Path

from PIL import Image, ImageDraw


OUT_DIR = Path(__file__).resolve().parents[1] / "game" / "assets" / "player"

OUTLINE = (38, 24, 18, 255)
SKIN = (232, 166, 92, 255)
SKIN_DARK = (133, 75, 39, 255)
HAIR = (70, 42, 22, 255)
CAP = (213, 178, 65, 255)
CAP_DARK = (125, 90, 32, 255)
SHIRT = (40, 169, 58, 255)
SHIRT_DARK = (13, 86, 43, 255)
PANTS = (246, 207, 69, 255)
PANTS_DARK = (182, 126, 34, 255)
BOOT = (128, 67, 25, 255)
GLOVE = (52, 40, 28, 255)
BELT = (57, 38, 23, 255)
BUCKLE = (232, 196, 75, 255)
HIT_FLASH = (255, 235, 113, 255)


ANIMATIONS = {
    "player_idle.png": {"size": (128, 256), "state": "idle"},
    "player_walk.png": {"size": (128, 256), "state": "walk"},
    "player_run.png": {"size": (128, 256), "state": "run"},
    "player_jump.png": {"size": (128, 256), "state": "jump"},
    "player_attack.png": {"size": (192, 256), "state": "attack"},
    "player_run_attack.png": {"size": (224, 256), "state": "run_attack"},
    "player_jump_attack.png": {"size": (224, 256), "state": "jump_attack"},
    "player_grab.png": {"size": (176, 256), "state": "grab"},
    "player_throw.png": {"size": (224, 256), "state": "throw"},
    "player_hit.png": {"size": (144, 256), "state": "hit"},
    "player_dead.png": {"size": (256, 128), "state": "dead"},
}


def ellipse(draw, box, fill, outline=None, width=1):
    draw.ellipse(tuple(int(v) for v in box), fill=fill, outline=outline, width=width)


def rect(draw, box, fill, outline=None, width=1):
    draw.rectangle(tuple(int(v) for v in box), fill=fill, outline=outline, width=width)


def line(draw, points, fill, width):
    draw.line([(int(x), int(y)) for x, y in points], fill=fill, width=int(width), joint="curve")


def polygon(draw, points, fill, outline=None):
    draw.polygon([(int(x), int(y)) for x, y in points], fill=fill, outline=outline)


def draw_arm(draw, shoulder, elbow, hand, sleeve=False):
    upper_color = SHIRT if sleeve else SKIN
    line(draw, [shoulder, elbow], OUTLINE, 25)
    line(draw, [shoulder, elbow], upper_color, 19)
    line(draw, [elbow, hand], OUTLINE, 23)
    line(draw, [elbow, hand], SKIN, 17)
    ellipse(draw, (hand[0] - 12, hand[1] - 10, hand[0] + 13, hand[1] + 11), OUTLINE)
    ellipse(draw, (hand[0] - 9, hand[1] - 8, hand[0] + 10, hand[1] + 9), GLOVE)


def draw_leg(draw, hip, knee, foot, front=True):
    color = PANTS if front else PANTS_DARK
    line(draw, [hip, knee], OUTLINE, 31)
    line(draw, [hip, knee], color, 25)
    line(draw, [knee, foot], OUTLINE, 29)
    line(draw, [knee, foot], color, 23)
    rect(draw, (foot[0] - 21, foot[1] - 11, foot[0] + 23, foot[1] + 10), OUTLINE)
    rect(draw, (foot[0] - 18, foot[1] - 8, foot[0] + 20, foot[1] + 8), BOOT)


def draw_starburst(draw, cx, cy, radius):
    points = []
    for i in range(12):
        angle = i * 3.14159 / 6
        r = radius if i % 2 == 0 else radius * 0.45
        points.append((cx + r * __import__("math").cos(angle), cy + r * __import__("math").sin(angle)))
    polygon(draw, points, HIT_FLASH)


def pose_values(state, frame):
    phase = [-1.0, -0.45, 0.25, 0.9, 0.35, -0.55][frame]
    values = {
        "body_x": 64,
        "body_y": 106,
        "lean": 0,
        "head_x": 72,
        "head_y": 56,
        "front_arm": ((83, 91), (101, 114), (93, 143)),
        "back_arm": ((50, 92), (39, 119), (45, 145)),
        "front_leg": ((74, 154), (78, 190), (87, 231)),
        "back_leg": ((53, 154), (49, 191), (39, 231)),
    }

    if state == "idle":
        bob = [0, 1, 2, 1, 0, -1][frame]
        values["body_y"] += bob
        values["head_y"] += bob
        values["front_arm"] = ((83, 91 + bob), (96, 119 + bob), (91, 148 + bob))
        values["back_arm"] = ((49, 92 + bob), (42, 121 + bob), (48, 149 + bob))
    elif state == "walk":
        values["body_x"] += phase * 3
        values["front_leg"] = ((74, 154), (74 + phase * 13, 190), (83 + phase * 22, 231))
        values["back_leg"] = ((53, 154), (51 - phase * 12, 190), (39 - phase * 20, 231))
        values["front_arm"] = ((83, 91), (96 - phase * 12, 117), (90 - phase * 18, 145))
        values["back_arm"] = ((49, 92), (42 + phase * 11, 119), (48 + phase * 17, 148))
    elif state == "run":
        values["lean"] = 12
        values["body_x"] += 8 + phase * 4
        values["head_x"] += 10
        values["front_leg"] = ((77, 154), (88 + phase * 18, 184), (102 + phase * 30, 228))
        values["back_leg"] = ((55, 154), (38 - phase * 16, 185), (24 - phase * 27, 228))
        values["front_arm"] = ((88, 91), (106 - phase * 17, 114), (104 - phase * 28, 143))
        values["back_arm"] = ((54, 92), (35 + phase * 16, 116), (25 + phase * 26, 144))
    elif state == "jump":
        lift = [30, 48, 62, 62, 45, 24][frame]
        values["body_y"] -= lift
        values["head_y"] -= lift
        values["front_leg"] = ((74, 154 - lift), (94, 177 - lift), (108, 202 - lift))
        values["back_leg"] = ((53, 154 - lift), (41, 181 - lift), (35, 211 - lift))
        values["front_arm"] = ((83, 91 - lift), (103, 86 - lift), (118, 70 - lift))
        values["back_arm"] = ((49, 92 - lift), (36, 87 - lift), (24, 73 - lift))
    elif state == "attack":
        ext = [12, 34, 58, 72, 42, 16][frame]
        values["body_x"] = 70
        values["lean"] = 8
        values["head_x"] = 78
        values["front_arm"] = ((89, 91), (116 + ext * 0.35, 95), (106 + ext, 97))
        values["back_arm"] = ((55, 93), (45, 119), (51, 145))
        values["front_leg"] = ((78, 154), (90, 189), (105, 231))
        values["back_leg"] = ((56, 154), (48, 191), (39, 231))
    elif state == "run_attack":
        ext = [18, 48, 84, 102, 62, 26][frame]
        values["body_x"] = 82
        values["lean"] = 18
        values["head_x"] = 92
        values["front_arm"] = ((100, 91), (132 + ext * 0.25, 93), (118 + ext, 94))
        values["back_arm"] = ((66, 93), (43, 120), (31, 144))
        values["front_leg"] = ((91, 154), (112, 185), (136, 229))
        values["back_leg"] = ((68, 154), (41, 188), (19, 226))
    elif state == "jump_attack":
        ext = [28, 58, 93, 108, 72, 34][frame]
        lift = [28, 43, 58, 61, 47, 30][frame]
        values["body_x"] = 76
        values["body_y"] -= lift
        values["head_x"] = 86
        values["head_y"] -= lift
        values["lean"] = 10
        values["front_leg"] = ((86, 154 - lift), (120 + ext * 0.25, 160 - lift), (112 + ext, 164 - lift))
        values["back_leg"] = ((61, 154 - lift), (45, 184 - lift), (36, 212 - lift))
        values["front_arm"] = ((92, 91 - lift), (109, 73 - lift), (125, 58 - lift))
        values["back_arm"] = ((58, 92 - lift), (43, 83 - lift), (30, 68 - lift))
    elif state == "grab":
        ext = [18, 34, 47, 47, 34, 18][frame]
        values["body_x"] = 67
        values["front_arm"] = ((86, 91), (108 + ext * 0.4, 111), (101 + ext, 128))
        values["back_arm"] = ((53, 92), (76 + ext * 0.35, 112), (73 + ext, 131))
    elif state == "throw":
        swing = [6, 25, 55, 88, 65, 24][frame]
        values["body_x"] = 78
        values["lean"] = [0, -8, -14, 16, 12, 3][frame]
        values["head_x"] = 86
        values["front_arm"] = ((96, 88), (118 + swing * 0.4, 66), (108 + swing, 76))
        values["back_arm"] = ((62, 92), (85 + swing * 0.35, 116), (80 + swing, 135))
        values["front_leg"] = ((88, 154), (102, 190), (118, 231))
        values["back_leg"] = ((65, 154), (50, 191), (37, 231))
    elif state == "hit":
        recoil = [0, -8, -14, -10, -5, 0][frame]
        values["body_x"] = 68 + recoil
        values["lean"] = -14
        values["head_x"] = 75 + recoil
        values["front_arm"] = ((82 + recoil, 91), (102 + recoil, 82), (112 + recoil, 73))
        values["back_arm"] = ((49 + recoil, 92), (35 + recoil, 105), (25 + recoil, 124))
        values["front_leg"] = ((74 + recoil, 154), (82 + recoil, 190), (96 + recoil, 231))
        values["back_leg"] = ((53 + recoil, 154), (42 + recoil, 190), (35 + recoil, 231))

    return values


def draw_character(draw, state, frame):
    if state == "dead":
        x = 50 + frame * 2
        y = 72 + min(frame, 3)
        rect(draw, (x + 29, y - 27, x + 111, y + 11), OUTLINE)
        rect(draw, (x + 32, y - 24, x + 108, y + 8), PANTS)
        rect(draw, (x + 99, y - 32, x + 148, y - 9), OUTLINE)
        rect(draw, (x + 102, y - 29, x + 145, y - 12), BOOT)
        rect(draw, (x + 3, y - 31, x + 77, y + 17), OUTLINE)
        rect(draw, (x + 6, y - 28, x + 74, y + 14), SHIRT_DARK)
        ellipse(draw, (x - 24, y - 44, x + 24, y + 4), OUTLINE)
        ellipse(draw, (x - 20, y - 40, x + 20, y), SKIN, SKIN_DARK, 2)
        rect(draw, (x - 19, y - 48, x + 20, y - 30), CAP_DARK)
        rect(draw, (x - 18, y - 51, x + 22, y - 35), CAP)
        rect(draw, (x + 14, y - 39, x + 42, y - 32), CAP_DARK)
        line(draw, [(x + 22, y - 14), (x + 48, y - 7), (x + 70, y - 4)], SKIN, 14)
        line(draw, [(x + 4, y + 4), (x - 17, y + 17)], SKIN, 13)
        return

    v = pose_values(state, frame)
    bx = v["body_x"]
    by = v["body_y"]
    lean = v["lean"]

    draw_leg(draw, *v["back_leg"], front=False)
    draw_leg(draw, *v["front_leg"], front=True)

    torso = [
        (bx - 34 + lean * 0.15, by - 48),
        (bx + 29 + lean * 0.7, by - 48),
        (bx + 39 + lean * 0.25, by + 39),
        (bx - 25 - lean * 0.25, by + 41),
    ]
    polygon(draw, torso, OUTLINE)
    inner_torso = [
        (torso[0][0] + 4, torso[0][1] + 4),
        (torso[1][0] - 4, torso[1][1] + 4),
        (torso[2][0] - 5, torso[2][1] - 4),
        (torso[3][0] + 5, torso[3][1] - 4),
    ]
    polygon(draw, inner_torso, SHIRT)
    polygon(draw, [(bx + 2, by - 42), inner_torso[1], inner_torso[2], (bx + 10, by + 34)], SHIRT_DARK)
    polygon(draw, [(bx - 18, by - 44), (bx + 12, by - 43), (bx + 1, by - 16)], (236, 226, 172, 255))
    rect(draw, (bx - 29, by + 31, bx + 35, by + 45), OUTLINE)
    rect(draw, (bx - 25, by + 34, bx + 31, by + 43), BELT)
    rect(draw, (bx - 2, by + 33, bx + 11, by + 44), BUCKLE)

    draw_arm(draw, *v["back_arm"], sleeve=True)
    draw_arm(draw, *v["front_arm"], sleeve=True)

    hx = v["head_x"] + lean * 0.35
    hy = v["head_y"]
    ellipse(draw, (hx - 25, hy - 28, hx + 23, hy + 25), OUTLINE)
    ellipse(draw, (hx - 21, hy - 24, hx + 19, hy + 22), SKIN, SKIN_DARK, 2)
    rect(draw, (hx - 24, hy - 37, hx + 19, hy - 21), OUTLINE)
    rect(draw, (hx - 21, hy - 39, hx + 18, hy - 24), CAP)
    rect(draw, (hx + 8, hy - 29, hx + 38, hy - 21), OUTLINE)
    rect(draw, (hx + 10, hy - 28, hx + 36, hy - 23), CAP_DARK)
    rect(draw, (hx - 13, hy - 19, hx + 1, hy - 14), HAIR)
    rect(draw, (hx + 7, hy - 4, hx + 21, hy + 2), (30, 28, 26, 255))
    rect(draw, (hx + 10, hy + 11, hx + 25, hy + 15), SKIN_DARK)

    if state == "hit" and frame in (1, 2, 3):
        draw_starburst(draw, hx + 35, hy + 30, 16 - frame * 2)


def save_sheet(filename, size, state):
    frame_w, frame_h = size
    sheet = Image.new("RGBA", (frame_w * 6, frame_h), (0, 0, 0, 0))
    for frame in range(6):
        image = Image.new("RGBA", size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        draw_character(draw, state, frame)
        sheet.alpha_composite(image, (frame_w * frame, 0))
    sheet.save(OUT_DIR / filename)


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for filename, config in ANIMATIONS.items():
        save_sheet(filename, config["size"], config["state"])
        print(f"wrote {OUT_DIR / filename}")


if __name__ == "__main__":
    main()
