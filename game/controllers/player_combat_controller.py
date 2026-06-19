from game.settings import *

from game.combat.attack_manager import AttackManager
from game.combat.hit_reaction import HitReaction

# TODO: attack buffering, counter-hit, clash/parry, and attack configs 
class PlayerCombatController:
    def __init__(self):
        self.attack_manager = AttackManager()
        self.attacks = {}
        self.weapon_attacks = {}

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
        return self.attack_manager.is_attacking

    @is_attacking.setter
    def is_attacking(self, value):
        if not value:
            self.attack_manager.cancel()

    @property
    def current_attack_name(self):
        return self.attack_manager.current_attack_name

    def mark_attack_hit(self, target):
        self.attack_manager.mark_target_hit(target)

    def can_hit_target(self, target):
        return self.attack_manager.can_hit_target(target)

    def can_hit_more_targets(self):
        return self.attack_manager.can_hit_more_targets()

    def is_attack_active(self):
        return self.attack_manager.is_active()

    def get_attack_phase_name(self):
        return self.attack_manager.get_phase_name()

    def get_attack_timing_label(self):
        return self.attack_manager.get_timing_label()

    def get_active_hitbox_data(self):
        if not self.is_attack_active():
            return None
        attack = self.attack_manager.current_attack
        if not attack:
            return None
        return attack

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
            if self.attack_manager.advance():
                finished_attack_name, finished_move, attack_connected = (
                    self.attack_manager.finish()
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

                if finished_move and finished_move.cooldown > 0:
                    self.action_lock_remaining = finished_move.cooldown
                    if finished_attack_name not in [owner.ATTACK_1, owner.ATTACK_2]:
                        self.combo_window_remaining = 0
                        self.combo_step = 0

                air = getattr(owner, "air", None)
                if air and air.is_landing and owner.state != owner.DEAD:
                    owner.state_machine.change_to(owner, owner.LANDING)
                elif owner.state != owner.DEAD:
                    owner.state_machine.change_to(owner, owner.IDLE)

    def start_attack(self, owner):
        if self.is_attacking:
            return
        if self.action_lock_remaining > 0:
            return
        air = getattr(owner, "air", None)
        if air and air.is_landing:
            return

        if owner.movement.can_start_run_attack():
            move_data = self.get_attack_data(owner, owner.RUN_ATTACK)
            self.attack_manager.start(owner.RUN_ATTACK, move_data)
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
            owner.movement.start_attack_3_nudge(owner)

        move_data = self.get_attack_data(owner, owner.state)
        self.attack_manager.start(owner.state, move_data)
        self.combo_window_remaining = move_data.combo_window if move_data else PLAYER_COMBO_WINDOW

    def start_jump_attack(self, owner):
        if not owner.movement.is_jumping:
            return
        air = getattr(owner, "air", None)
        if air and not air.can_start_jump_attack():
            return
        if self.is_attacking:
            return

        move_data = self.get_attack_data(owner, owner.JUMP_ATTACK)
        self.attack_manager.start(owner.JUMP_ATTACK, move_data)
        if air:
            air.mark_jump_attack_used()
        owner.state_machine.change_to(owner, owner.JUMP_ATTACK)

    def start_grab_knee_attack(self, owner):
        if not owner.grab_controller.grabbed_enemy:
            return
        if self.is_attacking:
            return

        move_data = self.get_attack_data(owner, owner.GRAB_KNEE)
        self.attack_manager.start(owner.GRAB_KNEE, move_data)
        owner.grab_controller.grab_knee_remaining = owner.grab_controller.grab_knee_duration
        owner.state_machine.change_to(owner, owner.GRAB_KNEE)

    def start_clash_recovery(self, owner):
        self.cancel_attack()
        self.action_lock_remaining = self.clash_recovery_duration
        owner.state_machine.change_to(owner, owner.RECOIL)

    # enemy hits should fully cancel the player’s combo.
    def cancel_attack(self):
        self.attack_manager.cancel()
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
        if not attack_data:
            return 10
        return int(attack_data.knockback_velocity + self.get_run_attack_power_bonus(
            owner,
            RUN_ATTACK_FULL_POWER_KNOCKBACK_BONUS,
        ))

    def get_attack_enemy_hit_stun_duration(self, owner):
        attack_data = self.get_current_or_state_attack_data(owner)
        if not attack_data:
            return 15
        return int(attack_data.hit_stun_duration + self.get_run_attack_power_bonus(
            owner,
            RUN_ATTACK_FULL_POWER_ENEMY_HIT_STUN_BONUS,
        ))

    def get_attack_hit_reaction(self, owner):
        return HitReaction(
            stun_frames=self.get_attack_enemy_hit_stun_duration(owner),
            knockback_velocity=self.get_attack_knockback_velocity(owner),
        )

    def get_run_attack_power_bonus(self, owner, full_power_bonus):
        if self.current_attack_name != owner.RUN_ATTACK:
            return 0

        movement = getattr(owner, "movement", None)
        run_distance = getattr(movement, "last_run_attack_distance", 0)
        bonus_distance = max(1, RUN_ATTACK_FULL_POWER_DISTANCE - RUN_ATTACK_REQUIRED_DISTANCE)
        bonus_ratio = (run_distance - RUN_ATTACK_REQUIRED_DISTANCE) / bonus_distance
        bonus_ratio = max(0, min(1, bonus_ratio))
        return full_power_bonus * bonus_ratio

    def get_current_or_state_attack_data(self, owner):
        if self.attack_manager.current_attack:
            return self.attack_manager.current_attack
        return self.get_attack_data(owner, owner.state)

    def get_attack_data(self, owner, attack_name):
        return owner.get_attack_data(attack_name)
