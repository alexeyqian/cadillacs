from game.components.movement_math import (
    clamp_to_world_and_lane,
    face_toward_x,
    get_distance_to,
    move_x,
)
from game.components.enemy_air_state import EnemyAirState
from game.components.enemy_flank_state import EnemyFlankState
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
        self.run_speed = speed
        self.can_run = False
        self.can_run_attack = False
        self.can_jump = False
        self.can_jump_attack = False

        self.detect_range = detect_range
        self.patrol_distance = patrol_distance
        self.patrol_direction = patrol_direction
        self.patrol_center_x = 0  # set to enemy's spawn x when the enemy is placed

        self.air_state = EnemyAirState()
        self.flank_state = EnemyFlankState()

    @property
    def is_jumping(self):
        return self.air_state.is_jumping

    def configure(self, speed, patrol_distance, detect_range, 
                can_run=False, run_speed=None, can_jump=False,
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
        self.flank_state.advance_timer()

    # --- Chase / patrol ---

    def get_player_distance(self, owner, player):
        return get_distance_to(owner, player)

    def face_player(self, owner, player):
        face_toward_x(owner, player.x)

    def patrol(self, owner):
        owner.x += self.patrol_direction
        owner.facing_right = self.patrol_direction > 0
        if owner.x > self.patrol_center_x + self.patrol_distance:
            self.patrol_direction = -1
        if owner.x < self.patrol_center_x - self.patrol_distance:
            self.patrol_direction = 1

    def move_toward_player(self, owner, player):
        dx, dy, distance_x, distance_y = get_distance_to(owner, player)
        if dx > 0:
            move_x(owner, 1, self.speed)
        elif dx < 0:
            move_x(owner, -1, self.speed)
        if abs(dy) > CHASE_VERTICAL_DEAD_ZONE:
            owner.y += self.y_speed if dy > 0 else -self.y_speed

    def run_toward_player(self, owner, player):
        dx, dy, distance_x, distance_y = get_distance_to(owner, player)
        if dx > 0:
            move_x(owner, 1, self.run_speed)
        elif dx < 0:
            move_x(owner, -1, self.run_speed)
        if abs(dy) > CHASE_VERTICAL_DEAD_ZONE:
            owner.y += self.y_speed if dy > 0 else -self.y_speed

    def separate_from_enemies(self, owner, enemies):
        for other in enemies:
            if other is owner or other.state == owner.DEAD:
                continue
            dx = other.x - owner.x
            if abs(dx) < SEPARATION_DISTANCE:
                owner.x += -SEPARATION_PUSH if dx > 0 else SEPARATION_PUSH

    # --- Flank navigation ---

    def has_flank_target(self):
        return self.flank_state.has_target()

    @property
    def flank_target_side(self):
        return self.flank_state.target_side

    def update_flank_target(self, owner, player, enemies):
        self.flank_state.update(owner, player, enemies)

    def get_flank_position(self, player):
        return self.flank_state.get_position(player)

    def clear_flank_target(self):
        self.flank_state.clear()

    def move_toward_position(self, owner, position):
        target_x, target_y = position
        if abs(owner.x - target_x) > self.speed:
            move_x(owner, 1 if owner.x < target_x else -1, self.speed)
        # Slightly slower vertical correction makes flanking look more organic.
        if abs(owner.y - target_y) > self.y_speed:
            owner.y += self.y_speed * FLANK_VERTICAL_SPEED_SCALE if owner.y < target_y else -self.y_speed * FLANK_VERTICAL_SPEED_SCALE

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
