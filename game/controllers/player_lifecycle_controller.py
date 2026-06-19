class PlayerLifecycleController:
    def __init__(self, respawn_x, respawn_y):
        self.respawn_x = respawn_x
        self.respawn_y = respawn_y

    def reset_for_stage_start(self, owner, x, y):
        self.respawn_x = x
        self.respawn_y = y
        self.reset_position_and_movement(owner, x, y)
        owner.state_machine.change_to(owner, owner.IDLE)
        owner.facing_right = True

    def update_dead_state(self, owner):
        self.update_respawn(owner)
        owner.animation_controller.update(owner)

    def update_hit_state(self, owner):
        if owner.health.hit_stun_remaining <= 0:
            return False

        still_in_hit_stun = owner.health.update_hit_stun()
        if still_in_hit_stun:
            owner.state_machine.change_to(owner, owner.HIT)
        else:
            owner.state_machine.change_to(owner, owner.IDLE)

        owner.animation_controller.update(owner)
        return True

    def take_damage(self, owner, damage, reaction=None, hit_stun_bonus=0):
        if owner.state == owner.DEAD:
            return

        # Enemy lands hit -> player attack is canceled
        # Enemy lands hit -> combo step resets
        # Enemy lands hit -> grabbed enemy is released
        # Player must restart pressure after recovering
        owner.combat_controller.cancel_attack()
        owner.movement.cancel_run_attack_momentum()
        owner.movement.cancel_attack_nudge()
        owner.grab_controller.grabbed_enemy = None

        lost_life = owner.health.take_damage(
            damage,
            reaction=reaction,
            hit_stun_bonus=hit_stun_bonus,
        )
        owner.state_machine.change_to(owner, owner.HIT)

        if lost_life:
            self.lost_life(owner)

    def lost_life(self, owner):
        owner.state_machine.change_to(owner, owner.DEAD)

    def update_respawn(self, owner):
        if owner.state != owner.DEAD:
            return
        if owner.health.lives <= 0:
            return
        if owner.health.update_respawn():
            self.respawn(owner)

    def respawn(self, owner):
        owner.health.reset_for_respawn()
        self.reset_position_and_movement(owner, self.respawn_x, self.respawn_y)
        owner.state_machine.change_to(owner, owner.IDLE)
        owner.combat_controller.is_attacking = False
        owner.grab_controller.grabbed_enemy = None

    def reset_position_and_movement(self, owner, x, y):
        owner.x = x
        owner.y = y
        owner.movement.ground_y = y
        owner.movement.vx = 0
        owner.movement.vy = 0
        owner.movement.is_jumping = False
        if owner.air:
            owner.air.reset()
        owner.movement.cancel_run_attack_momentum()
        owner.movement.cancel_attack_nudge()
