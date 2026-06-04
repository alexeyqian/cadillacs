import pygame
from game.settings import *
from game.camera import Camera
from game.level.level import Level
from game.level.wave import SpawnWave
from game.entities.player import Player
from game.entities.enemy import Enemy
from game.entities.weapon import Weapon
from game.entities.loot import Loot
from game.entities.breakable_object import BreakableObject

def create_enemy_rect(enemy):
    return pygame.Rect(enemy.x, enemy.y,
                enemy.width, enemy.height)

# level manages progression
# camera manages view
# wave manages spawning
# enemy manages AI

def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Cadillacs and Dinosaurs")

    clock = pygame.time.Clock()
    player = Player()
    level = Level()
    camera = Camera()
    enemies = []
    weapons = [
            Weapon(900,350, "knife"),
            Weapon(1500,350, "bat"),
            Weapon(2000, 350, "pistol")]
    projectiles = []
    enemy_projectiles = []
    # breakable objects
    objects = [
        BreakableObject(1100, 360),
        BreakableObject(1800, 360),
        BreakableObject(2500, 360),
    ]
    loot_items = []

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # create/trigger wave when player reaches trigger_x
        wave = level.get_current_wave()
        # only for SpawnWave
        if wave and wave.started:
            if hasattr(wave, "update"):
                enemies.extend(wave.update())

        # for normal Wave and BossWave
        # since they dont' implement update()
        if wave and not wave.started and player.x >= wave.trigger_x:
            # start the wave and initialize pending enemies
            wave.spawn()
            # lock camera only when wave actually starts
            # set lock_x to current camera.x so the viewport does not jump
            level.camera_locked = True
            level.lock_x = camera.x

        # if wave has started, spawn pending enemies over time
        if wave and wave.started:
            new_enemies = wave.update_spawn()
            if new_enemies:
                enemies.extend(new_enemies)
        # create loots when breakable destroys
        for enemy in enemies:
            if enemy.hp > 0:
                continue
            if enemy.loot_generated:
                continue
            loot = enemy.create_loot()
            if loot:
                loot_items.append(loot)
            enemy.loot_generated = True

        # collect player projectiles
        if player.pending_projectile:
            projectiles.append(player.pending_projectile)
            player.pending_projectile = None

        keys = pygame.key.get_pressed()
        update_player_weapon_interaction(player, weapons, keys)

        # auto pickup loot
        player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
        for loot in loot_items:
            if not loot.active:
                continue
            if player_rect.colliderect(loot.get_rect()):
                if loot.loot_type == "health":
                    player.hp = min(player.max_hp, player.hp + 30)
                elif loot.loot_type == "ammo":
                    if player.weapon and hasattr(player.weapon, "ammo"):
                        player.weapon.ammo += 10
                loot.active = False
        ############# update #############
        # update player
        player.update()
        # should move to player's own update() function
        # prevent escaping arena
        if level.camera_locked:
            left_wall = level.lock_x
            right_wall = level.lock_x + SCREEN_WIDTH - player.width
            if player.x < left_wall:
                player.x = left_wall
            if player.x > right_wall:
                player.x = right_wall

        # update enemies
        for enemy in enemies:
            enemy.update(player, enemies)
            if hasattr(enemy, "pending_projectile"):
                if enemy.pending_projectile:
                    enemy_projectiles.append(enemy.pending_projectile)
                    enemy.pending_projectile = None

        # update player projectiles
        for projectile in projectiles:
            projectile.update()

        # update enemy projectiles
        for projectile in enemy_projectiles:
            projectile.update()

        # update camera
        if level.camera_locked:
            camera.update(player, level.lock_x)
        else:
            camera.update(player)

        # player attack collision / combat detection
        attack_rect = player.get_attack_rect()
        if attack_rect and not player.already_hit_enemy:
            # attack enemies
            for enemy in enemies:
                enemy_rect = create_enemy_rect(enemy)
                if attack_rect.colliderect(enemy_rect):
                    enemy.take_damage(player.attack_damage(), player.x)
                    player.already_hit_enemy = True
                    break # ?? useless
            # attack breakables
            for obj in objects:
                if obj.destroyed:
                    continue
                if attack_rect.colliderect(obj.get_rect()):
                    obj.take_damage(player.attack_damage())

        # player projectile collision
        for projectile in projectiles:
            if not projectile.active:
                continue
            projectile_rect = projectile.get_rect()
            # projectile hit enemy
            for enemy in enemies:
                enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
                if projectile_rect.colliderect(enemy_rect):
                    enemy.take_damage(projectile.damage, player.x)
                    projectile.active = False
                    break
            # projectile hit breakable
            for obj in objects:
                if obj.destroyed:
                    continue
                if projectile_rect.colliderect(obj.get_rect()):
                    obj.take_damage(projectile.damage)
                    projectile.active = False
                    break

        # enemy projectile collision
        for projectile in enemy_projectiles:
            if not projectile.active:
                continue
            player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
            if projectile.get_rect().colliderect(player_rect):
                player.take_damage(projectile.damage)
                projectile.active = False

        # Create loot after combat damage, before destroyed objects are removed.
        for obj in objects:
            if obj.destroyed and not obj.loot_generated:
                loot = obj.create_loot()
                if loot:
                    loot_items.append(loot)
                obj.loot_generated = True
        
        # remove dead enemies
        enemies = [enemy for enemy in enemies if enemy.hp > 0]
        # clean up player projectiles
        projectiles = [p for p in projectiles if p.active]
        # clean up enemy projectiles
        enemy_projectiles = [p for p in enemy_projectiles if p.active]
        # clean up breakables
        objects = [obj for obj in objects if obj.hp > 0]
        # clean up loots
        loot_items = [l for l in loot_items if l.active]

        # wave completion logic
        wave = level.get_current_wave()
        if wave and wave.started:
            wave_finished = False
            if isinstance(wave, SpawnWave):
                wave_finished = wave.all_spawners_finished() and len(enemies) == 0
            else:
                wave_finished = len(enemies) == 0

            if wave_finished:
                wave.completed = True
                level.current_wave += 1
                level.camera_locked = False

        ############# draw #############
        main_draw(screen, camera, level, player, enemies, 
                    weapons, projectiles, enemy_projectiles, objects, loot_items)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

