from game.entities.attack_controller import AttackController

#EnemyAttackData = what the attack is
#EnemyAttackState = what is happening right now
#AttackController = generic timing/hit-target engine used inside state
#EnemyCombatController = enemy-specific combat orchestration
class EnemyAttackState:
    def __init__(self, attack_data=None):
        self.data = attack_data

        # new design
        # give every enemy attack a clean timer 
        # so the next chunk can use windup / active / recovery 
        # instead of relying only on animation frame position.
        self.controller = AttackController()
        self.decision_timer = 0
        self.already_hit = False
        self.cooldown = 0

        # todo: add enemy coordination layer in future
        # attack slot reservation system
        # expected behavior:
        # Enemy reserves a melee attack slot when attack starts
        # Enemy releases slot when attack ends, flinches, dies, or clashes
        # Attack limit becomes more reliable and easier to reason about
        self.has_slot = False

    @property
    def timer(self):
        return self.controller.attack_timer

    @timer.setter
    def timer(self, value):
        self.controller.attack_timer = value

    def reset_decision_timer(self):
        self.decision_timer = 0

    def reserve_slot(self, uses_slot):
        self.has_slot = uses_slot

    def release_slot(self):
        self.has_slot = False

    def clear_hit_state(self):
        self.already_hit = False

    def update_timers(self):
        if self.cooldown > 0:
            self.cooldown -= 1
