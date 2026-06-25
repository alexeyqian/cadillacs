from game.combat.attack_manager import AttackManager

from game.combat.attack_data import DEFAULT_ENEMY_ATTACK_DATA
from game.combat.damage_request import DamageRequest
class EnemyCombatController:
    def __init__(self, attack_data=None):
        self.attack_manager = AttackManager()
        self.attack_data = attack_data
        self.run_attack_data = None
        self.jump_attack_data = None
        self.cooldown_remaining = 0
        self.owns_attack_slot = False

    @property
    def has_attack_slot(self):
        return self.owns_attack_slot

    def start_attack(self, owner):
        owner.state = owner.ATTACK
        self.owns_attack_slot = True
        owner.ai_controller.reset_decision_timer()
        self.attack_manager.start(owner.ATTACK, self.get_attack_data(owner))
        owner.animation_controller.play(owner.ATTACK)
        owner.animation_controller.reset_current_animation()

    def start_run_attack(self, owner):
        owner.state = owner.RUN_ATTACK
        owner.ai_controller.reset_decision_timer()
        self.attack_manager.start(owner.RUN_ATTACK, self.get_run_attack_data(owner))
        owner.animation_controller.play(owner.RUN_ATTACK)
        owner.animation_controller.reset_current_animation()

    def update_run_attack(self, owner, level, player):
        attack_finished = self.attack_manager.advance()

        attack_rect = owner.get_attack_rect()
        player_hurt_rect = player.get_hurt_rect()

        if (self.attack_manager.is_active()
            and attack_rect and player_hurt_rect
            and not self.attack_manager.has_connected):
            lane_distance = level.get_lane_distance(owner.y, player.y)
            attack_data = self.get_run_attack_data(owner)
            if (lane_distance <= attack_data.lane_reach
                and attack_rect.colliderect(player_hurt_rect)):
                player.take_damage(DamageRequest.from_attack_data(attack_data))
                self.attack_manager.mark_target_hit(player)

        if attack_finished:
            self.finish_run_attack(owner)

    def finish_run_attack(self, owner):
        self.attack_manager.cancel()
        owner.state = owner.PATROL
        self.cooldown_remaining = self.get_run_attack_data(owner).cooldown

    def start_jump_attack(self, owner):
        owner.state = owner.JUMP_ATTACK
        owner.ai_controller.reset_decision_timer()
        self.attack_manager.start(owner.JUMP_ATTACK, self.get_jump_attack_data(owner))
        owner.animation_controller.play(owner.JUMP_ATTACK)
        owner.animation_controller.reset_current_animation()

    def start_clash_recovery(self, owner):
        attack_data = self.get_attack_data(owner)
        owner.state = owner.RECOIL
        owner.condition.set_action_lock(attack_data.cooldown)
        self.attack_manager.cancel()
        owner.ai_controller.reset_decision_timer()
        self.owns_attack_slot = False
        self.cooldown_remaining = max(self.cooldown_remaining, attack_data.cooldown)

    # Enemy attack has explicit windup frames
    # Enemy attack only damages during active frames
    # Enemy attack has explicit recovery before it can act again
    def update_jump_attack(self, owner, level, player):
        attack_finished = self.attack_manager.advance()

        attack_rect = owner.get_attack_rect()
        player_hurt_rect = player.get_hurt_rect()

        if (self.attack_manager.is_active()
            and attack_rect and player_hurt_rect
            and not self.attack_manager.has_connected):
            lane_distance = level.get_lane_distance(owner.y, player.y)
            attack_data = self.get_jump_attack_data(owner)
            if (lane_distance <= attack_data.lane_reach
                and attack_rect.colliderect(player_hurt_rect)):
                player.take_damage(DamageRequest.from_attack_data(attack_data))
                self.attack_manager.mark_target_hit(player)

        if attack_finished:
            self.finish_jump_attack(owner)

    def finish_jump_attack(self, owner):
        self.attack_manager.cancel()
        owner.state = owner.JUMP if owner.movement.is_jumping else owner.IDLE
        self.cooldown_remaining = self.get_jump_attack_data(owner).cooldown

    def update_attack(self, owner, level, player):
        owner.movement.face_player(owner, player)
        attack_finished = self.attack_manager.advance()

        attack_rect = owner.get_attack_rect()
        player_hurt_rect = player.get_hurt_rect()

        if (self.attack_manager.is_active()
            and attack_rect and player_hurt_rect
            and not self.attack_manager.has_connected):
            lane_distance = level.get_lane_distance(owner.y, player.y)
            attack_data = self.get_attack_data(owner)
            if (lane_distance <= attack_data.lane_reach
                and attack_rect.colliderect(player_hurt_rect)):
                player.take_damage(DamageRequest.from_attack_data(attack_data))
                self.attack_manager.mark_target_hit(player)

        if attack_finished:
            self.finish_attack(owner)

    def cancel_attack_timing(self, owner):
        self.attack_manager.cancel()

    def finish_attack(self, owner):
        self.attack_manager.cancel()
        owner.state = owner.PATROL
        self.owns_attack_slot = False
        self.cooldown_remaining = self.get_attack_data(owner).cooldown

    def is_attack_active(self, owner):
        return self.attack_manager.is_active()

    def get_active_hitbox_data(self):
        if not self.attack_manager.is_active():
            return None
        return self.attack_manager.current_attack

    def get_attack_timer(self, owner):
        return self.attack_manager.elapsed_frames

    def release_attack_slot(self, owner):
        self.owns_attack_slot = False

    def reserve_attack_slot(self, owner):
        self.owns_attack_slot = True

    @property
    def current_attack_name(self):
        return self.attack_manager.current_attack_name

    def get_attack_data(self, owner):
        if self.attack_data:
            return self.attack_data
        return DEFAULT_ENEMY_ATTACK_DATA

    def get_run_attack_data(self, owner):
        if self.run_attack_data:
            return self.run_attack_data
        return self.get_attack_data(owner)

    def get_jump_attack_data(self, owner):
        if self.jump_attack_data:
            return self.jump_attack_data
        return self.get_attack_data(owner)

    def get_attack_timing_label(self, owner):
        if owner.state != owner.ATTACK:
            return ""
        return self.attack_manager.get_timing_label()

    def advance_timers(self):
        if self.cooldown_remaining > 0:
            self.cooldown_remaining -= 1