def update_player_weapon_interaction(player,weapons,keys):
    if keys[pygame.K_e]:
        if player.weapon is None:
            player_rect = pygame.Rect(
                player.x,player.y,
                player.width,player.height)
            for weapon in weapons:
                if weapon.picked_up:
                    continue
                if player_rect.colliderect(weapon.get_rect()):
                    player.pick_up_weapon(weapon)
                    break
    if keys[pygame.K_q]:
        player.drop_weapon()

def main_draw(screen, camera, level, player, enemies, 
                    weapons, projectiles, enemy_projectiles, objects, loot_items):
    main_draw_world(screen, camera, level, player, enemies, 
                    weapons, projectiles, enemy_projectiles, objects, loot_items)
    main_draw_ui(screen, camera, level, player, enemies, 
                    weapons, projectiles, enemy_projectiles, objects, loot_items)

def main_draw_world(screen, camera, level, player, enemies, 
                    weapons, projectiles, enemy_projectiles, objects, loot_items):
    # draw background
    screen.fill((120, 190, 255))
    # ground
    pygame.draw.rect(screen, (80, 180, 80),# green
                    (0, LANE_TOP, SCREEN_WIDTH, 
                    LANE_BOTTOM - LANE_TOP + player.height))

    # world markers
    for x in range(0, WORLD_WIDTH, 200):
        screen_x = x - camera.x
        pygame.draw.line(
            screen, (150, 150, 150),
            (screen_x, LANE_TOP),
            (screen_x, LANE_BOTTOM+player.height),
            2
        )

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
    # draw breakables
    for obj in objects:
        obj.draw(screen, camera.x)
    # draw loots
    for loot in loot_items:
        loot.draw(screen, camera.x)

def main_draw_ui(screen, camera, level, player, enemies, 
                    weapons, projectiles, enemy_projectiles, objects, loot_items):
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
    if player.state == Player.DEAD:
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


if __name__ == "__main__":
    main()
