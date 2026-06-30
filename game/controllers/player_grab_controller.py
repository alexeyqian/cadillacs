# grab/throw/knee
class PlayerGrabController:
    def __init__(self):
        pass

    def advance_timers(self, owner):
        gs = owner.grab_state
        if gs.throw_remaining > 0:
            gs.throw_remaining -= 1

        if gs.grab_knee_remaining > 0:
            gs.grab_knee_remaining -= 1
            if gs.grab_knee_remaining <= 0:
                owner._end_grab_knee()

                if gs.grabbed_enemy:
                    owner.state_machine.change_to(owner, owner.GRAB)
                else:
                    owner.state_machine.change_to(owner, owner.IDLE)

    # keep grabbed enemy in front of player
    def update_grabbed_enemy_position(self, owner):
        gs = owner.grab_state
        if not gs.grabbed_enemy:
            return

        grabbed_width = gs.grabbed_enemy.geometry.collision_box_w
        grab_offset = (owner.geometry.collision_box_w + grabbed_width) / 2 + 5

        if owner.facing_right:
            gs.grabbed_enemy.x = owner.x + grab_offset
        else:
            gs.grabbed_enemy.x = owner.x - grab_offset

        gs.grabbed_enemy.y = owner.y

    def can_grab_enemy(self, owner, enemy, level):
        gs = owner.grab_state
        if enemy.state == enemy.DEAD:
            return False
        if enemy.state == enemy.GRABBED:
            return False
        # make heavy enemies harder to grab from the front.
        if enemy.enemy_id == "black_elmer":
            player_is_behind_enemy = owner.facing_right == enemy.facing_right
            if not player_is_behind_enemy:
                self.fail_heavy_grab(owner)
                return False

        dx = abs(enemy.x - owner.x)
        lane_distance = level.get_lane_distance(owner.y, enemy.y)
        return dx <= gs.grab_range and lane_distance == 0

    def fail_heavy_grab(self, owner):
        gs = owner.grab_state
        owner._set_action_lock(gs.failed_grab_recovery_duration)
        owner.state_machine.change_to(owner, owner.RECOIL)
        gs.grab_pressed = True
        gs.failed_grab_feedback = True

    def is_throwing(self, owner):
        return owner.grab_state.throw_remaining > 0

    def is_grab_kneeing(self, owner):
        return owner.grab_state.grab_knee_remaining > 0

    def grab_enemy(self, owner, enemy):
        owner.grab_state.grabbed_enemy = enemy
        enemy.grabbed_by_player()
        owner.state_machine.change_to(owner, owner.GRAB)

    def throw_grabbed_enemy(self, owner):
        gs = owner.grab_state
        if gs.grabbed_enemy is None:
            return

        direction = 1
        if not owner.facing_right:
            direction = -1

        throw_attack = owner.get_attack_data(owner.THROW)
        throw_damage = throw_attack.damage
        gs.grabbed_enemy.thrown_by_player(direction, throw_damage)
        gs.grabbed_enemy = None

        gs.throw_remaining = gs.throw_duration
        owner.state_machine.change_to(owner, owner.THROW)
