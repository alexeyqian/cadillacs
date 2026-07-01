class ProjectileSystem:
    @staticmethod
    def collect_player(game_state):
        for event in game_state.player.events.drain("spawn_projectile"):
            game_state.projectiles.append(event["payload"])

    @staticmethod
    def collect_enemy(game_state, enemy):
        if not enemy.pending_projectile:
            return
        game_state.enemy_projectiles.append(enemy.pending_projectile)
        enemy.pending_projectile = None

    @staticmethod
    def update(game_state):
        for projectile in game_state.projectiles:
            projectile.update(game_state.level.world_width)
        for projectile in game_state.enemy_projectiles:
            projectile.update(game_state.level.world_width)
