class EnemyAIMixin:
    def get_player_distance(self, player):
        self.movement.get_player_distance(self, player)

    def face_player(self, player):
        self.movement.face_player(self, player)

    def choose_state(self, distance_x, distance_y):
        if self.state == self.ATTACK:
            return

        # state selection, attack if close enough
        if (self.attack_cooldown <= 0
            and distance_x <= self.attack_range
            and distance_y <= self.attack_lane_range):
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
        self.movement.update_patrol(self)

    def update_chasing(self, dx, dy):
        self.movement.update_chasing(self, dx, dy)

    def separate_from_other_enemies(self, enemies):
        self.movement.separate_from_other_enemies(self, enemies)