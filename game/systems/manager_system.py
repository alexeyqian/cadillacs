def update_manager_system(game_state):
    game_state.score_manager.update()
    game_state.announcement_manager.update()
    game_state.stage_clear_manager.update()