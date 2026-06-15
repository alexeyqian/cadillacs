class PlayerLifecycle:
    def __init__(self, respawn_x, respawn_y):
        self.respawn_x = respawn_x
        self.respawn_y = respawn_y

    def update_dead_state(self, owner):
        self.update_respawn(owner)
        owner.animation_controller.update(owner)

    def update_hit_state(self, owner):
        if owner.health.hit_timer <= 0:
            return False

        still_in_hit_stun = owner.health.update_hit_timer()
        if still_in_hit_stun:
            owner.state_machine.change_to(owner, owner.HIT)
        else:
            owner.state_machine.change_to(owner, owner.IDLE)

        owner.animation_controller.update(owner)
        return True

    def take_damage(self, owner, damage):
        if owner.state == owner.DEAD:
            return

        # Enemy lands hit -> player attack is canceled
        # Enemy lands hit -> combo step resets
        # Enemy lands hit -> grabbed enemy is released
        # Player must restart pressure after recovering
        owner.combat.cancel_attack()
        owner.grab.grabbed_enemy = None

        lost_life = owner.health.take_damage(damage)
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
        if owner.health.update_respawn_timer():
            self.respawn(owner)

    def respawn(self, owner):
        owner.health.reset_for_respawn()
        owner.x = self.respawn_x
        owner.y = self.respawn_y
        owner.movement.ground_y = self.respawn_y
        owner.movement.vx = 0
        owner.movement.vy = 0
        owner.movement.is_jumping = False
        owner.state_machine.change_to(owner, owner.IDLE)
        owner.combat.is_attacking = False
        owner.grab.grabbed_enemy = None