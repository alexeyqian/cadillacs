from game.entities.attack_controller import AttackController
from game.entities.attack_data import AttackPhaseData, EnemyAttackData


class EnemyCombatController:
    def start_attack(self, owner):
        owner.state = owner.ATTACK
        owner.attack_already_hit = False
        owner.has_attack_slot = owner.uses_melee_attack_slot()
        owner.attack_decision_timer = 0
        self.start_attack_timer(owner)
        owner.animation_controller.play(owner.ATTACK)
        owner.animation_controller.reset_current_animation()

    def start_clash_recovery(self, owner):
        owner.state = owner.RECOIL
        owner.action_lock_remaining = owner.attack_clash_recovery_duration
        self.cancel_attack_timer(owner)
        owner.attack_decision_timer = 0
        owner.attack_already_hit = False
        owner.has_attack_slot = False
        owner.attack_cooldown = max(
            owner.attack_cooldown,
            owner.attack_clash_cooldown_duration
        )

    # Enemy attack has explicit windup frames
    # Enemy attack only damages during active frames
    # Enemy attack has explicit recovery before it can act again
    def update_attack(self, owner, level, player):
        owner.face_player(player)
        attack_finished = self.update_attack_timer(owner)

        attack_rect = owner.get_attack_rect()
        player_hurt_rect = player.get_hurt_rect()

        if (self.is_attack_active(owner)
            and attack_rect and player_hurt_rect 
            and not owner.attack_already_hit):
            lane_distance = level.get_lane_distance(owner.y, player.y)
            if (lane_distance <= owner.attack_lane_reach 
                and  attack_rect.colliderect(player_hurt_rect)):
                player.take_damage(owner.attack_damage)
                self.mark_attack_hit(owner, player)

        if attack_finished:
            self.finish_attack(owner)

    def start_attack_timer(self, owner):
        controller = self.get_attack_controller(owner)
        controller.start_attack(owner.ATTACK, self.get_attack_data(owner))
        owner.attack_timer = controller.attack_timer

    def update_attack_timer(self, owner):
        controller = self.get_attack_controller(owner)
        if not controller.is_attacking:
            controller.start_attack(owner.ATTACK, self.get_attack_data(owner))
            controller.attack_timer = getattr(owner, "attack_timer", 0)

        attack_finished = controller.update_attack_timer()
        owner.attack_timer = controller.attack_timer
        return attack_finished

    def cancel_attack_timer(self, owner):
        controller = self.get_attack_controller(owner)
        controller.cancel_attack()
        owner.attack_timer = 0

    def finish_attack(self, owner):
        self.cancel_attack_timer(owner)
        owner.state = owner.PATROL
        owner.attack_already_hit = False
        owner.has_attack_slot = False
        owner.attack_cooldown = owner.attack_cooldown_duration

    def is_attack_active(self, owner):
        controller = self.get_attack_controller(owner)
        if not controller.is_attacking:
            return owner.attack_windup <= owner.attack_timer < owner.attack_windup + owner.attack_active
        return controller.is_active()

    def mark_attack_hit(self, owner, target):
        controller = self.get_attack_controller(owner)
        controller.mark_target_hit(target)
        owner.attack_already_hit = True

    def get_attack_controller(self, owner):
        if not hasattr(owner, "attack_controller"):
            owner.attack_controller = AttackController()
        return owner.attack_controller

    def get_attack_data(self, owner):
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
