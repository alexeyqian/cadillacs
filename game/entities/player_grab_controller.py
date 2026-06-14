from game.settings import PLAYER_GRAB_KNEE_DURATION, PLAYER_GRAB_KNEE_HIT_FRAME


class PlayerGrabController:
    def __init__(self):
        self.grabbed_enemy = None
        self.grab_pressed = False

        self.throw_timer = 0
        self.throw_duration = 14

        self.grab_knee_timer = 0
        self.grab_knee_duration = PLAYER_GRAB_KNEE_DURATION
        self.grab_knee_hit_frame = PLAYER_GRAB_KNEE_HIT_FRAME

    def update_timers(self, owner):
        if self.throw_timer > 0:
            self.throw_timer -= 1

        if self.grab_knee_timer > 0:
            self.grab_knee_timer -= 1
            if self.grab_knee_timer <= 0:
                owner.is_attacking = False
                owner.already_hit_enemy = False

                if self.grabbed_enemy:
                    owner.state = owner.GRAB
                else:
                    owner.state = owner.IDLE

    # keep grabbed enemy in front of player
    def update_grabbed_enemy_position(self, owner):
        if not self.grabbed_enemy:
            return

        grabbed_width = self.grabbed_enemy.collision_box_w
        grab_offset = (owner.collision_box_w + grabbed_width) / 2 + 5

        if owner.facing_right:
            self.grabbed_enemy.x = owner.x + grab_offset
        else:
            self.grabbed_enemy.x = owner.x - grab_offset

        self.grabbed_enemy.y = owner.y

    def can_grab_enemy(self, owner, enemy):
        if enemy.state == enemy.DEAD:
            return False
        if enemy.state == enemy.GRABBED:
            return False

        dx = abs(enemy.x - owner.x)
        dy = abs(enemy.y - owner.y)
        return dx <= owner.grab_range and dy <= 40

    def grab_enemy(self, owner, enemy):
        self.grabbed_enemy = enemy
        enemy.grabbed_by_player()
        owner.state = owner.GRAB

    def throw_grabbed_enemy(self, owner):
        if self.grabbed_enemy is None:
            return

        direction = 1
        if not owner.facing_right:
            direction = -1

        self.grabbed_enemy.thrown_by_player(direction)
        self.grabbed_enemy = None

        self.throw_timer = self.throw_duration
        owner.state = owner.THROW