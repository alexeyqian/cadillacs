from game.combat.attack_manager import AttackManager


class EnemyCombatState:
    def __init__(self, attack_data=None):
        self._attack_data = attack_data
        self._run_attack_data = None
        self._jump_attack_data = None

        self.attack_manager = AttackManager()
        self.cooldown_remaining = 0
        self.owns_attack_slot = False

    def configure(self, attack_data, run_attack_data, jump_attack_data):
        self._attack_data = attack_data
        self._run_attack_data = run_attack_data
        self._jump_attack_data = jump_attack_data

    @property
    def current_attack_name(self):
        return self.attack_manager.current_attack_name
