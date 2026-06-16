import pygame
# module import is the right choice for mutable runtime flags
import game.settings as settings
from game.settings import *
from game.colors import *
from game.level.lane import LaneSystem
from game.entities.attack_debug import format_attack_debug_lines

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
    draw_exit_rect(screen, camera, level)
    draw_entity_lane_debug(screen, level, camera, player, enemies)
    draw_player_debug_boxes(screen, level, camera, player)
    draw_projectile_lane_debug(screen, level, camera, projectiles, enemy_projectiles)

def draw_exit_rect(screen, camera, level):
    if not SHOW_EXIT_RECT:
        return

    exit_rect = pygame.Rect(level.exit_rect)
    screen_rect = pygame.Rect(
        exit_rect.x - camera.x,
        exit_rect.y,
        exit_rect.width,
        exit_rect.height
    )
    pygame.draw.rect(screen, YELLOW_COLOR, screen_rect, 6)

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
    left_x = UI_FIRST_X
    right_x = screen.get_width() - UI_FIRST_X
    top_y = UI_FIRST_Y
    row_gap = 8
    small_line = small_font.get_linesize()
    font_line = font.get_linesize()

    score_text = font.render(
        f"SCORE {score_manager.score} | HI {score_manager.high_score}",True,BLACK_COLOR)
    score_rect = score_text.get_rect(topleft=(left_x, top_y))

    status_text = small_font.render(
        f"CREDITS {game_state.credits} | LIVES {player.health.lives} | NEXT LIFE {game_state.score_manager.next_extra_life_score}",
        True, BLACK_COLOR)
    status_rect = status_text.get_rect(topright=(right_x, top_y))
    if status_rect.left <= score_rect.right + 24:
        status_rect.top = score_rect.bottom + row_gap

    screen.blit(score_text, score_rect)
    screen.blit(status_text, status_rect)

    # health UI
    hp_bar_w = 220
    hp_bar_h = 20
    hp_y = max(score_rect.bottom, status_rect.bottom) + row_gap
    pygame.draw.rect(screen, (100, 100, 100), (left_x, hp_y, hp_bar_w, hp_bar_h))
    hp_ratio = max(0.0, min(1.0, player.health.hp / player.health.max_hp))
    hp_width = int(hp_bar_w * hp_ratio)
    pygame.draw.rect(screen, GREEN_COLOR, (left_x, hp_y, hp_width, hp_bar_h))
    hp_text = font.render(f"HP: {int(player.health.hp)}/{player.health.max_hp}", True, BLACK_COLOR)
    hp_text_rect = hp_text.get_rect(topleft=(left_x + hp_bar_w + 16, hp_y - 4))
    screen.blit(hp_text, hp_text_rect)

    # control
    #control_text = small_font.render("Run: Shift, Attack:J, Shoot:K, Grab/Throw:L, Drop:Q", True, BLACK_COLOR)
    #screen.blit(control_text, (UI_FIRST_X + 450, UI_FIRST_Y+UI_LINE_HEIGHT))

    right_panel_y = status_rect.bottom + row_gap

    # Weapon UI
    weapon = player.weapon_slot.weapon
    if weapon:
        weapon_name = weapon.weapon_type
        ammo_str = f" Ammo:{weapon.ammo}" if weapon.is_ranged else ""
        weapon_text = font.render(f"Weapon: {weapon_name}{ammo_str}", True, BLACK_COLOR)
        screen.blit(weapon_text, weapon_text.get_rect(topright=(right_x, right_panel_y)))
        right_panel_y += font_line + row_gap

    # combo UI
    combo = game_state.score_manager.combo_count
    multiplier = game_state.score_manager.get_multiplier()
    if combo > 1:
        combo_text = font.render(
            f"{combo} HIT COMBO x{multiplier}",
            True,BLACK_COLOR)
        screen.blit(combo_text, combo_text.get_rect(
            midtop=(screen.get_width() // 2, hp_y)))

    # debug UI
    player_feet_x, player_feet_y = player.get_logical_rect().midbottom
    debug_y = max(hp_y + hp_bar_h, hp_text_rect.bottom) + row_gap
    debug_lines = [
        f"Stage: {level.stage_name} | Camera x:{int(camera.x)} | Wave:{level.current_wave + 1} | Enemies:{len(enemies)}",
        f"Player feet x:{int(player_feet_x)} y:{int(player_feet_y)} | State:{player.state}",
    ]

    for debug_line in debug_lines:
        debug_text = small_font.render(debug_line, True, BLACK_COLOR)
        screen.blit(debug_text, (left_x, debug_y))
        debug_y += small_line
    
    if settings.SHOW_COMBAT_BOXES:
        active_slots = 0
        max_slots = MAX_MELEE_ATTACKERS

        for enemy in enemies:
            attack_state = getattr(enemy, "attack_state", None)
            has_attack_slot = (
                attack_state.has_slot
                if attack_state
                else getattr(enemy, "has_attack_slot", False)
            )
            if has_attack_slot:
                active_slots += 1
                max_slots = getattr(enemy, "melee_attack_slot_limit", None) or max_slots

        slot_text = small_font.render(f"Attack Slots: {active_slots}/{max_slots}",True,BLACK_COLOR)
        screen.blit(slot_text, (left_x, debug_y))
        debug_y += small_line

        attack_debug_lines = format_attack_debug_lines(
            "Player attack",
            player.combat.attack_controller,
            damage=player.combat.get_attack_damage(player),
            lane_reach=player.combat.get_attack_lane_reach(player),
        )
        for debug_line in attack_debug_lines:
            debug_text = small_font.render(debug_line, True, BLACK_COLOR)
            screen.blit(debug_text, (left_x, debug_y))
            debug_y += small_line

        active_enemy_debug_count = 0
        for enemy in enemies:
            if active_enemy_debug_count >= 3:
                break
            if enemy.state != enemy.ATTACK:
                continue

            attack_state = getattr(enemy, "attack_state", None)
            attack_controller = (
                attack_state.controller
                if attack_state
                else getattr(enemy, "attack_controller", None)
            )
            if not attack_controller:
                continue

            enemy_debug_lines = format_attack_debug_lines(
                enemy.display_name,
                attack_controller,
                damage=enemy.attack_damage,
                lane_reach=enemy.attack_lane_reach,
            )
            for debug_line in enemy_debug_lines:
                debug_text = small_font.render(debug_line, True, BLACK_COLOR)
                screen.blit(debug_text, (left_x, debug_y))
                debug_y += small_line

            active_enemy_debug_count += 1
    
    # end of debug text

    # stage clear manager UI
    stage_clear = game_state.stage_clear_manager
    if stage_clear.active:
        if game_state.stage_manager.has_next_stage():
            next_text = big_font.render("GO TO NEXT", True, YELLOW_COLOR)
            screen.blit(next_text, next_text.get_rect(
                center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)))
            return

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

        return


    # WIN OR GAME OVER UI
    if level.current_wave >= len(level.waves):
        exit_hint = big_font.render("GO TO EXIT", True, GREEN_COLOR)
        screen.blit(exit_hint, exit_hint.get_rect(
            center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)))
        return
    
    # announcement UI
    announcement = game_state.announcement_manager
    if announcement.active:
        flash_color = YELLOW_COLOR
        if announcement.title == "WARNING":
            if(announcement.timer // 10) % 2:
                flash_color = RED_COLOR
        title = big_font.render(announcement.title,True,flash_color)
        subtitle = big_font.render(announcement.subtitle,True,WHITE_COLOR)
        title_bounds = title.get_bounding_rect()
        subtitle_bounds = subtitle.get_bounding_rect()
        center_x = screen.get_width() // 2
        gap = 18
        total_height = title_bounds.height + gap + subtitle_bounds.height
        start_y = (screen.get_height() - total_height) // 2

        title_x = center_x - title_bounds.width // 2 - title_bounds.x
        title_y = start_y - title_bounds.y
        subtitle_x = center_x - subtitle_bounds.width // 2 - subtitle_bounds.x
        subtitle_y = (start_y + title_bounds.height
                    + gap - subtitle_bounds.y)

        screen.blit(title, (title_x, title_y))
        screen.blit(subtitle, (subtitle_x, subtitle_y))

    # Continue UI
    if game_state.continue_active:
        seconds = game_state.continue_timer // FPS
        continue_text = big_font.render(f"CONTINUE? {seconds}", True, YELLOW_COLOR)
        screen.blit(continue_text, continue_text.get_rect(center=(SCREEN_WIDTH//2,SCREEN_HEIGHT//2)))
        continue_hint_text = big_font.render(f"Press C to Continue, Credits: {game_state.credits}", True, WHITE_COLOR)
        screen.blit(continue_hint_text, continue_hint_text.get_rect(center=(SCREEN_WIDTH//2,SCREEN_HEIGHT//2 + 60)))
        return

    if player.state == player.DEAD and player.health.lives <= 0:
        game_over_text = big_font.render("GAME OVER", True, RED_COLOR)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(game_over_text, game_over_rect)
        return

def draw_player_debug_boxes(screen, level, camera, player):
    if not settings.SHOW_COMBAT_BOXES:
        return

    collision_rect = player.get_collision_rect()
    body_rect = player.get_logical_rect()
    hurt_rect = player.get_hurt_rect()
    counter_hurt_rect = player.get_counter_hurt_rect()
    attack_rect = player.get_attack_rect()

    # blue = collision / feet box
    pygame.draw.rect(screen, BLUE_COLOR, (
        collision_rect.x - camera.x,
        collision_rect.y,
        collision_rect.width,
        collision_rect.height
    ), 1)
    # small feet anchor marker
    pygame.draw.circle(
        screen,
        WHITE_COLOR,
        (int(player.x - camera.x), int(player.y)),
        3
    )

    # white = full animation frame / visual reference
    pygame.draw.rect(screen, WHITE_COLOR, (
        body_rect.x - camera.x,
        body_rect.y,
        body_rect.width,
        body_rect.height
    ), 1)

    # green = current animation frame hurt box
    if hurt_rect and hurt_rect.width > 0 and hurt_rect.height > 0:
        pygame.draw.rect(screen, GREEN_COLOR, (
            hurt_rect.x - camera.x,
            hurt_rect.y,
            hurt_rect.width,
            hurt_rect.height
        ), 2)
        
    # orange = counter-hurtbox / extended limb vulnerability
    if counter_hurt_rect and counter_hurt_rect.width > 0 and counter_hurt_rect.height > 0:
        pygame.draw.rect(screen, ORANGE_COLOR, (
            counter_hurt_rect.x - camera.x,
            counter_hurt_rect.y,
            counter_hurt_rect.width,
            counter_hurt_rect.height
        ), 2)

    # red = current animation frame attack box
    if attack_rect and attack_rect.width > 0 and attack_rect.height > 0:
        pygame.draw.rect(screen, RED_COLOR, (
            attack_rect.x - camera.x,
            attack_rect.y,
            attack_rect.width,
            attack_rect.height
        ), 2)

    timing_label = player.combat.get_attack_timing_label()
    if timing_label:
        font = pygame.font.SysFont(None, 20)
        label = font.render(timing_label, True, YELLOW_COLOR)
        screen.blit(label, (int(player.x - camera.x - 42), int(player.y - 210)))


def draw_entity_lane_debug(screen, level, camera, player, enemies):
    if not settings.SHOW_COMBAT_BOXES:
        return

    lane_system = level.lane_system
    font = pygame.font.SysFont(None, 20)
    lane_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

    lane_debug_rows = []

    # Each lane has equal height. Draw lane areas and boundaries clearly;
    # center lines are only the ideal standing/depth positions.
    for lane_index in range(lane_system.lane_count):
        top, bottom = lane_system.get_lane_bounds(lane_index)
        center_y = lane_system.get_lane_center(lane_index)
        top = int(top)
        bottom = int(bottom)
        center_y = int(center_y)
        lane_height = bottom - top

        band_color = (255, 255, 0, 20) if lane_index % 2 == 0 else (0, 255, 0, 14)
        pygame.draw.rect(lane_overlay, band_color, (0, top, SCREEN_WIDTH, lane_height))
        lane_debug_rows.append((lane_index, top, center_y, lane_height))

    screen.blit(lane_overlay, (0, 0))

    for lane_index, top, center_y, lane_height in lane_debug_rows:
        pygame.draw.line(screen, YELLOW_COLOR, (0, top), (SCREEN_WIDTH, top), 2)

        for dash_x in range(0, SCREEN_WIDTH, 36):
            pygame.draw.line(
                screen,
                (220, 220, 120),
                (dash_x, center_y),
                (min(dash_x + 18, SCREEN_WIDTH), center_y),
                1
            )

        label = font.render(f"LANE {lane_index}  {lane_height}px", True, YELLOW_COLOR)
        screen.blit(label, (8, center_y - 8))

    # Draw walkable bounds last so the full top-to-bottom range is obvious.
    pygame.draw.line(screen, GREEN_COLOR,
        (0, int(level.lane_top)),
        (SCREEN_WIDTH, int(level.lane_top)), 3)
    pygame.draw.line(screen, GREEN_COLOR,
        (0, int(level.lane_bottom)),
        (SCREEN_WIDTH, int(level.lane_bottom)), 3)
    pygame.draw.line(screen, YELLOW_COLOR,
        (0, int(level.lane_bottom)),
        (SCREEN_WIDTH, int(level.lane_bottom)), 2)

    # draw player lane
    player_lane = lane_system.get_lane_index(player.y)
    player_label = font.render(f"P LANE {player_lane}", True, YELLOW_COLOR)
    screen.blit(player_label, (int(player.x - camera.x - 30), int(player.y + 20)))

    # draw enemies' lanes
    for enemy in enemies:
        enemy_lane = lane_system.get_lane_index(enemy.y)
        enemy_label = font.render(f"E LANE {enemy_lane}", True, YELLOW_COLOR)
        screen.blit(enemy_label, (int(enemy.x - camera.x - 30), int(enemy.y + 20)))

def draw_projectile_lane_debug(screen, level, camera, projectiles, enemy_projectiles):
    if not settings.SHOW_COMBAT_BOXES:
        return

    font = pygame.font.SysFont(None, 18)

    all_projectiles = []
    all_projectiles.extend(projectiles)
    all_projectiles.extend(enemy_projectiles)

    for projectile in all_projectiles:
        if not projectile.active:
            continue

        lane_index = level.get_lane_index(projectile.lane_y)
        label = font.render(
            f"L{lane_index} R{projectile.lane_reach}",
            True,
            YELLOW_COLOR
        )

        screen.blit(
            label,
            (int(projectile.x - camera.x - 18), int(projectile.y - 28))
        )
