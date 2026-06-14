class EnemyStateResolver:
    def choose_state(self, owner, distance_x, distance_y):
        if owner.state == owner.ATTACK:
            return

        if (
            owner.attack_cooldown <= 0
            and distance_x <= owner.attack_range
            and distance_y <= owner.attack_lane_range
        ):
            owner.state = owner.ATTACK
        elif distance_x <= owner.detect_range:
            owner.state = owner.CHASE
        else:
            owner.state = owner.PATROL
