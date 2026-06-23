from game.components.movement_math import (
    clamp_to_world_and_lane,
    face_toward_x,
    get_distance_to,
    move_x,
)
from game.settings import ENEMY_Y_SPEED


CHASE_VERTICAL_DEAD_ZONE = 10
FLANK_VERTICAL_SPEED_SCALE = 0.75
SEPARATION_DISTANCE = 40
SEPARATION_PUSH = 1


class EnemyMovement:
    def __init__(
        self,
        speed=0,
        patrol_distance=0,
        detect_range=0,
        patrol_direction=1,
        y_speed=None,
    ):
        self.speed = speed
        self.y_speed = y_speed if y_speed is not None else ENEMY_Y_SPEED
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

    def patrol(self, owner, patrol_center_x):
        owner.x += self.patrol_direction
        self._face_patrol_direction(owner)
        self._turn_at_patrol_bounds(owner, patrol_center_x)

    def _face_patrol_direction(self, owner):
        if self.patrol_direction > 0:
            owner.facing_right = True
        elif self.patrol_direction < 0:
            owner.facing_right = False

    def _turn_at_patrol_bounds(self, owner, patrol_center_x):
        if owner.x > patrol_center_x + self.patrol_distance:
            self.patrol_direction = -1

        if owner.x < patrol_center_x - self.patrol_distance:
            self.patrol_direction = 1

    # Enemy has attack slot -> attacks
    # Enemy is in range but slot is full -> moves toward a side position
    # Enemy groups spread around player instead of stacking directly
    # pick less crowded side and drift there

    # With 1 slot: closest eligible enemy on its side attacks
    # With future 2 slots: one enemy per side can attack
    # Enemies without slots flank toward less crowded side
    # Flanking movement code is easier to read
    def move_toward_player(self, owner, player):
        dx, dy, distance_x, distance_y = self.get_player_distance(owner, player)
        self._move_horizontally(owner, dx)
        self._move_vertically(owner, dy)

    def _move_horizontally(self, owner, dx):
        if dx > 0:
            move_x(owner, 1, self.speed)
        elif dx < 0:
            move_x(owner, -1, self.speed)

    def _move_vertically(self, owner, dy):
        if abs(dy) > CHASE_VERTICAL_DEAD_ZONE:
            if dy > 0:
                owner.y += self.y_speed
            else:
                owner.y -= self.y_speed

    def separate_from_enemies(self, owner, enemies):
        for other in enemies:
            if other is owner:
                continue

            if other.state == owner.DEAD:
                continue

            self._separate_from_enemy(owner, other)

    def _separate_from_enemy(self, owner, other):
        dx = other.x - owner.x

        if abs(dx) >= SEPARATION_DISTANCE:
            return

        if dx > 0:
            owner.x -= SEPARATION_PUSH
        else:
            owner.x += SEPARATION_PUSH
                    
    def move_toward_position(self, owner, position):
        target_x, target_y = position
        self._move_toward_point(owner, target_x, target_y)

    def _move_toward_point(self, owner, target_x, target_y):
        if abs(owner.x - target_x) > self.speed:
            if owner.x < target_x:
                move_x(owner, 1, self.speed)
            else:
                move_x(owner, -1, self.speed)

        # Flanking has smoother vertical drift instead of sharp diagonal snapping
        # Slightly slower vertical correction makes enemy movement 
        # look more organic while still understandable.
        if abs(owner.y - target_y) > self.y_speed:
            if owner.y < target_y:
                owner.y += self.y_speed * FLANK_VERTICAL_SPEED_SCALE
            else:
                owner.y -= self.y_speed * FLANK_VERTICAL_SPEED_SCALE

    def apply_world_bounds(self, owner, world_width=None, lane_top=None, lane_bottom=None):
        clamp_to_world_and_lane(
            owner,
            world_width,
            lane_top,
            lane_bottom,
            half_width=owner.geometry.collision_box_w // 2,
            owner_name="Enemy",
        )
