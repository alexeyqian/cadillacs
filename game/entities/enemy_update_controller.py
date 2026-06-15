class EnemyUpdateController:
    def update(self, owner, player, enemies):
        if owner.update_special_states():
            return

        owner.update_timers()

        if owner.update_hit_state():
            return

        owner.apply_knockback()

        dx, dy, distance_x, distance_y = owner.get_player_distance(player)

        if distance_x <= owner.detect_range:
            owner.face_player(player)

        owner.choose_state(player, distance_x, distance_y, enemies)
        owner.execute_state(player, enemies, dx, dy)

        # owner.apply_world_bounds()
        owner.update_animation()
