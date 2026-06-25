from dataclasses import dataclass
from typing import Optional
from game.settings import ENEMY_ATTACK_LANE_RANGE, ENEMY_ATTACK_RANGE, ENEMY_FLANK_Y_TOLERANCE, ENEMY_RUN_CHASE_THRESHOLD, MAX_MELEE_ATTACKERS

# Frames the enemy pauses before turning when the player crosses to the other side.
DIRECTION_CHANGE_DELAY = 60


# pure read-only data 
@dataclass(frozen=True)
class EnemyAIConfig:
    attack_range: int = ENEMY_ATTACK_RANGE
    attack_lane_range: int = ENEMY_ATTACK_LANE_RANGE
    melee_attack_slot_limit: Optional[int] = None


class EnemyAIController:
    def __init__(self):
        self._decision_timer = 0
        self._direction_change_timer = 0
        self.config = EnemyAIConfig()

    def reset_decision_timer(self):
        self._decision_timer = 0
        self._direction_change_timer = 0

    def update(self, owner, context):
        owner.intent.clear()

        if owner.state in (owner.ATTACK, owner.RUN_ATTACK):
            return

        # While running, check for run attack opportunity before any other decision.
        if owner.state == owner.RUN:
            self._try_run_attack(owner, context)
            if owner.intent.wants_run_attack():
                return

        # While airborne, only allow jump attack — no other decisions.
        if owner.movement.is_jumping:
            if owner.state not in (owner.JUMP_ATTACK,):
                self._try_jump_attack(owner, context)
            return

        dx, dy, distance_x, distance_y = owner.movement.get_player_distance(
            owner,
            context.player,
        )

        # Detect player crossing to the other side while enemy is chasing.
        if distance_x <= owner.movement.detect_range:
            player_is_right = context.player.x > owner.x
            if player_is_right != owner.facing_right:
                self._direction_change_timer = DIRECTION_CHANGE_DELAY

        # While the hesitation timer is active: stay idle, don't turn yet.
        if self._direction_change_timer > 0:
            self._direction_change_timer -= 1
            owner.state = owner.IDLE
            return

        if distance_x <= owner.movement.detect_range:
            owner.movement.face_player(owner, context.player)

        if self._can_attack_player(owner, context, distance_x):
            self._prepare_attack_intent(owner, context.player)
        elif distance_x <= owner.movement.detect_range:
            if self._should_jump(owner, distance_x):
                self._request_jump_intent(owner)
            else:
                self._request_chase_intent(owner, context, distance_x, distance_y)
        else:
            self._request_patrol_intent(owner)

    def _prepare_attack_intent(self, owner, player):
        owner.flanking.clear_target()
        self._decision_timer += 1

        if self._decision_timer < owner.combat_controller.get_attack_data(owner).delay:
            owner.state = owner.IDLE
            return

        owner.intent.attack_player()
        owner.combat_controller.reserve_attack_slot(owner)
        self.reset_decision_timer()

    def _try_run_attack(self, owner, context):
        if not owner.movement.can_run_attack:
            return
        if owner.combat_controller.cooldown_remaining > 0:
            return
        dx, dy, distance_x, distance_y = owner.movement.get_player_distance(owner, context.player)
        if distance_x <= self.config.attack_range * 1.5:
            owner.intent.run_attack()
            owner.combat_controller.reserve_attack_slot(owner)

    def _try_jump_attack(self, owner, context):
        if not owner.movement.can_jump_attack:
            return
        if owner.combat_controller.cooldown_remaining > 0:
            return
        dx, dy, distance_x, distance_y = owner.movement.get_player_distance(owner, context.player)
        if distance_x <= self.config.attack_range * 2:
            owner.intent.jump_attack()

    def _should_jump(self, owner, distance_x):
        if not owner.movement.can_jump:
            return False
        if not owner.movement.air_state.can_jump_now:
            return False
        # Jump only when close enough to matter but not already in attack range.
        return distance_x <= self.config.attack_range * 3

    def _request_jump_intent(self, owner):
        owner.movement.air_state.on_jump_requested()
        owner.intent.jump()
        owner.state = owner.JUMP

    def _request_chase_intent(self, owner, context, distance_x, distance_y):
        self.reset_decision_timer()

        if self._should_flank(owner, distance_x, distance_y, context.enemies):
            owner.flanking.set_target(owner, context.player, context.enemies)
            owner.intent.flank_to(owner.flanking.get_target_position(context.player))
            owner.state = owner.CHASE
        elif owner.movement.can_run and distance_x > ENEMY_RUN_CHASE_THRESHOLD:
            owner.flanking.clear_target()
            owner.intent.run_toward_player()
            owner.state = owner.RUN
        else:
            owner.flanking.clear_target()
            owner.intent.move_toward_player()
            owner.state = owner.CHASE

    def _request_patrol_intent(self, owner):
        self.reset_decision_timer()
        owner.flanking.clear_target()
        owner.intent.patrol()
        owner.state = owner.PATROL

    def _can_attack_player(self, owner, context, distance_x):
        if owner.combat_controller.cooldown_remaining > 0:
            return False
        if not self._is_in_attack_range(owner, context, distance_x):
            return False
        if not self._has_available_attack_slot(owner, context.player, context.enemies):
            return False

        return True

    def _is_in_attack_range(self, owner, context, distance_x):
        if distance_x > self.config.attack_range:
            return False

        lane_distance = context.level.get_lane_distance(owner.y, context.player.y)
        return lane_distance <= owner.combat_controller.get_attack_data(owner).lane_reach

    def _has_available_attack_slot(self, owner, player, enemies):
        # only the closest eligible melee enemy should take the slot.
        # This makes group behavior feel more intentional.
        if self._count_active_melee_attackers(enemies) >= self._get_melee_attack_slot_limit(owner):
            return False
        if self._side_already_has_attacker(owner, player, enemies):
            return False
        return self._is_closest_melee_attacker_on_side(owner, player, enemies)

    def _is_closest_melee_attacker_on_side(self, owner, player, enemies):
        closest_enemy = owner
        closest_distance = float("inf")

        for enemy in enemies:
            if not self._is_eligible_melee_attacker(enemy, player):
                continue
            if self._get_side_of_player(enemy, player) != self._get_side_of_player(owner, player):
                continue

            dx = abs(enemy.x - player.x)
            if dx < closest_distance:
                closest_distance = dx
                closest_enemy = enemy

        return closest_enemy is owner

    def _is_eligible_melee_attacker(self, enemy, player):
        if self._get_attack_cooldown(enemy) > 0:
            return False
        # That means an enemy that already owns a slot remains counted as eligible
        # for priority until it releases the slot.
        # This makes the coordination stable during the attack.
        if enemy.combat_controller.owns_attack_slot:
            return True
        if enemy.state in [enemy.DEAD, enemy.HIT, enemy.GRABBED, enemy.THROWN, enemy.KNOCKDOWN, enemy.GETUP]:
            return False

        dx = abs(enemy.x - player.x)
        dy = abs(enemy.y - player.y)

        return dx <= enemy.ai_controller.config.attack_range and dy <= enemy.ai_controller.config.attack_lane_range

    # enemies prefer opposite sides
    # This prevents same-side dogpiles
    def _side_already_has_attacker(self, owner, player, enemies):
        owner_side = self._get_side_of_player(owner, player)

        for enemy in enemies:
            if enemy is owner:
                continue
            if not enemy.combat_controller.owns_attack_slot:
                continue
            if self._get_side_of_player(enemy, player) == owner_side:
                return True

        return False

    def _get_melee_attack_slot_limit(self, owner):
        return self.config.melee_attack_slot_limit or MAX_MELEE_ATTACKERS

    def _count_active_melee_attackers(self, enemies):
        count = 0
        for enemy in enemies:
            if enemy.combat_controller.owns_attack_slot:
                count += 1
        return count

    def _should_flank(self, owner, distance_x, distance_y, enemies):
        if distance_x > self.config.attack_range:
            return False
        # Why: enemies slightly above/below the attack lane should still
        # try to flank into position instead of giving up immediately.
        if distance_y > self.config.attack_lane_range + ENEMY_FLANK_Y_TOLERANCE:
            return False
        if self._count_active_melee_attackers(enemies) < self._get_melee_attack_slot_limit(owner):
            return False

        return True

    def _get_side_of_player(self, owner, player):
        if owner.x < player.x:
            return "left"
        return "right"
