from game.settings import FIST_DAMAGE
from game.entities.attack_data import (
    PLAYER_CLASH_RECOVERY,
    PLAYER_COMBO_WINDOW,
    PLAYER_COUNTER_HIT_STUN_BONUS,
    get_player_attack_data,
)
from game.entities.attack_controller import AttackController

# TODO: attack buffering, counter-hit, clash/parry, and attack configs 
class PlayerCombatController:
    def __init__(self):
        self.attack_controller = AttackController()

        # classic combo system
        # J punch 1, J punch 2, J punch 3
        self.combo_step = 0
        self.combo_window_remaining = 0
        # add a short lockout after ATTACK_3, 
        # so the finisher cannot immediately loop back into ATTACK_1.
        # expected feel: ATTACK_1 -> ATTACK_2 -> ATTACK_3 -> tiny recovery pause
        self.action_lock_remaining = 0

        # make clash create a tiny recovery pause 
        # where the player cannot attack again instantly.
        self.clash_recovery_duration = PLAYER_CLASH_RECOVERY
        # add a short recovery after a knee so the player cannot mash knee as freely.
        self.grab_knee_recovery_duration = 6

    @property
    def is_attacking(self):
        return self.attack_controller.is_attacking

    @is_attacking.setter
    def is_attacking(self, value):
        if not value:
            self.attack_controller.cancel()

    @property
    def attack_timer(self):
        return self.attack_controller.attack_timer

    @property
    def attack_remaining(self):
        return self.attack_controller.attack_remaining

    @attack_remaining.setter
    def attack_remaining(self, value):
        # Kept only for old callers during the migration.
        if value <= 0:
            self.attack_controller.cancel()

    @property
    def attack_connected(self):
        return self.attack_controller.attack_connected

    @attack_connected.setter
    def attack_connected(self, value):
        self.attack_controller.attack_connected = value

    @property
    def current_attack_name(self):
        return self.attack_controller.current_attack_name

    def mark_attack_connected(self):
        self.attack_controller.mark_connected()

    def mark_attack_hit(self, target):
        self.attack_controller.mark_target_hit(target)

    def can_hit_target(self, target):
        return self.attack_controller.can_hit_target(target)

    def can_hit_more_targets(self):
        return self.attack_controller.can_hit_more_targets()

    def is_attack_active(self):
        return self.attack_controller.is_active()

    def get_attack_phase_name(self):
        return self.attack_controller.get_phase_name()

    def get_attack_timing_label(self):
        return self.attack_controller.get_timing_label()

    def get_active_hitbox_data(self):
        if not self.is_attack_active():
            return None
        attack = self.attack_controller.current_attack
        if not attack or not attack.hitboxes:
            return None
        return attack.hitboxes[0]

    def get_active_counter_hurtbox_data(self):
        if not self.is_attack_active():
            return None
        attack = self.attack_controller.current_attack
        if not attack or not attack.counter_hurtboxes:
            return None
        return attack.counter_hurtboxes[0]

    # Avoiding the combo step advances when the player presses attack inside the combo window, 
    # even if the previous punch hit nothing. 
    # That means the player can “charge” into ATTACK_3 by punching air, 
    # then walk in and land the stronger hit. 
    # The combo damage has to be earned.
    def update_timers(self, owner):
        # action lock remaining means: the player cannot start a new action yet.
        if self.action_lock_remaining > 0:
            self.action_lock_remaining -= 1
            if owner.state == owner.RECOIL:
                if self.action_lock_remaining <= 0:
                    owner.state_machine.change_to(owner, owner.IDLE)
                # Why return?
                # During recoil, we do not want combo timers or attack ending logic to also manipulate state.
                # expected behavior:
                # Clash -> player enters RECOIL
                # Player stays RECOIL for clash recovery duration
                # Then returns to IDLE
                return

        if self.combo_window_remaining > 0:
            self.combo_window_remaining -= 1
        else:
            self.combo_step = 0

        if self.is_attacking:
            if self.attack_controller.advance():
                finished_attack_name, finished_move, attack_connected = (
                    self.attack_controller.finish()
                )

                # expected behavior:
                # Punch hits enemy -> combo can continue
                # Punch misses enemy -> combo resets
                # Player cannot build third hit by punching empty space
                attack_missed = (
                    finished_attack_name in [owner.ATTACK_1, owner.ATTACK_2, owner.ATTACK_3]
                    and not attack_connected
                )
                if attack_missed:
                    self.combo_window_remaining = 0
                    self.combo_step = 0

                if finished_move and finished_move.action_lock > 0:
                    self.action_lock_remaining = finished_move.action_lock
                    self.combo_window_remaining = 0
                    self.combo_step = 0

                if owner.state != owner.DEAD:
                    owner.state_machine.change_to(owner, owner.IDLE)

    def start_attack(self, owner):
        if self.is_attacking:
            return
        if self.action_lock_remaining > 0:
            return

        if owner.movement.is_running:
            move_data = self.get_attack_data(owner, owner.RUN_ATTACK)
            self.attack_controller.start(owner.RUN_ATTACK, move_data)
            owner.movement.start_run_attack_momentum(owner)
            self.combo_window_remaining = 0
            self.combo_step = 0
            owner.state_machine.change_to(owner, owner.RUN_ATTACK)
            return

        if self.combo_window_remaining > 0:
            self.combo_step += 1
        else:
            self.combo_step = 1

        self.combo_step = min(self.combo_step, 3)
        if self.combo_step == 1:
            owner.state_machine.change_to(owner, owner.ATTACK_1)
        elif self.combo_step == 2:
            owner.state_machine.change_to(owner, owner.ATTACK_2)
        else:
            owner.state_machine.change_to(owner, owner.ATTACK_3)

        move_data = self.get_attack_data(owner, owner.state)
        self.attack_controller.start(owner.state, move_data)
        self.combo_window_remaining = move_data.combo_window if move_data else PLAYER_COMBO_WINDOW

    def start_jump_attack(self, owner):
        if not owner.movement.is_jumping:
            return
        if self.is_attacking:
            return

        move_data = self.get_attack_data(owner, owner.JUMP_ATTACK)
        self.attack_controller.start(owner.JUMP_ATTACK, move_data)
        owner.state_machine.change_to(owner, owner.JUMP_ATTACK)

    def start_grab_knee_attack(self, owner):
        if not owner.grab.grabbed_enemy:
            return
        if self.is_attacking:
            return

        move_data = self.get_attack_data(owner, owner.GRAB_KNEE)
        self.attack_controller.start(owner.GRAB_KNEE, move_data)
        owner.grab.grab_knee_remaining = owner.grab.grab_knee_duration
        owner.state_machine.change_to(owner, owner.GRAB_KNEE)

    def start_clash_recovery(self, owner):
        self.cancel_attack()
        self.action_lock_remaining = self.clash_recovery_duration
        owner.state_machine.change_to(owner, owner.RECOIL)

    # enemy hits should fully cancel the player’s combo.
    def cancel_attack(self):
        self.attack_controller.cancel()
        self.combo_step = 0
        self.combo_window_remaining = 0
        self.action_lock_remaining = 0

    def get_attack_damage(self, owner):
        attack_data = self.get_current_or_state_attack_data(owner)
        if not attack_data:
            return int(FIST_DAMAGE)

        return int(attack_data.damage)
    
    def get_attack_lane_reach(self, owner):
        attack_data = self.get_current_or_state_attack_data(owner)
        return attack_data.lane_reach if attack_data else 0

    def get_attack_knockback_velocity(self, owner):
        attack_data = self.get_current_or_state_attack_data(owner)
        return attack_data.knockback_velocity if attack_data else 10

    def get_attack_enemy_hit_stun_duration(self, owner):
        attack_data = self.get_current_or_state_attack_data(owner)
        return attack_data.enemy_hit_stun_duration if attack_data else 15

    def get_current_or_state_attack_data(self, owner):
        if self.attack_controller.current_attack:
            return self.attack_controller.current_attack
        return self.get_attack_data(owner, owner.state)

    def get_attack_data(self, owner, attack_name):
        weapon_slot = getattr(owner, "weapon_slot", None)
        weapon = getattr(weapon_slot, "weapon", None)
        return get_player_attack_data(attack_name, weapon)
