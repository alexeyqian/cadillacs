class EnemyReactionState:
    def __init__(self):
        # Death countdown after dying — enemy lingers briefly before removal
        self._death_remaining = 30

        # Clash/recoil lock — prevents enemy instantly resuming pressure after a clash
        self._action_lock_remaining = 0

        # Hit stun — freezes enemy in HIT state for N frames
        self._hit_stun_remaining = 0
        # Knockback — slides the enemy away from the attacker each frame, decaying
        self._knockback_velocity = 0

        # Thrown — physics velocity applied while enemy is mid-throw arc
        self._thrown_velocity_x = 0
        self._thrown_remaining = 0
        self.throw_damage = 0          # read directly by combat_system for thrown-enemy collision damage
        self._thrown_hit_targets = set()

        # Knockdown / getup timers
        self._knockdown_remaining = 0
        self._getup_remaining = 0
