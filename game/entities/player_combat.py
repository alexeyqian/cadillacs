from game.settings import FIST_DAMAGE, PLAYER_GRAB_KNEE_DAMAGE


# TODO: attack buffering, counter-hit, clash/parry, and attack configs 
class PlayerCombat:
    def __init__(self):
        self.is_attacking = False
        self.attack_timer = 0
        self.attack_duration = 12
        self.already_hit_enemy = False

        # classic combo system
        # J punch 1, J punch 2, J punch 3
        self.combo_step = 0
        self.combo_timer = 0
        # add a short lockout after ATTACK_3, 
        # so the finisher cannot immediately loop back into ATTACK_1.
        # expected feel: ATTACK_1 -> ATTACK_2 -> ATTACK_3 -> tiny recovery pause
        self.attack_recovery_timer = 0
        self.third_hit_recovery_duration = 10

    def update_timers(self, owner):
        if self.attack_recovery_timer > 0:
            self.attack_recovery_timer -= 1

        if self.combo_timer > 0:
            self.combo_timer -= 1
        else:
            self.combo_step = 0

        if self.is_attacking:
            self.attack_timer -= 1
            if self.attack_timer <= 0:
                finished_state = owner.state
                self.is_attacking = False

                if finished_state == owner.ATTACK_3:
                    self.attack_recovery_timer = self.third_hit_recovery_duration
                    self.combo_timer = 0
                    self.combo_step = 0

                if owner.state != owner.DEAD:
                    owner.state_machine.change_to(owner, owner.IDLE)

    def start_attack(self, owner):
        if self.is_attacking:
            return
        if self.attack_recovery_timer > 0:
            return

        self.is_attacking = True
        self.attack_timer = self.attack_duration
        self.already_hit_enemy = False

        if owner.movement.is_running:
            self.attack_timer = owner.run_attack_duration
            self.combo_timer = 0
            self.combo_step = 0
            owner.state_machine.change_to(owner, owner.RUN_ATTACK)
            return

        if self.combo_timer > 0:
            self.combo_step += 1
        else:
            self.combo_step = 1

        self.combo_step = min(self.combo_step, 3)
        self.combo_timer = 30 # TODO: adjust timer

        if self.combo_step == 1:
            owner.state_machine.change_to(owner, owner.ATTACK_1)
        elif self.combo_step == 2:
            owner.state_machine.change_to(owner, owner.ATTACK_2)
        else:
            owner.state_machine.change_to(owner, owner.ATTACK_3)

    def start_jump_attack(self, owner):
        if not owner.movement.is_jumping:
            return
        if self.is_attacking:
            return

        self.is_attacking = True
        self.attack_timer = owner.jump_attack_duration
        self.already_hit_enemy = False
        owner.state_machine.change_to(owner, owner.JUMP_ATTACK)

    def start_grab_knee_attack(self, owner):
        if not owner.grab.grabbed_enemy:
            return
        if self.is_attacking:
            return

        self.is_attacking = True
        self.attack_timer = owner.grab.grab_knee_duration
        owner.grab.grab_knee_timer = owner.grab.grab_knee_duration
        self.already_hit_enemy = False
        owner.state_machine.change_to(owner, owner.GRAB_KNEE)

    def attack_damage(self, owner):
        base_damage = FIST_DAMAGE

        if owner.state == owner.ATTACK_1:
            base_damage = FIST_DAMAGE - 2
        elif owner.state == owner.ATTACK_2:
            base_damage = FIST_DAMAGE
        elif owner.state == owner.ATTACK_3:
            base_damage = FIST_DAMAGE + 4
        elif owner.state == owner.RUN_ATTACK:
            base_damage = FIST_DAMAGE
        elif owner.state == owner.JUMP_ATTACK:
            base_damage = FIST_DAMAGE
        elif owner.state == owner.GRAB_KNEE:
            base_damage = PLAYER_GRAB_KNEE_DAMAGE

        weapon = owner.weapon_slot.weapon
        if weapon and not weapon.is_ranged:
            base_damage += weapon.damage

        return int(base_damage)
