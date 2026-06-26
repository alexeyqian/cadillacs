class PlayerLifecycleController:
    def __init__(self):
        pass

    def advance_timers(self, owner):
        ls = owner.lifecycle_state
        if ls.lives > 0 and ls.respawn_remaining > 0:
            ls.respawn_remaining -= 1

    def reset_for_stage_start(self, owner, x, y):
        ls = owner.lifecycle_state
        ls.respawn_x = x
        ls.respawn_y = y
        self.reset_position_and_movement(owner, x, y)
        owner.reaction_controller.reset(owner)
        owner.state_machine.change_to(owner, owner.IDLE)
        owner.facing_right = True

    def update_respawn(self, owner):
        if owner.state != owner.DEAD:
            return
        ls = owner.lifecycle_state
        if ls.lives <= 0:
            return
        self.advance_timers(owner)
        if self.is_respawn_ready(owner):
            self.respawn(owner)

    def respawn(self, owner):
        ls = owner.lifecycle_state
        owner.health.hp = owner.health.max_hp
        ls.respawn_remaining = 0
        owner.reaction_controller.reset(owner)
        self.reset_position_and_movement(owner, ls.respawn_x, ls.respawn_y)
        owner.state_machine.change_to(owner, owner.IDLE)
        owner._cancel_combat_commitment()

    def enter_dead_state(self, owner):
        owner.state_machine.change_to(owner, owner.DEAD)

    def gain_life(self, owner):
        owner.lifecycle_state.lives += 1

    def lose_life(self, owner):
        ls = owner.lifecycle_state
        ls.lives -= 1
        ls.respawn_remaining = 90

    def is_respawn_ready(self, owner):
        ls = owner.lifecycle_state
        return ls.lives > 0 and ls.respawn_remaining <= 0

    def reset_position_and_movement(self, owner, x, y):
        owner.x = x
        owner.y = y
        owner.movement.is_jumping = False
        if owner.movement.air:
            owner.movement.air.reset()
        owner.movement.attack_movement.cancel_run_attack_momentum()
        owner.movement.attack_movement.cancel_combo_finisher_nudge()
