class EnemyStateResolver:
    def choose_state(self, owner, distance_x, distance_y):
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
