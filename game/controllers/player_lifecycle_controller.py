class PlayerLifecycleController:
    def __init__(self, respawn_x, respawn_y, lives):
        self.lives = lives
        self.respawn_x = respawn_x
        self.respawn_y = respawn_y
        self.respawn_remaining = 0

    def advance_timers(self):
        if self.lives > 0 and self.respawn_remaining > 0:
            self.respawn_remaining -= 1

    def reset_for_stage_start(self, owner, x, y):
        self.respawn_x = x
        self.respawn_y = y
        self.reset_position_and_movement(owner, x, y)
        owner.reaction_controller.reset()
        owner.state_machine.change_to(owner, owner.IDLE)
        owner.facing_right = True

    def update_respawn(self, owner):
        if owner.state != owner.DEAD:
            return
        if self.lives <= 0:
            return
        self.advance_timers()
        if self.is_respawn_ready():
            self.respawn(owner)

    def respawn(self, owner):
        owner.health.hp = owner.health.max_hp
        self.respawn_remaining = 0
        owner.reaction_controller.reset()
        self.reset_position_and_movement(owner, self.respawn_x, self.respawn_y)
        owner.state_machine.change_to(owner, owner.IDLE)
        owner.combat_controller.cancel_attack()
        owner.grab_controller.grabbed_enemy = None

    def gain_life(self):
        self.lives += 1

    def lose_life(self):
        self.lives -= 1
        self.respawn_remaining = 90

    def is_respawn_ready(self):
        return self.lives > 0 and self.respawn_remaining <= 0

    def reset_position_and_movement(self, owner, x, y):
        owner.x = x
        owner.y = y
        owner.movement.is_jumping = False
        if owner.air:
            owner.air.reset()
        owner.movement.attack_movement.cancel_run_attack_momentum()
        owner.movement.attack_movement.cancel_combo_finisher_nudge()
