from game.settings import MAX_MELEE_ATTACKERS

class EnemyStateResolver:
    def choose_state(self, owner, distance_x, distance_y, enemies):
        if owner.state == owner.ATTACK:
            return

        if (
            owner.attack_cooldown <= 0
            and distance_x <= owner.attack_range
            and distance_y <= owner.attack_lane_range
        ):
            owner.start_attack()
        elif distance_x <= owner.detect_range:
            # todo: replace with entry function like: start_chase()
            owner.state = owner.CHASE
        else:
            # todo: replace with: start_patrol()
            owner.state = owner.PATROL

    def can_attack_player(self, owner, distance_x, distance_y, enemies):
        if owner.attack_cooldown > 0:
            return False
        if distance_x > owner.attack_range:
            return False
        if distance_y > owner.attack_lane_range:
            return False
        if owner.can_bypass_attack_slot_limit():
            return True
        
        active_melee_attackers = 0
        for enemy in enemies:
            if enemy is owner:
                continue
            if enemy.has_attack_slot:
                active_melee_attackers += 1
        return active_melee_attackers < MAX_MELEE_ATTACKERS