class EnemyActionController:
    def execute_state(self, owner, level, player, enemies, dx, dy):
        if owner.state == owner.PATROL:
            owner.update_patrol()
        elif owner.state == owner.CHASE:
            owner.update_chasing(player, dx, dy)
            owner.separate_from_other_enemies(enemies)
        elif owner.state == owner.ATTACK:
            owner.update_attack(level, player)
