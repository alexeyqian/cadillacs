from game.settings import ENEMY_FLANK_Y_TOLERANCE, MAX_MELEE_ATTACKERS

class EnemyStateController:
    def __init__(self):
        self.decision_timer = 0

    def reset_decision_timer(self):
        self.decision_timer = 0

    def choose_state(self, owner, level, player, distance_x, distance_y, enemies):
        if owner.state == owner.ATTACK:
            return

        if self._can_attack_player(owner, level, player, distance_x, enemies):
            owner.flanking.clear_target()
            self._prepare_or_start_attack(owner, player)
        elif distance_x <= owner.movement.detect_range:
            self._enter_chase(owner, player, distance_x, distance_y, enemies)
        else:
            self._enter_patrol(owner)

    def _enter_chase(self, owner, player, distance_x, distance_y, enemies):
        self.reset_attack_decision()
        if self._should_flank(owner, distance_x, distance_y, enemies):
            owner.flanking.set_target(owner, player, enemies)
        else:
            owner.flanking.clear_target()
        owner.state = owner.CHASE

    def _enter_patrol(self, owner):
        self.reset_attack_decision()
        owner.flanking.clear_target()
        owner.state = owner.PATROL

    def execute_movement_state(self, owner, player, enemies, dx, dy):
        if owner.state == owner.PATROL:
            owner.movement.update_patrol(owner)
        elif owner.state == owner.CHASE:
            owner.movement.update_chasing(owner, player, dx, dy)
            owner.movement.separate_from_other_enemies(owner, enemies)

    def _prepare_or_start_attack(self, owner, player=None):
        self._increment_attack_decision()

        if self._get_attack_decision() >= self._get_required_attack_delay(owner, player):
            owner.start_attack()
            return

        # A short readable pause before windup makes attack commitment fairer.
        owner.state = owner.IDLE

    def _can_attack_player(self, owner, level, player, distance_x, enemies):
        if self._get_attack_cooldown(owner) > 0:
            return False
        if not self._is_in_attack_range(owner, level, player, distance_x):
            return False
        if not self._has_available_attack_slot(owner, player, enemies):
            return False

        return True

    def _is_in_attack_range(self, owner, level, player, distance_x):
        if distance_x > owner.combat_controller.attack_range:
            return False
        lane_distance = level.get_lane_distance(owner.y, player.y)
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

        return dx <= enemy.combat_controller.attack_range and dy <= enemy.combat_controller.attack_lane_range
    
    #  enemies prefer opposite sides
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
        return owner.combat_controller.melee_attack_slot_limit or MAX_MELEE_ATTACKERS
    
    def _count_active_melee_attackers(self, enemies):
        count = 0
        for enemy in enemies:
            if enemy.combat_controller.owns_attack_slot:
                count += 1
        return count
    
    def _should_flank(self, owner, distance_x, distance_y, enemies):
        if distance_x > owner.combat_controller.attack_range:
            return False
        # Why: enemies slightly above/below the attack lane should still
        # try to flank into position instead of giving up immediately.
        if distance_y > owner.combat_controller.attack_lane_range + ENEMY_FLANK_Y_TOLERANCE:
            return False
        if self._count_active_melee_attackers(enemies) < self._get_melee_attack_slot_limit(owner):
            return False

        return True

    def reset_attack_decision(self):
        self.decision_timer = 0

    def _increment_attack_decision(self):
        self.decision_timer += 1

    def _get_attack_decision(self):
        return self.decision_timer

    def _get_required_attack_delay(self, owner, player=None):
        return owner.combat_controller.get_attack_data(owner).delay

    def _get_attack_cooldown(self, owner):
        return owner.combat_controller.cooldown_remaining

    def _get_side_of_player(self, owner, player):
        if owner.x < player.x:
            return "left"
        return "right"
