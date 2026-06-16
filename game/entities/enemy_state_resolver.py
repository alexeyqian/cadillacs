from game.settings import *

class EnemyStateResolver:
    def choose_state(self, owner, level, player, distance_x, distance_y, enemies):
        if owner.state == owner.ATTACK:
            return

        if self.can_attack_player(owner, level, player, distance_x, distance_y, enemies):
            owner.flanking.clear_target()
            self.prepare_or_start_attack(owner)
        elif distance_x <= owner.detect_range:
            owner.attack_decision_timer = 0
            if self.should_flank(owner, player, distance_x, distance_y, enemies):
                owner.flanking.set_target(owner, player, enemies)
            else:
                owner.flanking.clear_target()
            # todo: replace with entry function like: start_chase()
            owner.state = owner.CHASE
        else:
            owner.attack_decision_timer = 0
            owner.flanking.clear_target()
            # todo: replace with: start_patrol()
            owner.state = owner.PATROL

    def prepare_or_start_attack(self, owner):
        owner.attack_decision_timer += 1

        if owner.attack_decision_timer >= owner.attack_delay:
            owner.start_attack()
            return

        # A short readable pause before windup makes attack commitment fairer.
        owner.state = owner.IDLE

    def can_attack_player(self, owner, level, player, distance_x, distance_y, enemies):
        if owner.attack_cooldown > 0:
            return False
        if distance_x > owner.attack_range:
            return False
        lane_distance = level.get_lane_distance(owner.y, player.y)
        if lane_distance > owner.attack_lane_reach:
            return False
        if owner.can_bypass_attack_slot_limit():
            return True
        # only the closest eligible melee enemy should take the slot. 
        # This makes group behavior feel more intentional.
        if self.count_active_melee_attackers(enemies) >= self.get_melee_attack_slot_limit(owner):
            return False
        if self.side_already_has_attacker(owner, player, enemies):
            return False
        if not self.is_closest_melee_attacker_on_side(owner, player, enemies):
            return False

        return True
    
    def is_closest_melee_attacker_on_side(self, owner, player, enemies):
        closest_enemy = owner
        closest_distance = float("inf")

        for enemy in enemies:
            if not self.is_eligible_melee_attacker(enemy, player):
                continue
            if enemy.get_side_of_player(player) != owner.get_side_of_player(player):
                continue

            dx = abs(enemy.x - player.x)
            if dx < closest_distance:
                closest_distance = dx
                closest_enemy = enemy

        return closest_enemy is owner

    def is_eligible_melee_attacker(self, enemy, player):
        if not enemy.uses_melee_attack_slot():
            return False
        if enemy.attack_cooldown > 0:
            return False
        # That means an enemy that already owns a slot remains counted as eligible 
        # for priority until it releases the slot. 
        # This makes the coordination stable during the attack.
        if enemy.has_attack_slot:
            return True
        if enemy.state in [enemy.DEAD, enemy.HIT, enemy.GRABBED, enemy.THROWN, enemy.KNOCKDOWN, enemy.GETUP]:
            return False

        dx = abs(enemy.x - player.x)
        dy = abs(enemy.y - player.y)

        return dx <= enemy.attack_range and dy <= enemy.attack_lane_range
    
    #  enemies prefer opposite sides
    # This prevents same-side dogpiles
    def side_already_has_attacker(self, owner, player, enemies):
        owner_side = owner.get_side_of_player(player)

        for enemy in enemies:
            if enemy is owner:
                continue
            if not enemy.has_attack_slot:
                continue
            if enemy.get_side_of_player(player) == owner_side:
                return True

        return False
    
    def get_melee_attack_slot_limit(self, owner):
        return getattr(owner, "melee_attack_slot_limit", None) or MAX_MELEE_ATTACKERS
    
    def count_active_melee_attackers(self, enemies):
        count = 0
        for enemy in enemies:
            if enemy.has_attack_slot:
                count += 1
        return count
    
    def should_flank(self, owner, player, distance_x, distance_y, enemies):
        if owner.can_bypass_attack_slot_limit():
            return False
        if not owner.uses_melee_attack_slot():
            return False
        if distance_x > owner.attack_range:
            return False
        # Why: enemies slightly above/below the attack lane should still 
        # try to flank into position instead of giving up immediately.
        if distance_y > owner.attack_lane_range + ENEMY_FLANK_Y_TOLERANCE:
            return False
        if self.count_active_melee_attackers(enemies) < self.get_melee_attack_slot_limit(owner):
            return False

        return True
