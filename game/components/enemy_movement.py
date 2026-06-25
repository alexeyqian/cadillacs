from game.components.movement_math import (
    clamp_to_world_and_lane,
    face_toward_x,
    get_distance_to,
    move_x,
)
from game.components.enemy_air_state import EnemyAirState
from game.settings import (
    ENEMY_FLANK_DECISION_DURATION,
    ENEMY_FLANK_OFFSET_X,
    ENEMY_FLANK_OFFSET_Y,
    ENEMY_Y_SPEED,
)


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
        self.run_speed = speed
        self.can_run = False
        self.can_jump = False
        self.can_run_attack = False
        self.can_jump_attack = False
        self.air_state = EnemyAirState()
        self.y_speed = y_speed if y_speed is not None else ENEMY_Y_SPEED
        self.patrol_distance = patrol_distance
        self.detect_range = detect_range
        self.patrol_direction = patrol_direction

        # Flank state — which side the enemy is committed to when slots are full
        self.flank_target_side = None
        self._flank_target_y_offset = 0
        self._flank_offset_x = ENEMY_FLANK_OFFSET_X
        self._flank_offset_y = ENEMY_FLANK_OFFSET_Y
        self._flank_decision_remaining = 0
        self._flank_decision_duration = ENEMY_FLANK_DECISION_DURATION

    @property
    def is_jumping(self):
        return self.air_state.is_jumping

    def configure(self, speed, patrol_distance, detect_range, can_run=False, run_speed=None, can_jump=False,
                  can_run_attack=False, can_jump_attack=False):
        self.speed = speed
        self.run_speed = run_speed if run_speed is not None else speed
        self.can_run = can_run
        self.can_jump = can_jump
        self.can_run_attack = can_run_attack
        self.can_jump_attack = can_jump_attack
        self.patrol_distance = patrol_distance
        self.detect_range = detect_range

    def advance_timers(self):
        if self._flank_decision_remaining > 0:
            self._flank_decision_remaining -= 1

    # --- Chase / patrol ---

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

    def move_toward_player(self, owner, player):
        dx, dy, distance_x, distance_y = self.get_player_distance(owner, player)
        self._move_horizontally(owner, dx, self.speed)
        self._move_vertically(owner, dy)

    def run_toward_player(self, owner, player):
        dx, dy, distance_x, distance_y = self.get_player_distance(owner, player)
        self._move_horizontally(owner, dx, self.run_speed)
        self._move_vertically(owner, dy)

    def _move_horizontally(self, owner, dx, speed):
        if dx > 0:
            move_x(owner, 1, speed)
        elif dx < 0:
            move_x(owner, -1, speed)

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

    # --- Flank navigation ---

    def has_flank_target(self):
        return self.flank_target_side is not None

    def update_flank_target(self, owner, player, enemies):
        if self._flank_decision_remaining > 0 and self.flank_target_side:
            return

        left_count = sum(
            1 for e in enemies
            if e is not owner
            and e.state not in [e.DEAD, e.GRABBED, e.THROWN, e.KNOCKDOWN]
            and e.x < player.x
        )
        right_count = sum(
            1 for e in enemies
            if e is not owner
            and e.state not in [e.DEAD, e.GRABBED, e.THROWN, e.KNOCKDOWN]
            and e.x >= player.x
        )

        self.flank_target_side = "left" if left_count <= right_count else "right"
        same_side_count = left_count if self.flank_target_side == "left" else right_count
        self._flank_target_y_offset = -self._flank_offset_y if same_side_count % 2 == 0 else self._flank_offset_y
        self._flank_decision_remaining = self._flank_decision_duration

    def get_flank_position(self, player):
        target_y = player.y + self._flank_target_y_offset
        if self.flank_target_side == "left":
            return player.x - self._flank_offset_x, target_y
        return player.x + self._flank_offset_x, target_y

    def clear_flank_target(self):
        self.flank_target_side = None
        self._flank_target_y_offset = 0
        self._flank_decision_remaining = 0

    def move_toward_position(self, owner, position):
        target_x, target_y = position
        self._move_toward_point(owner, target_x, target_y)

    def _move_toward_point(self, owner, target_x, target_y):
        if abs(owner.x - target_x) > self.speed:
            if owner.x < target_x:
                move_x(owner, 1, self.speed)
            else:
                move_x(owner, -1, self.speed)

        # Slightly slower vertical correction makes flanking look more organic.
        if abs(owner.y - target_y) > self.y_speed:
            if owner.y < target_y:
                owner.y += self.y_speed * FLANK_VERTICAL_SPEED_SCALE
            else:
                owner.y -= self.y_speed * FLANK_VERTICAL_SPEED_SCALE

    # --- Air ---

    def start_jump(self):
        self.air_state.start_jump()

    def update_jump(self):
        self.air_state.update()

    def tick_air_cooldown(self):
        self.air_state.tick_cooldown()

    def get_jump_visual_y_offset(self):
        return self.air_state.get_visual_y_offset()

    def apply_world_bounds(self, owner, world_width=None, lane_top=None, lane_bottom=None):
        clamp_to_world_and_lane(
            owner,
            world_width,
            lane_top,
            lane_bottom,
            half_width=owner.geometry.collision_box_w // 2,
            owner_name="Enemy",
        )
