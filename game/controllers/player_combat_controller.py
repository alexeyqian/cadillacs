import game.settings as settings

from game.combat.player_attack_result import PlayerAttackResult


# TODO: attack buffering, clash/parry, and attack configs
class PlayerCombatController:
    def __init__(self):
        self.attack_result = PlayerAttackResult()

    # --- State queries ---

    def get_active_hitbox_data(self, owner):
        cs = owner.combat_state
        if not cs.attack_manager.is_active():
            return None
        return cs.attack_manager.current_attack

    def get_attack_data(self, owner):
        cs = owner.combat_state
        if cs.attack_manager.current_attack:
            return cs.attack_manager.current_attack
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

    def can_hit_target(self, owner, target):
        return owner.combat_state.attack_manager.can_hit_target(target)

    def can_hit_more_targets(self, owner):
        return owner.combat_state.attack_manager.can_hit_more_targets()

    def mark_attack_hit(self, owner, target):
        owner.combat_state.attack_manager.mark_target_hit(target)

    # --- Per-frame updates ---

    def advance_timers(self, owner):
        if self._tick_action_lock(owner):
            return
        self._tick_combo_window(owner)

    def update_attack(self, owner):
        self._finish_attack_if_done(owner)

    # --- Attack starters ---

    def start_attack(self, owner):
        cs = owner.combat_state
        if cs.is_attacking:
            return
        if cs._action_lock_remaining > 0:
            return
        if self._can_start_run_attack(owner):
            self._start_run_attack(owner)
            return

        self._start_combo_attack(owner)

    def start_jump_attack(self, owner):
        cs = owner.combat_state
        if not owner.movement.is_jumping:
            return
        if owner.air and not owner.air.can_start_jump_attack():
            return
        if cs.is_attacking:
            return

        move_data = owner.get_attack_data(owner.JUMP_ATTACK)
        cs.attack_manager.start(owner.JUMP_ATTACK, move_data)
        if owner.air:
            owner.air.mark_jump_attack_used()
        owner.state_machine.change_to(owner, owner.JUMP_ATTACK)

    def start_grab_knee_attack(self, owner):
        cs = owner.combat_state
        gs = owner.grab_state
        if not gs.grabbed_enemy:
            return
        if cs.is_attacking:
            return

        move_data = owner.get_attack_data(owner.GRAB_KNEE)
        cs.attack_manager.start(owner.GRAB_KNEE, move_data)
        gs.grab_knee_remaining = gs.grab_knee_duration
        owner.state_machine.change_to(owner, owner.GRAB_KNEE)

    def start_clash_recovery(self, owner):
        cs = owner.combat_state
        self.cancel_attack(owner)
        cs._action_lock_remaining = cs.clash_recovery_duration
        owner.state_machine.change_to(owner, owner.RECOIL)

    # enemy hits should fully cancel the player's combo.
    def cancel_attack(self, owner):
        cs = owner.combat_state
        cs.attack_manager.cancel()
        self._reset_combo(owner)
        cs._action_lock_remaining = 0

    def set_action_lock(self, owner, frames):
        owner.combat_state._action_lock_remaining = frames

    # --- Private helpers ---

    def _tick_action_lock(self, owner):
        cs = owner.combat_state
        if cs._action_lock_remaining > 0:
            cs._action_lock_remaining -= 1
            if owner.state == owner.RECOIL:
                if cs._action_lock_remaining <= 0:
                    owner.state_machine.change_to(owner, owner.IDLE)
                return True
        return False

    def _tick_combo_window(self, owner):
        cs = owner.combat_state
        if cs._combo_window_remaining > 0:
            cs._combo_window_remaining -= 1
        else:
            cs._combo_step = 0

    def _finish_attack_if_done(self, owner):
        cs = owner.combat_state
        if not cs.is_attacking:
            return
        if not cs.attack_manager.advance():
            return

        finished_attack_name, finished_move, attack_connected = cs.attack_manager.finish()

        self._update_combo_after_attack(owner, finished_attack_name, finished_move, attack_connected)
        if finished_attack_name == owner.RUN_ATTACK:
            owner.movement.run_movement.start_run_attack_cooldown()

        self._return_to_ready_state(owner)

    def _update_combo_after_attack(self, owner, finished_attack_name, finished_move, attack_connected):
        cs = owner.combat_state
        attack_missed = (
            finished_attack_name in [owner.ATTACK, owner.ATTACK2, owner.ATTACK3]
            and not attack_connected
        )
        if attack_missed and not settings.ALLOW_COMBO_NOT_HIT:
            self._reset_combo(owner)

        if finished_move and finished_move.cooldown > 0:
            cs._action_lock_remaining = finished_move.cooldown
            if finished_attack_name not in [owner.ATTACK, owner.ATTACK2]:
                self._reset_combo(owner)

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
        cs = owner.combat_state
        move_data = owner.get_attack_data(owner.RUN_ATTACK)
        cs.attack_manager.start(owner.RUN_ATTACK, move_data)
        owner.movement.start_run_attack_momentum(owner)
        self._reset_combo(owner)
        owner.input_state.run_attack_requires_attack_release = True
        owner.state_machine.change_to(owner, owner.RUN_ATTACK)

    def _start_combo_attack(self, owner):
        cs = owner.combat_state
        if cs._combo_window_remaining > 0:
            cs._combo_step += 1
        else:
            cs._combo_step = 1

        cs._combo_step = min(cs._combo_step, 3)
        if cs._combo_step == 1:
            attack_name = owner.ATTACK
        elif cs._combo_step == 2:
            attack_name = owner.ATTACK2
        else:
            attack_name = owner.ATTACK3

        move_data = owner.get_attack_data(attack_name)
        if not move_data:
            raise ValueError(f"Missing player attack data: {attack_name}")

        owner.state_machine.change_to(owner, attack_name)
        if attack_name == owner.ATTACK3:
            owner.movement.attack_movement.start_combo_finisher_nudge(owner)

        cs.attack_manager.start(attack_name, move_data)
        cs._combo_window_remaining = move_data.combo_window

    def _reset_combo(self, owner):
        cs = owner.combat_state
        cs._combo_step = 0
        cs._combo_window_remaining = 0
