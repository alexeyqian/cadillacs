class EnemyActionController:
    # todo: rename to execute_action?
    def execute_state(self, owner, player, enemies, dx, dy):
        if owner.state == owner.PATROL:
            owner.update_patrol()

        elif owner.state == owner.CHASE:
            owner.update_chasing(dx, dy)
            owner.separate_from_other_enemies(enemies)

        elif owner.state == owner.ATTACK:
            owner.update_attack(player)
