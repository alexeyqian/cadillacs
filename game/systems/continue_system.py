import pygame

def update_continue_system(game_state, keys):
    player = game_state.player
    
    if not game_state.continue_active:
        return

    if game_state.continue_timer > 0:
        game_state.continue_timer -= 1
    if game_state.continue_timer <= 0:
        game_state.continue_active = False

    # keys = pygame.key.get_pressed()
    if keys[pygame.K_c]:
        if game_state.credits <= 0:
            return
        game_state.credits -= 1

        player.health.lives = 3
        player.health.hp = player.health.max_hp
        player.state = player.IDLE
        player.x = player.respawn_x
        player.y = player.respawn_y
        
        game_state.continue_timer = 600
        game_state.continue_active = False
        # todo: add limits for continue times
        game_state.continue_used += 1
