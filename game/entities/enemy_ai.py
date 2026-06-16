class EnemyAIMixin:
    def get_player_distance(self, player):
        return self.movement.get_player_distance(self, player)

    def face_player(self, player):
        self.movement.face_player(self, player)

    def choose_state(self, level, player, distance_x, distance_y, enemies):
        self.state_resolver.choose_state(self, level, player, distance_x, distance_y, enemies)

    def execute_state(self, level, player, enemies, dx, dy):
        self.action_controller.execute_state(self, level, player, enemies, dx, dy)

    
    # enemy patrol back and forth
    def update_patrol(self):
        self.movement.update_patrol(self)

    def update_chasing(self, player, dx, dy):
        self.movement.update_chasing(self,player, dx, dy)

    def separate_from_other_enemies(self, enemies):
        self.movement.separate_from_other_enemies(self, enemies)