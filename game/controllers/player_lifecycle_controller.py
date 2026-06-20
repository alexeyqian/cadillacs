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
        owner.hit_reaction_controller.reset()
        owner.state_machine.change_to(owner, owner.IDLE)
        owner.facing_right = True

    def update_dead_state(self, owner):
        self.update_respawn(owner)

    def take_damage(self, owner, damage, reaction=None):
        if owner.state == owner.DEAD:
            return

        # Enemy lands hit -> player attack is canceled
        # Enemy lands hit -> combo step resets
        # Enemy lands hit -> grabbed enemy is released
        # Player must restart pressure after recovering
        owner.combat_controller.cancel_attack()
        owner.movement.cancel_run_attack_momentum()
        owner.movement.cancel_combo_finisher_nudge()
        owner.grab_controller.grabbed_enemy = None

        owner.health.take_damage(damage)
        owner.state_machine.change_to(owner, owner.HIT)

        if owner.health.is_dead():
            self.lose_life()
            self.lost_life(owner)
            return

        owner.hit_reaction_controller.start_hit_stun(reaction)

    def lost_life(self, owner):
        owner.state_machine.change_to(owner, owner.DEAD)

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
        owner.hit_reaction_controller.reset()
        self.reset_position_and_movement(owner, self.respawn_x, self.respawn_y)
        owner.state_machine.change_to(owner, owner.IDLE)
        owner.combat_controller.is_attacking = False
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
        owner.movement.cancel_run_attack_momentum()
        owner.movement.cancel_combo_finisher_nudge()
