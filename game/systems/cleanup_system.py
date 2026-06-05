def cleanup_game_state(game_state):
    # remove dead enemies
    game_state.enemies[:] = [
        enemy for enemy in game_state.enemies
        if not enemy.is_ready_to_remove()
    ]
    # clean up player projectiles
    game_state.projectiles[:] = [p for p in game_state.projectiles if p.active]
    # clean up enemy projectiles
    game_state.enemy_projectiles[:] = [
        p for p in game_state.enemy_projectiles
        if p.active
    ]
    # clean up breakables
    game_state.objects[:] = [obj for obj in game_state.objects if obj.hp > 0]
    # clean up loots
    game_state.loot_items[:] = [l for l in game_state.loot_items if l.active]
    # clean up hit sparks
    game_state.hit_sparks[:] = [s for s in game_state.hit_sparks if s.active]
    # clean floating text
    game_state.floating_texts[:] = [item for item in game_state.floating_texts if item.active]
