from game.settings import PLAYER_GRAB_KNEE_DURATION, PLAYER_GRAB_KNEE_HIT_FRAME, PLAYER_GRAB_RANGE

# grab/throw/knee
class PlayerGrabController:
    def __init__(self):
        self.grabbed_enemy = None
        self.grab_pressed = False
        self.grab_range = PLAYER_GRAB_RANGE
        # failed heavy grab causes a tiny recovery and slightly punishable.
        self.failed_grab_recovery_duration = 8
        self.failed_grab_feedback = False

        self.throw_remaining = 0
        self.throw_duration = 14

        self.grab_knee_remaining = 0
        self.grab_knee_duration = PLAYER_GRAB_KNEE_DURATION
        self.grab_knee_hit_frame = PLAYER_GRAB_KNEE_HIT_FRAME

    def advance_timers(self, owner):
        if self.throw_remaining > 0:
            self.throw_remaining -= 1

        if self.grab_knee_remaining > 0:
            self.grab_knee_remaining -= 1
            if self.grab_knee_remaining <= 0:
                owner._end_grab_knee()

                if self.grabbed_enemy:
                    owner.state_machine.change_to(owner, owner.GRAB)
                else:
                    owner.state_machine.change_to(owner, owner.IDLE)

    # keep grabbed enemy in front of player
    def update_grabbed_enemy_position(self, owner):
        if not self.grabbed_enemy:
            return

        grabbed_width = self.grabbed_enemy.geometry.collision_box_w
        grab_offset = (owner.geometry.collision_box_w + grabbed_width) / 2 + 5

        if owner.facing_right:
            self.grabbed_enemy.x = owner.x + grab_offset
        else:
            self.grabbed_enemy.x = owner.x - grab_offset

        self.grabbed_enemy.y = owner.y

    def can_grab_enemy(self, owner, enemy, level):
        if enemy.state == enemy.DEAD:
            return False
        if enemy.state == enemy.GRABBED:
            return False
        # make heavy enemies harder to grab from the front.
        # todo: use archtype heavy instead of enemy id
        if enemy.enemy_id == "black_elmer":
            player_is_behind_enemy = owner.facing_right == enemy.facing_right
            if not player_is_behind_enemy:
                self.fail_heavy_grab(owner)
                return False

        dx = abs(enemy.x - owner.x)
        lane_distance = level.get_lane_distance(owner.y, enemy.y)
        return dx <= self.grab_range and lane_distance == 0

    def fail_heavy_grab(self, owner):
        # punish for 8 game frames if grab fails on heavy enemy in front
        owner._set_action_lock(self.failed_grab_recovery_duration)
        # failed grab read as a small bounce-off.
        owner.state_machine.change_to(owner, owner.RECOIL)
        # Small edge case: after a failed heavy grab,
        # the player may still be holding L,
        # and grab_pressed can make the next grab attempt feel unresponsive until release.
        # Failed grab consumes the grab press
        # Player must release and press L again for another grab attempt
        self.grab_pressed = True
        self.failed_grab_feedback = True

    def grab_enemy(self, owner, enemy):
        self.grabbed_enemy = enemy
        enemy.grabbed_by_player()
        owner.state_machine.change_to(owner, owner.GRAB)

    def throw_grabbed_enemy(self, owner):
        if self.grabbed_enemy is None:
            return

        direction = 1
        if not owner.facing_right:
            direction = -1

        throw_attack = owner.get_attack_data(owner.THROW)
        throw_damage = throw_attack.damage
        self.grabbed_enemy.thrown_by_player(direction, throw_damage)
        self.grabbed_enemy = None

        self.throw_remaining = self.throw_duration
        owner.state_machine.change_to(owner, owner.THROW)
