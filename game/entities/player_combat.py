from game.settings import FIST_DAMAGE, PLAYER_GRAB_KNEE_DAMAGE
PLAYER_MOVE_DAMAGE = {
    "ATTACK_1": FIST_DAMAGE - 2,
    "ATTACK_2": FIST_DAMAGE,
    "ATTACK_3": FIST_DAMAGE + 4,
    "RUN_ATTACK": FIST_DAMAGE,
    "JUMP_ATTACK": FIST_DAMAGE,
    "GRAB_KNEE": PLAYER_GRAB_KNEE_DAMAGE,
}
PLAYER_COMBO_WINDOW = 30
PLAYER_THIRD_HIT_RECOVERY = 10
PLAYER_CLASH_RECOVERY = 8

# TODO: attack buffering, counter-hit, clash/parry, and attack configs 
class PlayerCombat:
    def __init__(self):
        self.is_attacking = False
        self.attack_timer = 0
        self.attack_duration = 12
        self.attack_connected = False

        # classic combo system
        # J punch 1, J punch 2, J punch 3
        self.combo_step = 0
        self.combo_timer = 0
        # add a short lockout after ATTACK_3, 
        # so the finisher cannot immediately loop back into ATTACK_1.
        # expected feel: ATTACK_1 -> ATTACK_2 -> ATTACK_3 -> tiny recovery pause
        self.action_lock_timer = 0
        self.third_hit_recovery_duration = PLAYER_THIRD_HIT_RECOVERY
        # make clash create a tiny recovery pause 
        # where the player cannot attack again instantly.
        self.clash_recovery_duration = PLAYER_CLASH_RECOVERY

    # Avoiding the combo step advances when the player presses attack inside the combo timer, 
    # even if the previous punch hit nothing. 
    # That means the player can “charge” into ATTACK_3 by punching air, 
    # then walk in and land the stronger hit. 
    # The combo damage has to be earned.
    def update_timers(self, owner):
        # action lock timer means:  the player cannot start a new action yet.
        if self.action_lock_timer > 0:
            self.action_lock_timer -= 1
            if owner.state == owner.RECOIL:
                if self.action_lock_timer <= 0:
                    owner.state_machine.change_to(owner, owner.IDLE)
                # Why return?
                # During recoil, we do not want combo timers or attack ending logic to also manipulate state.
                # expected behavior:
                # Clash -> player enters RECOIL
                # Player stays RECOIL for clash recovery duration
                # Then returns to IDLE
                return

        if self.combo_timer > 0:
            self.combo_timer -= 1
        else:
            self.combo_step = 0

        if self.is_attacking:
            self.attack_timer -= 1
            if self.attack_timer <= 0:
                finished_state = owner.state

                # expected behavior:
                # Punch hits enemy -> combo can continue
                # Punch misses enemy -> combo resets
                # Player cannot build third hit by punching empty space
                attack_missed = (
                    finished_state in [owner.ATTACK_1, owner.ATTACK_2, owner.ATTACK_3]
                    and not self.attack_connected
                )
                if attack_missed:
                    self.combo_timer = 0
                    self.combo_step = 0

                self.is_attacking = False

                if finished_state == owner.ATTACK_3:
                    self.action_lock_timer = self.third_hit_recovery_duration
                    self.combo_timer = 0
                    self.combo_step = 0

                if owner.state != owner.DEAD:
                    owner.state_machine.change_to(owner, owner.IDLE)

    def start_attack(self, owner):
        if self.is_attacking:
            return
        if self.action_lock_timer > 0:
            return

        self.is_attacking = True
        self.attack_timer = self.attack_duration
        self.attack_connected = False

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
        self.combo_timer = PLAYER_COMBO_WINDOW

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
        self.attack_connected = False
        owner.state_machine.change_to(owner, owner.JUMP_ATTACK)

    def start_grab_knee_attack(self, owner):
        if not owner.grab.grabbed_enemy:
            return
        if self.is_attacking:
            return

        self.is_attacking = True
        self.attack_timer = owner.grab.grab_knee_duration
        owner.grab.grab_knee_timer = owner.grab.grab_knee_duration
        self.attack_connected = False
        owner.state_machine.change_to(owner, owner.GRAB_KNEE)

    def start_clash_recovery(self, owner):
        self.cancel_attack()
        self.action_lock_timer = self.clash_recovery_duration
        owner.state_machine.change_to(owner, owner.RECOIL)

    # enemy hits should fully cancel the player’s combo.
    def cancel_attack(self):
        self.is_attacking = False
        self.attack_timer = 0
        self.attack_connected = False
        self.combo_step = 0
        self.combo_timer = 0
        self.action_lock_timer = 0

    def get_attack_damage(self, owner):
        base_damage = PLAYER_MOVE_DAMAGE.get(owner.state, FIST_DAMAGE)

        weapon = owner.weapon_slot.weapon
        if weapon and not weapon.is_ranged:
            base_damage += weapon.damage

        return int(base_damage)
