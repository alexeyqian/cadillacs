import pygame


def combat_box_to_world_rect(anchor_x, anchor_y, facing_right, box):
    if facing_right:
        world_x = anchor_x + box.x
    else:
        world_x = anchor_x - box.x - box.width

    return pygame.Rect(
        int(world_x),
        int(anchor_y + box.y),
        int(box.width),
        int(box.height)
    )
