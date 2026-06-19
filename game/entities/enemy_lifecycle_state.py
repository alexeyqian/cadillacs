class EnemyLifecycleState:
    def __init__(self):
        # Lifecycle
        self.death_remaining = 30
        self.death_countdown_started = False
        # This keeps the clash fair on both sides: the player cannot instantly re-punch,
        # and the enemy cannot instantly resume pressure either.
        self.action_lock_remaining = 0

        # Reactions
        # hit reaction # enemy gets briefly white when hit by player
        self.knockback_velocity = 0
        self.hit_stun_remaining = 0
        # grab/throw
        self.thrown_velocity_x = 0
        self.thrown_remaining = 0
        self.throw_damage = 0
        self.thrown_hit_targets = set()

        #knockdown/getup
        self.knockdown_remaining = 0
        self.getup_remaining = 0
