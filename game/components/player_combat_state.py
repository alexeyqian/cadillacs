import game.settings as settings

from game.combat.attack_manager import AttackManager


class PlayerCombatState:
    def __init__(self):
        self.attack_manager = AttackManager()
        self.attacks = {}
        self.weapon_attacks = {}

        self._combo_step = 0
        self._combo_window_remaining = 0
        self._action_lock_remaining = 0

        self.clash_recovery_duration = settings.PLAYER_CLASH_RECOVERY
        self.grab_knee_recovery_duration = 6

    @property
    def is_attacking(self):
        return self.attack_manager.is_attacking

    @property
    def current_attack_name(self):
        return self.attack_manager.current_attack_name
