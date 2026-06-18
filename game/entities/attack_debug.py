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

    hitbox_line = format_hitbox_line("hitbox", get_attack_hitbox(attack))
    if hitbox_line:
        lines.append(hitbox_line)

    counter_line = format_hitbox_line(
        "counter",
        getattr(attack, "counter_hurtbox", None)
    )
    if counter_line:
        lines.append(counter_line)

    return lines


def get_attack_hitbox(attack):
    return getattr(attack, "hitbox", None)


def format_hitbox_line(label, box):
    if not box:
        return ""
    return (
        f"{label} x:{box.x} y:{box.y} "
        f"w:{box.width} h:{box.height}"
    )
