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

    # Enemy has attack slot -> attacks
    # Enemy is in range but slot is full -> moves toward a side position
    # Enemy groups spread around player instead of stacking directly
    # pick less crowded side and drift there

    # With 1 slot: closest eligible enemy on its side attacks
    # With future 2 slots: one enemy per side can attack
    # Enemies without slots flank toward less crowded side
    # Flanking movement code is easier to read
    def update_chasing(self, owner, player, dx, dy):
        if owner.flank_target_side:
            target_x, target_y = owner.get_flank_target_position(player)
            self.move_toward_point(owner, target_x, target_y)
            return

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
                    
    def move_toward_point(self, owner, target_x, target_y):
        if abs(owner.x - target_x) > owner.speed:
            if owner.x < target_x:
                owner.x += owner.speed
                owner.facing_right = True
            else:
                owner.x -= owner.speed
                owner.facing_right = False

        if abs(owner.y - target_y) > owner.speed:
            if owner.y < target_y:
                owner.y += owner.speed
            else:
                owner.y -= owner.speed
