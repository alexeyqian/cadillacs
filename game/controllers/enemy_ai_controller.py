from dataclasses import dataclass
from typing import Optional
from game.settings import ENEMY_ATTACK_LANE_RANGE, ENEMY_ATTACK_RANGE, ENEMY_FLANK_Y_TOLERANCE, ENEMY_RUN_CHASE_THRESHOLD, MAX_MELEE_ATTACKERS

# Frames the enemy pauses before turning when the player crosses to the other side.
DIRECTION_CHANGE_DELAY = 60


@dataclass(frozen=True)
class EnemyAIConfig:
    attack_range: int = ENEMY_ATTACK_RANGE
    attack_lane_range: int = ENEMY_ATTACK_LANE_RANGE
    melee_attack_slot_limit: Optional[int] = None


class EnemyAIController:
    def __init__(self):
        self.config = EnemyAIConfig()

    def update(self, owner, context):
        owner.intent.clear()

        if owner.state in (owner.ATTACK, owner.RUN_ATTACK):
            return

        if owner.state == owner.RUN:
            self._try_run_attack(owner, context)
            if owner.intent.wants_run_attack():
                return

        if owner.movement.is_jumping:
            if owner.state not in (owner.JUMP_ATTACK,):
                self._try_jump_attack(owner, context)
            return

        _, _, dist_x, dist_y = owner.movement.get_player_distance(owner, context.player)
        in_detect_range = dist_x <= owner.movement.detect_range

        self._update_facing(owner, context.player, in_detect_range)

        if self._direction_change_pending(owner):
            return

        if in_detect_range:
            owner.movement.face_player(owner, context.player)

        if self._can_attack_player(owner, context, dist_x):
            self._attack_after_delay(owner, context.player)
        elif in_detect_range:
            if self._should_jump(owner, dist_x):
                self._jump(owner)
            else:
                self._chase(owner, context, dist_x, dist_y)
        else:
            self._patrol(owner)

    # --- Combat decisions ---

    def _try_run_attack(self, owner, context):
        if not owner.movement.can_run_attack:
            return
        if owner.combat_controller.is_on_cooldown(owner):
            return
        _, _, dist_x, _ = owner.movement.get_player_distance(owner, context.player)
        if dist_x <= self.config.attack_range * 1.5:
            owner.intent.run_attack()
            owner.combat_controller.reserve_attack_slot(owner)

    def _try_jump_attack(self, owner, context):
        if not owner.movement.can_jump_attack:
            return
        if owner.combat_controller.is_on_cooldown(owner):
            return
        _, _, dist_x, _ = owner.movement.get_player_distance(owner, context.player)
        if dist_x <= self.config.attack_range * 2:
            owner.intent.jump_attack()

    def _attack_after_delay(self, owner, player):
        """Increments a windup timer; fires attack intent once the delay elapses."""
        owner.movement.clear_flank_target()
        owner.ai_state._decision_timer += 1

        if owner.ai_state._decision_timer < self._get_attack_data(owner).delay:
            owner.state = owner.IDLE
            return

        owner.intent.attack_player()
        owner.combat_controller.reserve_attack_slot(owner)
        self._reset_timers(owner)

    # --- Movement decisions ---

    def _jump(self, owner):
        owner.movement.air_state.on_jump_requested()
        owner.intent.jump()
        owner.state = owner.JUMP

    def _chase(self, owner, context, dist_x, dist_y):
        self._reset_timers(owner)

        if self._should_flank(owner, dist_x, dist_y, context.enemies):
            owner.movement.update_flank_target(owner, context.player, context.enemies)
            owner.intent.flank_to(owner.movement.get_flank_position(context.player))
            owner.state = owner.CHASE
        elif owner.movement.can_run and dist_x > ENEMY_RUN_CHASE_THRESHOLD:
            owner.movement.clear_flank_target()
            owner.intent.run_toward_player()
            owner.state = owner.RUN
        else:
            owner.movement.clear_flank_target()
            owner.intent.move_toward_player()
            owner.state = owner.CHASE

    def _patrol(self, owner):
        self._reset_timers(owner)
        owner.movement.clear_flank_target()
        owner.intent.patrol()
        owner.state = owner.PATROL

    # --- Attack eligibility ---

    def _can_attack_player(self, owner, context, dist_x):
        if owner.combat_controller.is_on_cooldown(owner):
            return False
        if not self._in_attack_range(owner, context, dist_x):
            return False
        return self._can_claim_attack_slot(owner, context.player, context.enemies)

    def _in_attack_range(self, owner, context, dist_x):
        if dist_x > self.config.attack_range:
            return False
        lane_dist = context.level.get_lane_distance(owner.y, context.player.y)
        return lane_dist <= self._get_attack_data(owner).lane_reach

    def _can_claim_attack_slot(self, owner, player, enemies):
        slot_limit = self.config.melee_attack_slot_limit or MAX_MELEE_ATTACKERS
        active = sum(1 for e in enemies if e.combat_state.owns_attack_slot)
        if active >= slot_limit:
            return False
        if self._same_side_slot_taken(owner, player, enemies):
            return False
        return self._is_closest_on_same_side(owner, player, enemies)

    def _same_side_slot_taken(self, owner, player, enemies):
        """Returns True if another enemy already holds a slot on owner's side of the player."""
        owner_side = self._side_of_player(owner, player)
        return any(
            e is not owner
            and e.combat_state.owns_attack_slot
            and self._side_of_player(e, player) == owner_side
            for e in enemies
        )

    def _is_closest_on_same_side(self, owner, player, enemies):
        """Returns True if owner is the closest in-range enemy on its side of the player."""
        owner_side = self._side_of_player(owner, player)
        closest = min(
            (e for e in enemies
             if self._side_of_player(e, player) == owner_side
             and self._is_threatening_enemy(e, player)),
            key=lambda e: abs(e.x - player.x),
            default=None,
        )
        return closest is owner

    def _is_threatening_enemy(self, enemy, player):
        """Returns True if this enemy could realistically contest an attack slot."""
        if enemy.combat_controller.is_on_cooldown(enemy):
            return False
        if enemy.combat_state.owns_attack_slot:
            return True
        if enemy.state in (enemy.DEAD, enemy.HIT, enemy.GRABBED, enemy.THROWN,
                           enemy.KNOCKDOWN, enemy.GETUP):
            return False
        dist_x = abs(enemy.x - player.x)
        dist_y = abs(enemy.y - player.y)
        return (dist_x <= enemy.ai_controller.config.attack_range
                and dist_y <= enemy.ai_controller.config.attack_lane_range)

    def _should_flank(self, owner, dist_x, dist_y, enemies):
        if dist_x > self.config.attack_range:
            return False
        if dist_y > self.config.attack_lane_range + ENEMY_FLANK_Y_TOLERANCE:
            return False
        slot_limit = self.config.melee_attack_slot_limit or MAX_MELEE_ATTACKERS
        active = sum(1 for e in enemies if e.combat_state.owns_attack_slot)
        return active >= slot_limit

    def _should_jump(self, owner, dist_x):
        if not owner.movement.can_jump:
            return False
        if not owner.movement.air_state.can_jump_now:
            return False
        return dist_x <= self.config.attack_range * 3

    # --- Facing / direction ---

    def _update_facing(self, owner, player, in_detect_range):
        """Starts direction-change hesitation timer when the player crosses sides."""
        if not in_detect_range:
            return
        player_is_right = player.x > owner.x
        if player_is_right == owner.facing_right:
            return
        if owner.ai_state._direction_change_timer > 0:
            return
        owner.ai_state._direction_change_timer = DIRECTION_CHANGE_DELAY
        owner.facing_right = player_is_right  # commit now so this doesn't retrigger

    def _direction_change_pending(self, owner):
        if owner.ai_state._direction_change_timer <= 0:
            return False
        owner.ai_state._direction_change_timer -= 1
        owner.state = owner.IDLE
        return True

    # --- Helpers ---

    def _side_of_player(self, enemy, player):
        return "right" if enemy.x >= player.x else "left"

    def _get_attack_data(self, owner):
        return owner.combat_controller.get_attack_data(owner)

    def reset_decision_timer(self, owner):
        owner.ai_state._decision_timer = 0
        owner.ai_state._direction_change_timer = 0

    def _reset_timers(self, owner):
        self.reset_decision_timer(owner)
