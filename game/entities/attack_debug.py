def format_attack_debug_lines(label, controller, damage=None, lane_reach=None):
    attack = controller.current_attack
    if not attack:
        return []

    lines = [
        (
            f"{label}: {controller.current_attack_name} "
            f"{controller.get_phase_name()} "
            f"{controller.elapsed_frames}/{controller.get_attack_duration()}"
        )
    ]

    details = [
        f"hits {controller.get_hit_count()}/{controller.get_max_targets()}",
    ]
    if damage is not None:
        details.append(f"damage {int(damage)}")
    if lane_reach is not None:
        details.append(f"lane {lane_reach}")
    lines.append(" | ".join(details))

    hitbox_line = format_hitbox_line(
        "hitbox",
        attack.hitbox_offset_x,
        attack.hitbox_offset_y,
        attack.hitbox_w,
        attack.hitbox_h,
    )
    if hitbox_line:
        lines.append(hitbox_line)

    return lines


def format_hitbox_line(label, offset_x, offset_y, width, height):
    if width <= 0 or height <= 0:
        return ""
    return (
        f"{label} x:{offset_x} y:{offset_y} "
        f"w:{width} h:{height}"
    )
