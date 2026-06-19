from game.components.movement_math import (
    clamp_to_world_and_lane,
    face_toward_x,
    get_distance_to,
    move_x,
)


class EnemyMovement:
    def __init__(
        self,
        spawn_x=0,
        speed=0,
        patrol_distance=0,
        detect_range=0,
        patrol_direction=1,
    ):
        self.spawn_x = spawn_x
        self.speed = speed
        self.patrol_distance = patrol_distance
        self.detect_range = detect_range
        self.patrol_direction = patrol_direction

    def configure(self, speed, patrol_distance, detect_range):
        self.speed = speed
        self.patrol_distance = patrol_distance
        self.detect_range = detect_range

    def get_player_distance(self, owner, player):
        return get_distance_to(owner, player)

    def face_player(self, owner, player):
        face_toward_x(owner, player.x)

    def update_patrol(self, owner):
        owner.x += self.patrol_direction

        if self.patrol_direction > 0:
            owner.facing_right = True
        elif self.patrol_direction < 0:
            owner.facing_right = False

        if owner.x > self.spawn_x + self.patrol_distance:
            self.patrol_direction = -1

        if owner.x < self.spawn_x - self.patrol_distance:
            self.patrol_direction = 1

    # Enemy has attack slot -> attacks
    # Enemy is in range but slot is full -> moves toward a side position
    # Enemy groups spread around player instead of stacking directly
    # pick less crowded side and drift there

    # With 1 slot: closest eligible enemy on its side attacks
    # With future 2 slots: one enemy per side can attack
    # Enemies without slots flank toward less crowded side
    # Flanking movement code is easier to read
    def update_chasing(self, owner, player, dx, dy):
        if owner.flanking.has_target():
            target_x, target_y = owner.flanking.get_target_position(player)
            self.move_toward_point(owner, target_x, target_y)
            return

        if dx > 0:
            move_x(owner, 1, self.speed)
        elif dx < 0:
            move_x(owner, -1, self.speed)

        if abs(dy) > 10:
            if dy > 0:
                owner.y += self.speed
            else:
                owner.y -= self.speed

    def separate_from_other_enemies(self, owner, enemies):
        for other in enemies:
            if other is owner:
                continue

            if other.state == owner.DEAD:
                continue

            dx = other.x - owner.x

            if abs(dx) < 40:
                if dx > 0:
                    owner.x -= 1
                else:
                    owner.x += 1
                    
    def move_toward_point(self, owner, target_x, target_y):
        if abs(owner.x - target_x) > self.speed:
            if owner.x < target_x:
                move_x(owner, 1, self.speed)
            else:
                move_x(owner, -1, self.speed)

        # Flanking has smoother vertical drift instead of sharp diagonal snapping
        # Slightly slower vertical correction makes enemy movement 
        # look more organic while still understandable.
        if abs(owner.y - target_y) > self.speed:
            if owner.y < target_y:
                owner.y += self.speed * 0.75
            else:
                owner.y -= self.speed * 0.75

    def apply_world_bounds(self, owner, world_width=None, lane_top=None, lane_bottom=None):
        clamp_to_world_and_lane(
            owner,
            world_width,
            lane_top,
            lane_bottom,
            half_width=owner.collision_box_w // 2,
            owner_name="Enemy",
        )
