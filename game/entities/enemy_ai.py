class EnemyAIMixin:
    def get_player_distance(self, player):
        dx = player.x - self.x
        dy = player.y - self.y

        distance_x = abs(dx)
        distance_y = abs(dy)

        return dx, dy, distance_x, distance_y

    def face_player(self, player):
        self.facing_right = player.x > self.x

    def choose_state(self, distance_x, distance_y):
        if self.state == self.ATTACK:
            return

        # state selection, attack if close enough
        if (self.attack_cooldown <= 0
            and distance_x <= self.attack_hitbox_w
            and distance_y <= self.attack_hitbox_h):
            self.state = self.ATTACK
        elif distance_x <= self.detect_range:
            self.state = self.CHASE
        else:
            self.state = self.PATROL

    def execute_state(self, player, enemies, dx, dy):
        if self.state == self.PATROL:
            self.update_patrol()
        elif self.state == self.CHASE:
            self.update_chasing(dx, dy)
            self.separate_from_other_enemies(enemies)
        elif self.state == self.ATTACK:
            self.update_attack(player)
            
    
    # enemy patrol back and forth
    def update_patrol(self):
        self.x += self.patrol_direction
        if self.patrol_direction > 0:
            self.facing_right = True
        elif self.patrol_direction < 0:
            self.facing_right = False
        if self.x > self.spawn_x + self.patrol_distance:
            self.patrol_direction = -1
        if self.x < self.spawn_x - self.patrol_distance:
            self.patrol_direction = 1

    def update_chasing(self, dx, dy):
        # horizontal movement
        if dx > 0:
            self.x += self.speed
            self.facing_right = True
        elif dx < 0:
            self.x -= self.speed
            self.facing_right = False
        # vertical movement
        if abs(dy) > 10: # allow some vertical leniency
            if dy > 0:
                self.y += self.speed
            else:
                self.y -= self.speed

    def separate_from_other_enemies(self, enemies):
        for other in enemies:
            if other is self:
                continue
            if other.state == self.DEAD:
                continue
            dx = other.x - self.x
            if abs(dx) < 40:
                if dx > 0:
                    self.x -= 1
                else:
                    self.x += 1