import pygame
from game.settings import *
from game.colors import *

# draw order: 
# far background, mid background, ground layer, decorations behind player,
# player, enemies, objects, weapons, projectiles, foreground, decorations in front, ui
# world decorations: street lamps, destroyed signs, bones, trees, dinosaur skeletons etc
def main_draw(game_state):
    main_draw_world(game_state)
    main_draw_ui(game_state)

def main_draw_world(game_state):
    screen = game_state.screen
    camera = game_state.camera
    level = game_state.level
    player = game_state.player
    enemies = game_state.enemies
    weapons = game_state.weapons
    projectiles = game_state.projectiles
    enemy_projectiles = game_state.enemy_projectiles
    objects = game_state.objects
    loot_items = game_state.loot_items
    hit_sparks = game_state.hit_sparks
    floating_texts = game_state.floating_texts

    # draw background
    #screen.fill((120, 190, 255))
    level.background.draw_back(screen, camera.x)
    #level.draw_props(screen, camera.x, "back")
    exit_rect = pygame.Rect(level.exit_rect)
    if exit_rect and SHOW_EXIT_RECT:
        pygame.draw.rect(screen, YELLOW_COLOR, 
            (exit_rect.x - camera.x, exit_rect.y, exit_rect.width, exit_rect.height), 3)
    # ground
    #pygame.draw.rect(screen, (80, 180, 80),# green
    #                (0, LANE_TOP, SCREEN_WIDTH, 
    #                LANE_BOTTOM - LANE_TOP + player.height))

    # world markers - todo: remove
    #for x in range(0, WORLD_WIDTH, 200):
    #    screen_x = x - camera.x
    #    pygame.draw.line(
    #        screen, (150, 150, 150),
    #        (screen_x, LANE_TOP),
    #        (screen_x, LANE_BOTTOM+player.height),
    #        2
    #    )

    # depth sorting
    # Depth Sorting: Characters need to scale in size and dynamically re-order in front of 
    # or behind background props based on their Y-axis position.
    # Classic beat'em-up games draw lower objects later.
    # other wise, may render incorrectly.
    # higher y draw later, appears closer to camera
    # Exactly how arcade beat'em-ups fake depth.
    entities = []
    entities.append(player)
    for enemy in enemies:
        entities.append(enemy)
    entities.sort(key=lambda e: e.y)
    # draw entities
    for entity in entities:
        entity.draw(screen, camera.x)
    # draw weapons
    for weapon in weapons:
        weapon.draw(screen, camera.x)
    # draw player projectiles
    for projectile in projectiles:
        projectile.draw(screen, camera.x)
    # draw enemy projectiles
    for projectile in enemy_projectiles:
        projectile.draw(screen, camera.x)
    # draw hit sparks
    for spark in hit_sparks:
        spark.draw(screen, camera.x)
    # draw breakables
    for obj in objects:
        obj.draw(screen, camera.x)
    for explosion in game_state.explosions:
        explosion.draw(screen, camera.x)
    # draw loots
    for loot in loot_items:
        loot.draw(screen, camera.x)
    # draw floating texts
    for floating_text in floating_texts:
        floating_text.draw(screen, camera.x)

    #level.draw_props(screen, camera.x, "front")
    level.background.draw_front(screen, camera.x)

