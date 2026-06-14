class EnemyAIMixin:
    def get_player_distance(self, player):
        return self.movement.get_player_distance(self, player)

    def face_player(self, player):
        self.movement.face_player(self, player)

    def choose_state(self, distance_x, distance_y):
        self.state_resolver.choose_state(self, distance_x, distance_y)

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