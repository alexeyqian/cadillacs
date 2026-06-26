from game.combat.hit_reaction import HitReaction


class EnemyReactionController:
    def __init__(self):
        # minimum damage in a single hit to trigger a flinch (HIT state + hit stun)
        self.flinch_damage_threshold = 0
        # minimum damage in a single hit to knock the enemy down instead of just flinching
        self.knockdown_damage_threshold = 40

    # --- Public API: reactions ---

    def is_reaction_blocked(self, owner):
        """Pure read — returns True if the enemy is currently locked in a reaction."""
        return owner.reaction_state._hit_stun_remaining > 0

    def update_reactions(self, owner):
        self._tick_hit_stun(owner)
        self._apply_knockback(owner)
        rs = owner.reaction_state
        owner.state = owner.HIT if rs._hit_stun_remaining > 0 else owner.IDLE

    def take_damage(self, owner, damage, attacker_x, reaction=None):
        if owner.state == owner.DEAD:
            return
        if reaction is None:
            reaction = HitReaction()

        owner.health.take_damage(damage)

        if owner.health.hp > 0 and damage >= self.knockdown_damage_threshold:
            self._knockdown(owner)
            return

        if owner.health.is_dead():
            self._die(owner)
            return

        if damage >= self.flinch_damage_threshold:
            self._apply_flinch(owner, attacker_x, reaction)

    def grabbed_by_player(self, owner):
        if owner.state == owner.DEAD:
            return
        self._clear_combat_commitment(owner)
        owner.state = owner.GRABBED
        owner.reaction_state._knockback_velocity = 0
        owner.reaction_state._hit_stun_remaining = 0

    def thrown_by_player(self, owner, direction, damage):
        if owner.state == owner.DEAD:
            return
        self._clear_combat_commitment(owner)
        owner.state = owner.THROWN
        owner.facing_right = direction > 0
        self.start_thrown(owner, direction, damage)
        owner.health.take_damage(damage)
        if owner.health.is_dead():
            self._die(owner)

    def take_grab_knee_damage(self, owner, damage):
        if owner.state == owner.DEAD:
            return
        self._clear_combat_commitment(owner)
        owner.health.take_damage(damage)
        if owner.health.is_dead():
            self._die(owner)
            return
        owner.state = owner.GRABBED

    # --- Public API: state timer operations (called by EnemyStateController / EnemyCombatController) ---

    def has_action_lock(self, owner):
        return owner.reaction_state._action_lock_remaining > 0

    def set_action_lock(self, owner, frames):
        owner.reaction_state._action_lock_remaining = frames

    def tick_action_lock(self, owner):
        rs = owner.reaction_state
        if rs._action_lock_remaining > 0:
            rs._action_lock_remaining -= 1

    def start_knockdown(self, owner, duration=60):
        owner.reaction_state._knockdown_remaining = duration

    def tick_knockdown(self, owner):
        rs = owner.reaction_state
        if rs._knockdown_remaining > 0:
            rs._knockdown_remaining -= 1
        return rs._knockdown_remaining <= 0

    def start_getup(self, owner, duration=20):
        owner.reaction_state._getup_remaining = duration

    def tick_getup(self, owner):
        rs = owner.reaction_state
        if rs._getup_remaining > 0:
            rs._getup_remaining -= 1
        return rs._getup_remaining <= 0

    def tick_death(self, owner):
        rs = owner.reaction_state
        if rs._death_remaining > 0:
            rs._death_remaining -= 1

    def is_death_finished(self, owner):
        return owner.reaction_state._death_remaining <= 0

    def start_thrown(self, owner, direction, damage, velocity=14, duration=30):
        rs = owner.reaction_state
        rs._thrown_velocity_x = velocity * direction
        rs._thrown_remaining = duration
        rs.throw_damage = damage
        rs._thrown_hit_targets.clear()

    def has_thrown_hit(self, owner, target):
        return id(target) in owner.reaction_state._thrown_hit_targets

    def mark_thrown_hit(self, owner, target):
        owner.reaction_state._thrown_hit_targets.add(id(target))

    # --- Private helpers ---

    def _die(self, owner):
        self._clear_combat_commitment(owner)
        owner.health.hp = 0
        owner.state = owner.DEAD
        owner.reaction_state._death_remaining = 30

    def _knockdown(self, owner):
        self._clear_combat_commitment(owner)
        owner.state = owner.KNOCKDOWN
        owner.reaction_state._knockdown_remaining = 60
        owner.reaction_state._knockback_velocity = 0

    def _apply_flinch(self, owner, attacker_x, reaction):
        stun_frames = reaction.stun_frames
        if stun_frames is None:
            stun_frames = owner.combat_controller.get_attack_data().hit_stun_duration
        owner.reaction_state._hit_stun_remaining = stun_frames
        owner.state = owner.HIT
        self._clear_combat_commitment(owner)

        knockback = reaction.knockback_velocity
        owner.reaction_state._knockback_velocity = knockback if attacker_x < owner.x else -knockback

    def _tick_hit_stun(self, owner):
        rs = owner.reaction_state
        if rs._hit_stun_remaining > 0:
            rs._hit_stun_remaining -= 1

    def _apply_knockback(self, owner):
        rs = owner.reaction_state
        v = rs._knockback_velocity
        if v == 0:
            return
        owner.x += v
        v *= 0.8
        rs._knockback_velocity = v if abs(v) >= 0.5 else 0

    def _clear_combat_commitment(self, owner):
        owner._clear_combat_commitment()
