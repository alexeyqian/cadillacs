class EnemyMovement:
    def get_player_distance(self, owner, player):
        dx = player.x - owner.x
        dy = player.y - owner.y

        distance_x = abs(dx)
        distance_y = abs(dy)

        return dx, dy, distance_x, distance_y

    def face_player(self, owner, player):
        owner.facing_right = player.x > owner.x

    def update_patrol(self, owner):
        owner.x += owner.patrol_direction

        if owner.patrol_direction > 0:
            owner.facing_right = True
        elif owner.patrol_direction < 0:
            owner.facing_right = False

        if owner.x > owner.spawn_x + owner.patrol_distance:
            owner.patrol_direction = -1

        if owner.x < owner.spawn_x - owner.patrol_distance:
            owner.patrol_direction = 1

    def update_chasing(self, owner, dx, dy):
        if dx > 0:
            owner.x += owner.speed
            owner.facing_right = True
        elif dx < 0:
            owner.x -= owner.speed
            owner.facing_right = False

        if abs(dy) > 10:
            if dy > 0:
                owner.y += owner.speed
            else:
                owner.y -= owner.speed

    def separate_from_other_enemies(self, owner, enemies):
        for other in enemies:
            if other is owner:
                continue

            if other.state == owner.DEAD:
                continue

            dx = other.x - owner.x

            if abs(dx) < 40:
                if dx > 0:
                    owner.x -= 1
                else:
                    owner.x += 1
