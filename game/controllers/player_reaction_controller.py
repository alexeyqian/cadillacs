class PlayerReactionController:
    def take_damage(self, owner, damage, reaction=None):
        if owner.state == owner.DEAD:
            return

        self.cancel_combat_commitment(owner)
        owner.health.take_damage(damage)
        owner.state_machine.change_to(owner, owner.HIT)

        if owner.health.is_dead():
            owner.lifecycle_controller.lose_life()
            owner.lifecycle_controller.enter_dead_state(owner)
            return

        owner.hit_reaction_controller.start_hit_stun(reaction)

    def cancel_combat_commitment(self, owner):
        # Enemy lands hit -> player attack is canceled
        # Enemy lands hit -> combo step resets
        # Enemy lands hit -> grabbed enemy is released
        # Player must restart pressure after recovering
        owner.combat_controller.cancel_attack()
        owner.movement.cancel_run_attack_momentum()
        owner.movement.cancel_combo_finisher_nudge()
        owner.grab_controller.grabbed_enemy = None
