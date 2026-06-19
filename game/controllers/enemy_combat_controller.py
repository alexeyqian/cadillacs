from game.combat.attack_manager import AttackManager

from game.combat.attack_data import DEFAULT_ENEMY_ATTACK_DATA
from game.combat.damage_request import DamageRequest
from game.settings import ENEMY_ATTACK_LANE_RANGE, ENEMY_ATTACK_RANGE


class EnemyCombatController:
    def __init__(self, attack_data=None):
        self.attack_manager = AttackManager()
        self.attack_data = attack_data
        self.already_hit = False
        self.cooldown_remaining = 0
        self.has_attack_slot = False
        self.attack_range = ENEMY_ATTACK_RANGE
        self.attack_lane_range = ENEMY_ATTACK_LANE_RANGE
        self.melee_attack_slot_limit = None

    def start_attack(self, owner):
        owner.state = owner.ATTACK
        self.already_hit = False
        self.has_attack_slot = self.uses_melee_attack_slot(owner)
        owner.state_controller.reset_decision_timer()
        self.attack_manager.start(owner.ATTACK, self.get_attack_data(owner))
        owner.animation_controller.play(owner.ATTACK)
        owner.animation_controller.reset_current_animation()

    def start_clash_recovery(self, owner):
        attack_data = self.get_attack_data(owner)
        owner.state = owner.RECOIL
        owner.life_cycle.set_action_lock(attack_data.cooldown)
        self.attack_manager.cancel()
        owner.state_controller.reset_decision_timer()
        self.already_hit = False
        self.has_attack_slot = False
        self.cooldown_remaining = max(self.cooldown_remaining, attack_data.cooldown)

    # Enemy attack has explicit windup frames
    # Enemy attack only damages during active frames
    # Enemy attack has explicit recovery before it can act again
    def update_attack(self, owner, level, player):
        owner.movement.face_player(owner, player)
        attack_finished = self.attack_manager.advance()

        attack_rect = owner.get_attack_rect()
        player_hurt_rect = player.get_hurt_rect()

        if (self.attack_manager.is_active()
            and attack_rect and player_hurt_rect
            and not self.already_hit):
            lane_distance = level.get_lane_distance(owner.y, player.y)
            attack_data = self.get_attack_data(owner)
            if (lane_distance <= attack_data.lane_reach
                and attack_rect.colliderect(player_hurt_rect)):
                self.damage_player(player, attack_data)
                self.attack_manager.mark_target_hit(player)
                self.already_hit = True

        if attack_finished:
            self.finish_attack(owner)

    def start_attack_timing(self, owner):
        self.attack_manager.start(owner.ATTACK, self.get_attack_data(owner))

    def advance_attack_timing(self, owner):
        return self.attack_manager.advance()

    def cancel_attack_timing(self, owner):
        self.attack_manager.cancel()

    def finish_attack(self, owner):
        self.attack_manager.cancel()
        owner.state = owner.PATROL
        self.already_hit = False
        self.has_attack_slot = False
        self.cooldown_remaining = self.get_attack_data(owner).cooldown

    def is_attack_active(self, owner):
        return self.attack_manager.is_active()

    def get_active_hitbox_data(self, owner):
        if not self.is_attack_active(owner):
            return None
        return self.get_attack_data(owner)

    def mark_attack_hit(self, owner, target):
        self.attack_manager.mark_target_hit(target)
        self.already_hit = True

    def get_attack_timer(self, owner):
        return self.attack_manager.elapsed_frames

    def set_attack_timer(self, owner, value):
        self.attack_manager.elapsed_frames = value

    def release_attack_slot(self, owner):
        self.has_attack_slot = False

    def get_attack_data(self, owner):
        if self.attack_data:
            return self.attack_data
        return DEFAULT_ENEMY_ATTACK_DATA

    def damage_player(self, player, attack_data):
        request = DamageRequest.from_attack_data(attack_data)

        try:
            player.take_damage(request)
        except TypeError:
            # Lightweight tests and older player-like objects may still expose
            # the damage-only API while production Player accepts HitReaction.
            try:
                player.take_damage(request.damage, reaction=request.reaction)
            except TypeError:
                player.take_damage(request.damage)

    def uses_melee_attack_slot(self, owner):
        return True

    def get_attack_phase_name(self, owner):
        if owner.state != owner.ATTACK:
            return ""
        return self.attack_manager.get_phase_name()

    def get_attack_timing_label(self, owner):
        if owner.state != owner.ATTACK:
            return ""
        return self.attack_manager.get_timing_label()

    def update_timers(self):
        if self.cooldown_remaining > 0:
            self.cooldown_remaining -= 1
