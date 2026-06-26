from game.combat.attack_data import DEFAULT_ENEMY_ATTACK_DATA
from game.combat.damage_request import DamageRequest


class EnemyCombatController:
    def __init__(self):
        pass

    # --- Public API ---

    def get_attack_data(self, owner):
        cs = owner.combat_state
        return cs._attack_data or DEFAULT_ENEMY_ATTACK_DATA

    def get_attack_timing_label(self, owner):
        if owner.state != owner.ATTACK:
            return ""
        return owner.combat_state.attack_manager.get_timing_label()

    def get_active_hitbox_data(self, owner):
        cs = owner.combat_state
        if not cs.attack_manager.is_active():
            return None
        return cs.attack_manager.current_attack

    def is_attack_active(self, owner):
        return owner.combat_state.attack_manager.is_active()

    def reserve_attack_slot(self, owner):
        owner.combat_state.owns_attack_slot = True

    def release_attack_slot(self, owner):
        owner.combat_state.owns_attack_slot = False

    def advance_timers(self, owner):
        cs = owner.combat_state
        if cs.cooldown_remaining > 0:
            cs.cooldown_remaining -= 1

    # --- Attack lifecycle (called from enemy.py) ---

    def start_attack(self, owner):
        owner.combat_state.owns_attack_slot = True
        owner._begin_attack(owner.ATTACK, owner.ATTACK, self.get_attack_data(owner))

    def update_attack(self, owner, level, player):
        cs = owner.combat_state
        owner.movement.face_player(owner, player)
        attack_finished = cs.attack_manager.advance()
        self._try_hit_player(owner, level, player, self.get_attack_data(owner))
        if attack_finished:
            self._finish_attack(owner)

    def start_run_attack(self, owner):
        owner._begin_attack(owner.RUN_ATTACK, owner.RUN_ATTACK, self._get_run_attack_data(owner))

    def update_run_attack(self, owner, level, player):
        cs = owner.combat_state
        attack_finished = cs.attack_manager.advance()
        self._try_hit_player(owner, level, player, self._get_run_attack_data(owner))
        if attack_finished:
            self._finish_run_attack(owner)

    def start_jump_attack(self, owner):
        owner._begin_attack(owner.JUMP_ATTACK, owner.JUMP_ATTACK, self._get_jump_attack_data(owner))

    def update_jump_attack(self, owner, level, player):
        cs = owner.combat_state
        attack_finished = cs.attack_manager.advance()
        self._try_hit_player(owner, level, player, self._get_jump_attack_data(owner))
        if attack_finished:
            self._finish_jump_attack(owner)

    def cancel_attack(self, owner):
        owner.combat_state.attack_manager.cancel()

    def start_clash_recovery(self, owner):
        attack_data = self.get_attack_data(owner)
        owner.state = owner.RECOIL
        owner.reaction_controller.set_action_lock(owner, attack_data.cooldown)
        owner._clear_combat_commitment()
        cs = owner.combat_state
        cs.cooldown_remaining = max(cs.cooldown_remaining, attack_data.cooldown)

    # --- Private helpers ---

    def _get_run_attack_data(self, owner):
        cs = owner.combat_state
        return cs._run_attack_data or self.get_attack_data(owner)

    def _get_jump_attack_data(self, owner):
        cs = owner.combat_state
        return cs._jump_attack_data or self.get_attack_data(owner)

    def _try_hit_player(self, owner, level, player, attack_data):
        cs = owner.combat_state
        if not cs.attack_manager.is_active():
            return
        if cs.attack_manager.has_connected:
            return
        attack_rect = owner.get_attack_rect()
        player_hurt_rect = player.get_hurt_rect()
        if not attack_rect or not player_hurt_rect:
            return
        lane_distance = level.get_lane_distance(owner.y, player.y)
        if lane_distance <= attack_data.lane_reach and attack_rect.colliderect(player_hurt_rect):
            player.take_damage(DamageRequest.from_attack_data(attack_data))
            cs.attack_manager.mark_target_hit(player)

    def _finish_attack(self, owner):
        cs = owner.combat_state
        cs.attack_manager.cancel()
        owner.state = owner.PATROL
        cs.owns_attack_slot = False
        cs.cooldown_remaining = self.get_attack_data(owner).cooldown

    def _finish_run_attack(self, owner):
        cs = owner.combat_state
        cs.attack_manager.cancel()
        owner.state = owner.PATROL
        cs.cooldown_remaining = self._get_run_attack_data(owner).cooldown

    def _finish_jump_attack(self, owner):
        cs = owner.combat_state
        cs.attack_manager.cancel()
        owner.state = owner.JUMP if owner.movement.is_jumping else owner.IDLE
        cs.cooldown_remaining = self._get_jump_attack_data(owner).cooldown
