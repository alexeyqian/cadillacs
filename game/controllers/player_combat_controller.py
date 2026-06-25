import game.settings as settings

from game.combat.attack_manager import AttackManager
from game.combat.player_attack_result import PlayerAttackResult

# TODO: attack buffering, clash/parry, and attack configs
class PlayerCombatController:
    def __init__(self):
        self.attack_manager = AttackManager()
        self.attack_result = PlayerAttackResult(self)
        self.attacks = {}
        self.weapon_attacks = {}

        # classic combo system
        # J punch 1, J punch 2, J punch 3
        self._combo_step = 0
        self._combo_window_remaining = 0
        # add a short lockout after ATTACK3,
        # so the finisher cannot immediately loop back into ATTACK.
        # expected feel: ATTACK -> ATTACK2 -> ATTACK3 -> tiny recovery pause
        self._action_lock_remaining = 0

        # make clash create a tiny recovery pause
        # where the player cannot attack again instantly.
        self.clash_recovery_duration = settings.PLAYER_CLASH_RECOVERY
        # add a short recovery after a knee so the player cannot mash knee as freely.
        self.grab_knee_recovery_duration = 6

    # --- State queries ---

    @property
    def is_attacking(self):
        return self.attack_manager.is_attacking

    @property
    def current_attack_name(self):
        return self.attack_manager.current_attack_name

    def get_active_hitbox_data(self):
        if not self.attack_manager.is_active():
            return None
        return self.attack_manager.current_attack

    def get_attack_data(self, owner):
        if self.attack_manager.current_attack:
            return self.attack_manager.current_attack
        return owner.get_attack_data(owner.state)

    def get_attack_damage(self, owner):
        attack_data = self.get_attack_data(owner)
        if not attack_data:
            return 0
        return attack_data.damage

    def get_attack_lane_reach(self, owner):
        attack_data = self.get_attack_data(owner)
        if not attack_data:
            return 0
        return attack_data.lane_reach

    def can_hit_target(self, target):
        return self.attack_manager.can_hit_target(target)

    def can_hit_more_targets(self):
        return self.attack_manager.can_hit_more_targets()

    def mark_attack_hit(self, target):
        self.attack_manager.mark_target_hit(target)

    # --- Per-frame updates ---

    # Avoiding the combo step advances when the player presses attack inside the combo window,
    # even if the previous punch hit nothing.
    # That means the player can "charge" into ATTACK3 by punching air,
    # then walk in and land the stronger hit.
    # The combo damage has to be earned.
    def advance_timers(self, owner):
        if self._tick_action_lock(owner):
            return
        self._tick_combo_window()

    def update_attack(self, owner):
        self._finish_attack_if_done(owner)

    # --- Attack starters ---

    def start_attack(self, owner):
        if self.is_attacking:
            return
        if self._action_lock_remaining > 0:
            return
        if self._can_start_run_attack(owner):
            self._start_run_attack(owner)
            return

        self._start_combo_attack(owner)

    def start_jump_attack(self, owner):
        if not owner.movement.is_jumping:
            return
        if owner.air and not owner.air.can_start_jump_attack():
            return
        if self.is_attacking:
            return

        move_data = owner.get_attack_data(owner.JUMP_ATTACK)
        self.attack_manager.start(owner.JUMP_ATTACK, move_data)
        if owner.air:
            owner.air.mark_jump_attack_used()
        owner.state_machine.change_to(owner, owner.JUMP_ATTACK)

    def start_grab_knee_attack(self, owner):
        if not owner.grab_controller.grabbed_enemy:
            return
        if self.is_attacking:
            return

        move_data = owner.get_attack_data(owner.GRAB_KNEE)
        self.attack_manager.start(owner.GRAB_KNEE, move_data)
        owner.grab_controller.grab_knee_remaining = owner.grab_controller.grab_knee_duration
        owner.state_machine.change_to(owner, owner.GRAB_KNEE)

    def start_clash_recovery(self, owner):
        self.cancel_attack()
        self._action_lock_remaining = self.clash_recovery_duration
        owner.state_machine.change_to(owner, owner.RECOIL)

    # enemy hits should fully cancel the player's combo.
    def cancel_attack(self):
        self.attack_manager.cancel()
        self._reset_combo()
        self._action_lock_remaining = 0

    def set_action_lock(self, frames):
        self._action_lock_remaining = frames

    # --- Private helpers ---

    def _tick_action_lock(self, owner):
        # action lock remaining means: the player cannot start a new action yet.
        if self._action_lock_remaining > 0:
            self._action_lock_remaining -= 1
            if owner.state == owner.RECOIL:
                if self._action_lock_remaining <= 0:
                    owner.state_machine.change_to(owner, owner.IDLE)
                # Why return?
                # During recoil, we do not want combo timers or attack ending logic to also manipulate state.
                # expected behavior:
                # Clash -> player enters RECOIL
                # Player stays RECOIL for clash recovery duration
                # Then returns to IDLE
                return True
        return False

    def _tick_combo_window(self):
        if self._combo_window_remaining > 0:
            self._combo_window_remaining -= 1
        else:
            self._combo_step = 0

    def _finish_attack_if_done(self, owner):
        if not self.is_attacking:
            return
        if not self.attack_manager.advance():
            return

        finished_attack_name, finished_move, attack_connected = self.attack_manager.finish()

        self._update_combo_after_attack(owner, finished_attack_name, finished_move, attack_connected)
        if finished_attack_name == owner.RUN_ATTACK:
            owner.movement.run_movement.start_run_attack_cooldown()

        self._return_to_ready_state(owner)

    def _update_combo_after_attack(self, owner, finished_attack_name, finished_move, attack_connected):
        # expected behavior:
        # Punch hits enemy -> combo can continue
        # Punch misses enemy -> combo resets
        # Player cannot build third hit by punching empty space
        attack_missed = (
            finished_attack_name in [owner.ATTACK, owner.ATTACK2, owner.ATTACK3]
            and not attack_connected
        )
        if attack_missed and not settings.ALLOW_COMBO_NOT_HIT:
            self._reset_combo()

        if finished_move and finished_move.cooldown > 0:
            self._action_lock_remaining = finished_move.cooldown
            if finished_attack_name not in [owner.ATTACK, owner.ATTACK2]:
                self._reset_combo()

    def _return_to_ready_state(self, owner):
        if owner.state == owner.DEAD:
            return
        owner.state_machine.change_to(owner, owner.IDLE)

    def _can_start_run_attack(self, owner):
        return (
            owner.movement.run_movement.can_start_run_attack()
            and not owner.input_state.run_attack_requires_attack_release
        )

    def _start_run_attack(self, owner):
        move_data = owner.get_attack_data(owner.RUN_ATTACK)
        self.attack_manager.start(owner.RUN_ATTACK, move_data)
        owner.movement.start_run_attack_momentum(owner)
        self._reset_combo()
        owner.input_state.run_attack_requires_attack_release = True
        owner.state_machine.change_to(owner, owner.RUN_ATTACK)

    def _start_combo_attack(self, owner):
        if self._combo_window_remaining > 0:
            self._combo_step += 1
        else:
            self._combo_step = 1

        self._combo_step = min(self._combo_step, 3)
        if self._combo_step == 1:
            attack_name = owner.ATTACK
        elif self._combo_step == 2:
            attack_name = owner.ATTACK2
        else:
            attack_name = owner.ATTACK3

        move_data = owner.get_attack_data(attack_name)
        if not move_data:
            raise ValueError(f"Missing player attack data: {attack_name}")

        owner.state_machine.change_to(owner, attack_name)
        if attack_name == owner.ATTACK3:
            owner.movement.attack_movement.start_combo_finisher_nudge(owner)

        self.attack_manager.start(attack_name, move_data)
        self._combo_window_remaining = move_data.combo_window

    def _reset_combo(self):
        self._combo_step = 0
        self._combo_window_remaining = 0
