from game.entities.attack_controller import AttackController
from game.entities.attack_data import AttackPhaseData, EnemyAttackData


class EnemyCombatController:
    def start_attack(self, owner):
        owner.state = owner.ATTACK
        self.clear_hit_state(owner)
        self.reserve_attack_slot(owner, owner.uses_melee_attack_slot())
        self.reset_decision_timer(owner)
        self.start_attack_timing(owner)
        owner.animation_controller.play(owner.ATTACK)
        owner.animation_controller.reset_current_animation()

    def start_clash_recovery(self, owner):
        owner.state = owner.RECOIL
        owner.action_lock_remaining = owner.attack_clash_recovery_duration
        self.cancel_attack_timing(owner)
        self.reset_decision_timer(owner)
        self.clear_hit_state(owner)
        self.release_attack_slot(owner)
        self.set_cooldown(owner, max(
            self.get_cooldown(owner),
            owner.attack_clash_cooldown_duration
        ))

    # Enemy attack has explicit windup frames
    # Enemy attack only damages during active frames
    # Enemy attack has explicit recovery before it can act again
    def update_attack(self, owner, level, player):
        owner.face_player(player)
        attack_finished = self.advance_attack_timing(owner)

        attack_rect = owner.get_attack_rect()
        player_hurt_rect = player.get_hurt_rect()

        if (self.is_attack_active(owner)
            and attack_rect and player_hurt_rect 
            and not self.has_attack_hit(owner)):
            lane_distance = level.get_lane_distance(owner.y, player.y)
            if (lane_distance <= owner.attack_lane_reach 
                and  attack_rect.colliderect(player_hurt_rect)):
                player.take_damage(owner.attack_damage)
                self.mark_attack_hit(owner, player)

        if attack_finished:
            self.finish_attack(owner)

    def start_attack_timing(self, owner):
        controller = self.get_attack_controller(owner)
        controller.start(owner.ATTACK, self.get_attack_data(owner))
        self.set_attack_timer(owner, controller.attack_timer)

    def advance_attack_timing(self, owner):
        controller = self.get_attack_controller(owner)
        if not controller.is_attacking:
            controller.start(owner.ATTACK, self.get_attack_data(owner))
            controller.attack_timer = self.get_attack_timer(owner)

        attack_finished = controller.advance()
        self.set_attack_timer(owner, controller.attack_timer)
        return attack_finished

    def cancel_attack_timing(self, owner):
        controller = self.get_attack_controller(owner)
        controller.cancel()
        self.set_attack_timer(owner, 0)

    def finish_attack(self, owner):
        self.cancel_attack_timing(owner)
        owner.state = owner.PATROL
        self.clear_hit_state(owner)
        self.release_attack_slot(owner)
        self.set_cooldown(owner, owner.attack_cooldown_duration)

    def is_attack_active(self, owner):
        controller = self.get_attack_controller(owner)
        if not controller.is_attacking:
            attack_data = self.get_attack_data(owner)
            return (
                attack_data.windup
                <= self.get_attack_timer(owner)
                < attack_data.windup + attack_data.active
            )
        return controller.is_active()

    def get_active_hitbox_data(self, owner):
        if not self.is_attack_active(owner):
            return None

        attack_data = self.get_attack_data(owner)
        if not attack_data.hitboxes:
            return None

        return attack_data.hitboxes[0]

    def mark_attack_hit(self, owner, target):
        controller = self.get_attack_controller(owner)
        controller.mark_target_hit(target)
        self.mark_attack_already_hit(owner)

    def get_attack_controller(self, owner):
        if hasattr(owner, "attack_state"):
            return owner.attack_state.controller
        if not hasattr(owner, "attack_controller"):
            owner.attack_controller = AttackController()
        return owner.attack_controller

    def get_attack_timer(self, owner):
        if hasattr(owner, "attack_state"):
            return owner.attack_state.timer
        return getattr(owner, "attack_timer", 0)

    def set_attack_timer(self, owner, value):
        if hasattr(owner, "attack_state"):
            owner.attack_state.timer = value
        else:
            owner.attack_timer = value

    def reset_decision_timer(self, owner):
        if hasattr(owner, "attack_state"):
            owner.attack_state.reset_decision_timer()
        else:
            owner.attack_decision_timer = 0

    def has_attack_hit(self, owner):
        if hasattr(owner, "attack_state"):
            return owner.attack_state.already_hit
        return owner.attack_already_hit

    def mark_attack_already_hit(self, owner):
        if hasattr(owner, "attack_state"):
            owner.attack_state.already_hit = True
        else:
            owner.attack_already_hit = True

    def clear_hit_state(self, owner):
        if hasattr(owner, "attack_state"):
            owner.attack_state.clear_hit_state()
        else:
            owner.attack_already_hit = False

    def reserve_attack_slot(self, owner, uses_slot):
        if hasattr(owner, "attack_state"):
            owner.attack_state.reserve_slot(uses_slot)
        else:
            owner.has_attack_slot = uses_slot

    def release_attack_slot(self, owner):
        if hasattr(owner, "attack_state"):
            owner.attack_state.release_slot()
        else:
            owner.has_attack_slot = False

    def get_cooldown(self, owner):
        if hasattr(owner, "attack_state"):
            return owner.attack_state.cooldown
        return owner.attack_cooldown

    def set_cooldown(self, owner, value):
        if hasattr(owner, "attack_state"):
            owner.attack_state.cooldown = value
        else:
            owner.attack_cooldown = value

    def get_attack_data(self, owner):
        if hasattr(owner, "attack_state") and owner.attack_state.data:
            return owner.attack_state.data
        if hasattr(owner, "attack_data"):
            return owner.attack_data

        return EnemyAttackData(
            damage=owner.attack_damage,
            delay=owner.attack_delay,
            cooldown=owner.attack_cooldown_duration,
            phase=AttackPhaseData(
                windup=owner.attack_windup,
                active=owner.attack_active,
                recovery=owner.attack_recovery,
            ),
            clash_recovery_duration=owner.attack_clash_recovery_duration,
            clash_cooldown_duration=owner.attack_clash_cooldown_duration,
        )

    # Compatibility aliases for older call sites while migration continues.
    def start_attack_timer(self, owner):
        self.start_attack_timing(owner)

    def update_attack_timer(self, owner):
        return self.advance_attack_timing(owner)

    def cancel_attack_timer(self, owner):
        self.cancel_attack_timing(owner)
