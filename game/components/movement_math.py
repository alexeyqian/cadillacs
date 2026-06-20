from game.settings import WORLD_WIDTH


def get_distance_to(source, target):
    dx = target.x - source.x
    dy = target.y - source.y
    return dx, dy, abs(dx), abs(dy)


def face_toward_x(owner, target_x):
    owner.facing_right = target_x > owner.x


def move_x(owner, direction, speed):
    if direction == 0:
        return

    owner.x += direction * speed
    owner.facing_right = direction > 0


def get_input_axis(negative_down, positive_down):
    if negative_down and not positive_down:
        return -1
    if positive_down and not negative_down:
        return 1
    return 0


def get_input_direction(player_input):
    return (
        get_input_axis(player_input.left, player_input.right),
        get_input_axis(player_input.up, player_input.down),
    )


def clamp_to_world_and_lane(
    owner,
    world_width=None,
    lane_top=None,
    lane_bottom=None,
    half_width=None,
    owner_name="Character",
):
    if world_width is None:
        world_width = WORLD_WIDTH
    if lane_top is None or lane_bottom is None:
        raise ValueError(f"{owner_name}.apply_world_bounds requires lane_top and lane_bottom")

    if half_width is None:
        raise ValueError(f"{owner_name}.apply_world_bounds requires half_width")

    owner.x = max(half_width, owner.x)
    owner.x = min(owner.x, world_width - half_width)
    owner.y = max(lane_top, owner.y)
    owner.y = min(lane_bottom, owner.y)
