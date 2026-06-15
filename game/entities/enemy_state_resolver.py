from game.settings import MAX_MELEE_ATTACKERS

class EnemyStateResolver:
    def choose_state(self, owner, player, distance_x, distance_y, enemies):
        if owner.state == owner.ATTACK:
            return

        if self.can_attack_player(owner, player, distance_x, distance_y, enemies):
            owner.start_attack()
        elif distance_x <= owner.detect_range:
            # todo: replace with entry function like: start_chase()
            owner.state = owner.CHASE
        else:
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
        if not self.is_closest_melee_attacker(owner, player, enemies):
            return False
        
        active_melee_attackers = 0
        for enemy in enemies:
            if enemy is owner:
                continue
            if enemy.has_attack_slot:
                active_melee_attackers += 1
        return active_melee_attackers < MAX_MELEE_ATTACKERS
    
    def is_closest_melee_attacker(self, owner, player, enemies):
        closest_enemy = owner
        closest_distance = float("inf")

        for enemy in enemies:
            if not enemy.uses_melee_attack_slot():
                continue
            if enemy.attack_cooldown > 0:
                continue
            if enemy.state in [enemy.DEAD, enemy.HIT, enemy.GRABBED, enemy.THROWN, enemy.KNOCKDOWN, enemy.GETUP]:
                continue

            dx = abs(enemy.x - player.x)
            dy = abs(enemy.y - player.y)

            if dx > enemy.attack_range or dy > enemy.attack_lane_range:
                continue

            if dx < closest_distance:
                closest_distance = dx
                closest_enemy = enemy

        return closest_enemy is owner
