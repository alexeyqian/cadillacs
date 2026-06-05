import pygame
from game.settings import *

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

    # draw background
    #screen.fill((120, 190, 255))
    level.background.draw_back(screen, camera.x)
    level.draw_props(screen, camera.x, "back")
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
    # draw loots
    for loot in loot_items:
        loot.draw(screen, camera.x)

    #level.draw_props(screen, camera.x, "front")
    level.background.draw_front(screen, camera.x)

def main_draw_ui(game_state):
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

    font = pygame.font.SysFont(None, 30)
    small_font = pygame.font.SysFont(None, 20)
    big_font = pygame.font.SysFont(None, 60)

    # health UI
    pygame.draw.rect(screen,(100,100,100), (20,20,200,20))
    hp_width = int(200 * (player.hp / player.max_hp))
    pygame.draw.rect(screen, (0,255,0), (20,20,hp_width,20))
    hp_text = font.render(f"HP: {player.hp}/{player.max_hp}", True, (0,0,0))
    screen.blit(hp_text, (230, 20))
    # Weapon UI
    weapon_name = ""
    ammo_str = ""
    if player.weapon:
        weapon_name = player.weapon.weapon_type
        if player.weapon.is_ranged:
            ammo_str = f" Ammo:{player.weapon.ammo}"
        weapon_text = small_font.render(f"Weapon:{weapon_name}{ammo_str}",True,(0,0,0))
        screen.blit(weapon_text,(500, 20))
        
    # enemies UI
    #boss_alive = False
    #boss_str = ""
    #for enemy in enemies:
    #    if enemy.__class__.__name__ == "BossEnemy":
    #        boss_alive = True
    #if boss_alive:
    #    boss_str = "Boss Alive"
    #if boss_alive:
    #    boss_text = big_font.render("BOSS", True, (255,50,50))
    #    screen.blit(boss_text, (SCREEN_WIDTH//2 - 120, 80))

    # WIN OR GAME OVER UI
    if level.current_wave >= len(level.waves):
        stage_clear = big_font.render("Stage Clear - YOU WIN!", True, (0,200,0))
        screen.blit(stage_clear, stage_clear.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)))
    if player.state == player.DEAD:
        game_over_text = big_font.render("GAME OVER", True, (255,0,0))
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(game_over_text, game_over_rect)
    # if no enemies remain, show win screen and stop
    #if len(enemies) == 0:
    #    screen.fill((120, 190, 255))
    #    game_win_text = big_font.render("YOU WIN!", True, (255, 215, 0))
    #    game_win_rect = game_win_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    #    screen.blit(game_win_text, game_win_rect)
        #pygame.display.flip()
        #pygame.time.delay(2000)  # pause 2 seconds so player can see the message
        #running = False
        #continue

    # debug UI
    control_text = small_font.render("Attack:J, Shoot:K, Pickup:E, Drop:Q", True, (0,0,0))
    screen.blit(control_text, (20, 50))
    player_str =  f"Player x:{int(player.x)} y:{int(player.y)} State:{player.state} Combo:{player.combo_step} Camera x:{int(camera.x)} Wave:{level.current_wave + 1} Enemies:{len(enemies)}"
    player_text = small_font.render(player_str,True, (0,0,0))
    screen.blit(player_text, (400, 50))
    # end of debug text