def main_draw_ui(game_state):
    screen = game_state.screen
    camera = game_state.camera
    level = game_state.level
    player = game_state.player
    enemies = game_state.enemies
    score_manager = game_state.score_manager

    small_font = pygame.font.SysFont(None, int(UI_FONT_SIZE*0.8))
    font = pygame.font.SysFont(None, UI_FONT_SIZE)
    big_font = pygame.font.SysFont(None, int(UI_FONT_SIZE*1.2))

    ############### HUD ###############
    # score
    score_text = font.render(
        f"SCORE {score_manager.score} | HI {score_manager.high_score}",True,BLACK_COLOR)
    screen.blit(score_text,(UI_FIRST_X, UI_FIRST_Y))

    # credits and lives
    next_life_text = small_font.render(
        f"CREDITS {game_state.credits} | LIVES: {player.lives} | NEXT LIFE {game_state.score_manager.next_extra_life_score}",
        True, BLACK_COLOR)
    screen.blit(next_life_text, (400, UI_FIRST_Y))

    # health UI
    pygame.draw.rect(screen,(100,100,100), (UI_FIRST_X,UI_FIRST_Y+UI_LINE_HEIGHT,200,20))
    hp_width = int(200 * (player.hp / player.max_hp))
    pygame.draw.rect(screen, GREEN_COLOR, (UI_FIRST_X,UI_FIRST_Y+UI_LINE_HEIGHT,hp_width,20))
    hp_text = font.render(f"HP: {int(player.hp)}/{player.max_hp}", True, BLACK_COLOR)
    screen.blit(hp_text, (240, UI_FIRST_Y+UI_LINE_HEIGHT))

    # control
    control_text = small_font.render("Run: Shift, Attack:J, Shoot:K, Grab/Throw:L, Drop:Q", True, BLACK_COLOR)
    screen.blit(control_text, (UI_FIRST_X + 450, UI_FIRST_Y+UI_LINE_HEIGHT))

    # combo UI
    combo = game_state.score_manager.combo_count
    multiplier = game_state.score_manager.get_multiplier()
    if combo > 1:
        combo_text = font.render(
            f"{combo} HIT COMBO x{multiplier}",
            True,BLACK_COLOR)
        screen.blit(combo_text,(450, UI_FIRST_Y))

    # Weapon UI
    weapon_name = ""
    ammo_str = ""
    if player.weapon:
        weapon_name = player.weapon.weapon_type
        if player.weapon.is_ranged:
            ammo_str = f" Ammo:{player.weapon.ammo}"
        weapon_text = font.render(f"Weapon:{weapon_name}{ammo_str}",True,BLACK_COLOR)
        screen.blit(weapon_text,(650, UI_FIRST_Y))

    # debug UI
    player_str = (f"State: {level.stage_name} Camera x:{int(camera.x)} "
                f"Player x:{int(player.x)} y:{int(player.y)} State:{player.state} "
                f"Wave:{level.current_wave + 1} Enemies:{len(enemies)}")
    player_text = small_font.render(player_str,True, BLACK_COLOR)
    screen.blit(player_text, (UI_FIRST_X, UI_FIRST_Y+2*UI_LINE_HEIGHT))
    # end of debug text

    # stage clear manager UI
    stage_clear = game_state.stage_clear_manager
    if stage_clear.active:
        title = big_font.render("WELL DONE!", True, YELLOW_COLOR)
        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH//2, 120)))

        life_text = font.render(
            f"Life Bonus: {stage_clear.life_bonus}",
            True, WHITE_COLOR)
        score_text = font.render(
            f"Score Bonus: {stage_clear.score_bonus}",
            True, WHITE_COLOR)
        total_text = font.render(
            f"TOTAL: {stage_clear.total_bonus}",
            True,YELLOW_COLOR)

        screen.blit(life_text,life_text.get_rect(center=(SCREEN_WIDTH//2, 220)))
        screen.blit(score_text,score_text.get_rect(center=(SCREEN_WIDTH//2, 270)))
        screen.blit(total_text,total_text.get_rect(center=(SCREEN_WIDTH//2, 340)))

        if stage_clear.timer <= 0:
            press_text = font.render("Press ENTER",True,WHITE_COLOR)
            screen.blit(press_text,press_text.get_rect(center=(SCREEN_WIDTH//2, 420)))

        return


    # WIN OR GAME OVER UI
    if level.current_wave >= len(level.waves):
        stage_clear = big_font.render("YOU WIN!", True, GREEN_COLOR)
        screen.blit(stage_clear, stage_clear.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)))
        #pygame.display.flip()
        #pygame.time.delay(2000)  # pause 2 seconds so player can see the message
        #running = False
        #continue
        return
    
    # announcement UI
    announcement = game_state.announcement_manager
    if announcement.active:
        flash_color = YELLOW_COLOR
        if announcement.title == "WARNING":
            if(announcement.timer // 10) % 2:
                flash_color = RED_COLOR
        title = big_font.render(announcement.title,True,flash_color)
        screen.blit(title,title.get_rect(
                center=(SCREEN_WIDTH // 2,140)))
        subtitle = big_font.render(announcement.subtitle,True,WHITE_COLOR)
        screen.blit(subtitle,subtitle.get_rect(
                center=(SCREEN_WIDTH // 2,210)))

    # Continue UI
    if game_state.continue_active:
        seconds = game_state.continue_timer // FPS
        continue_text = big_font.render(f"CONTINUE? {seconds}", True, YELLOW_COLOR)
        screen.blit(continue_text, continue_text.get_rect(center=(SCREEN_WIDTH//2,SCREEN_HEIGHT//2)))
        continue_hint_text = big_font.render(f"Press C to Continue, Credits: {game_state.credits}", True, WHITE_COLOR)
        screen.blit(continue_hint_text, continue_hint_text.get_rect(center=(SCREEN_WIDTH//2,SCREEN_HEIGHT//2 + 60)))
        return

    if player.state == player.DEAD and player.lives <= 0:
        game_over_text = big_font.render("GAME OVER", True, RED_COLOR)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(game_over_text, game_over_rect)
        return