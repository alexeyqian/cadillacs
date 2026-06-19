from game.settings import ENEMY_FLANK_Y_TOLERANCE, MAX_MELEE_ATTACKERS

class EnemyStateController:
    def __init__(self):
        self.decision_timer = 0

    def reset_decision_timer(self):
        self.decision_timer = 0

    def choose_state(self, owner, level, player, distance_x, distance_y, enemies):
        if owner.state == owner.ATTACK:
            return

        if self.can_attack_player(owner, level, player, distance_x, distance_y, enemies):
            owner.flanking.clear_target()
            self.prepare_or_start_attack(owner, player)
        elif distance_x <= owner.movement.detect_range:
            self.enter_chase(owner, player, distance_x, distance_y, enemies)
        else:
            self.enter_patrol(owner)

    def enter_chase(self, owner, player, distance_x, distance_y, enemies):
        self.reset_attack_decision(owner)
        if self.should_flank(owner, player, distance_x, distance_y, enemies):
            owner.flanking.set_target(owner, player, enemies)
        else:
            owner.flanking.clear_target()
        owner.state = owner.CHASE

    def enter_patrol(self, owner):
        self.reset_attack_decision(owner)
        owner.flanking.clear_target()
        owner.state = owner.PATROL

    def execute_state(self, owner, level, player, enemies, dx, dy):
        if owner.state == owner.PATROL:
            owner.movement.update_patrol(owner)
        elif owner.state == owner.CHASE:
            owner.movement.update_chasing(owner, player, dx, dy)
            owner.movement.separate_from_other_enemies(owner, enemies)
        elif owner.state == owner.ATTACK:
            owner.update_attack(level, player)

    def prepare_or_start_attack(self, owner, player=None):
        self.increment_attack_decision(owner)

        if self.get_attack_decision(owner) >= self.get_required_attack_delay(owner, player):
            owner.start_attack()
            return

        # A short readable pause before windup makes attack commitment fairer.
        owner.state = owner.IDLE

    def can_attack_player(self, owner, level, player, distance_x, distance_y, enemies):
        if self.get_attack_cooldown(owner) > 0:
            return False
        if not self.is_in_attack_range(owner, level, player, distance_x):
            return False
        if not self.has_available_attack_slot(owner, player, enemies):
            return False

        return True

    def is_in_attack_range(self, owner, level, player, distance_x):
        if distance_x > owner.combat_controller.attack_range:
            return False
        lane_distance = level.get_lane_distance(owner.y, player.y)
        return lane_distance <= owner.combat_controller.get_attack_data(owner).lane_reach

    def has_available_attack_slot(self, owner, player, enemies):
        # only the closest eligible melee enemy should take the slot.
        # This makes group behavior feel more intentional.
        if self.count_active_melee_attackers(enemies) >= self.get_melee_attack_slot_limit(owner):
            return False
        if self.side_already_has_attacker(owner, player, enemies):
            return False
        return self.is_closest_melee_attacker_on_side(owner, player, enemies)
    
    def is_closest_melee_attacker_on_side(self, owner, player, enemies):
        closest_enemy = owner
        closest_distance = float("inf")

        for enemy in enemies:
            if not self.is_eligible_melee_attacker(enemy, player):
                continue
            if self.get_side_of_player(enemy, player) != self.get_side_of_player(owner, player):
                continue

            dx = abs(enemy.x - player.x)
            if dx < closest_distance:
                closest_distance = dx
                closest_enemy = enemy

        return closest_enemy is owner

    def is_eligible_melee_attacker(self, enemy, player):
        if self.get_attack_cooldown(enemy) > 0:
            return False
        # That means an enemy that already owns a slot remains counted as eligible 
        # for priority until it releases the slot. 
        # This makes the coordination stable during the attack.
        if self.has_attack_slot(enemy):
            return True
        if enemy.state in [enemy.DEAD, enemy.HIT, enemy.GRABBED, enemy.THROWN, enemy.KNOCKDOWN, enemy.GETUP]:
            return False

        dx = abs(enemy.x - player.x)
        dy = abs(enemy.y - player.y)

        return dx <= enemy.combat_controller.attack_range and dy <= enemy.combat_controller.attack_lane_range
    
    #  enemies prefer opposite sides
    # This prevents same-side dogpiles
    def side_already_has_attacker(self, owner, player, enemies):
        owner_side = self.get_side_of_player(owner, player)

        for enemy in enemies:
            if enemy is owner:
                continue
            if not self.has_attack_slot(enemy):
                continue
            if self.get_side_of_player(enemy, player) == owner_side:
                return True

        return False
    
    def get_melee_attack_slot_limit(self, owner):
        return owner.combat_controller.melee_attack_slot_limit or MAX_MELEE_ATTACKERS
    
    def count_active_melee_attackers(self, enemies):
        count = 0
        for enemy in enemies:
            if self.has_attack_slot(enemy):
                count += 1
        return count
    
    def should_flank(self, owner, player, distance_x, distance_y, enemies):
        if distance_x > owner.combat_controller.attack_range:
            return False
        # Why: enemies slightly above/below the attack lane should still
        # try to flank into position instead of giving up immediately.
        if distance_y > owner.combat_controller.attack_lane_range + ENEMY_FLANK_Y_TOLERANCE:
            return False
        if self.count_active_melee_attackers(enemies) < self.get_melee_attack_slot_limit(owner):
            return False

        return True

    def reset_attack_decision(self, owner):
        self.decision_timer = 0

    def increment_attack_decision(self, owner):
        self.decision_timer += 1

    def get_attack_decision(self, owner):
        return self.decision_timer

    def get_required_attack_delay(self, owner, player=None):
        return owner.combat_controller.get_attack_data(owner).delay

    def get_attack_cooldown(self, owner):
        return owner.combat_controller.cooldown_remaining

    def has_attack_slot(self, owner):
        return owner.combat_controller.has_attack_slot

    def get_side_of_player(self, owner, player):
        if owner.x < player.x:
            return "left"
        return "right"
