from game.settings import MAX_MELEE_ATTACKERS

class EnemyStateResolver:
    def choose_state(self, owner, player, distance_x, distance_y, enemies):
        if owner.state == owner.ATTACK:
            return

        if self.can_attack_player(owner, player, distance_x, distance_y, enemies):
            owner.flank_target_side = None
            owner.start_attack()
        elif distance_x <= owner.detect_range:
            if self.should_flank(owner, player, distance_x, distance_y, enemies):
                owner.set_flank_target(player, enemies)
            else:
                owner.flank_target_side = None
            # todo: replace with entry function like: start_chase()
            owner.state = owner.CHASE
        else:
            owner.flank_target_side = None
            # todo: replace with: start_patrol()
            owner.state = owner.PATROL

    def can_attack_player(self, owner, player, distance_x, distance_y, enemies):
        if owner.attack_cooldown > 0:
            return False
        if distance_x > owner.attack_range:
            return False
        if distance_y > owner.attack_lane_range:
            return False
        if owner.can_bypass_attack_slot_limit():
            return True
        # only the closest eligible melee enemy should take the slot. 
        # This makes group behavior feel more intentional.
        if self.count_active_melee_attackers(enemies) >= self.get_max_melee_attackers(owner):
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
    
    def get_max_melee_attackers(self, owner):
        return getattr(owner, "max_melee_attackers", MAX_MELEE_ATTACKERS)
    
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
        if distance_y > owner.attack_lane_range:
            return False
        if self.count_active_melee_attackers(enemies) < self.get_max_melee_attackers(owner):
            return False

        return True