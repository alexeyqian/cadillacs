import pygame
from game.settings import *
from game.camera import Camera
from game.entities.player import Player
from game.entities.enemy import Enemy
from game.level.level import Level
from game.settings import LANE_TOP, LANE_BOTTOM

def create_enemy_rect(enemy):
    return pygame.Rect(enemy.x, enemy.y,
                enemy.width, enemy.height)

def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Cadillacs and Dinosaurs")

    font = pygame.font.SysFont(None, 30)
    small_font = pygame.font.SysFont(None, 20)
    big_font = pygame.font.SysFont(None, 60)

    clock = pygame.time.Clock()
    player = Player()
    level = Level()
    camera = Camera()
    enemies = []

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        ############# update #############
        # trigger wave
        wave = level.get_current_wave()
        if wave:
            if (not wave.started and player.x >= wave.trigger_x):
                enemies.extend(wave.spawn())
                # lock camera only when wave actually starts
                # set lock_x to current camera.x so the viewport does not jump
                level.camera_locked = True
                level.lock_x = camera.x # wave.trigger_x

        # update player
        player.update()
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

        # combat detection / player attack collision:
        attack_rect = player.get_attack_rect()
        if attack_rect and not player.already_hit_enemy:
            for enemy in enemies:
                enemy_rect = create_enemy_rect(enemy)
                if attack_rect.colliderect(enemy_rect):
                    enemy.take_damage(player.attack_damage(), player.x)
                    player.already_hit_enemy = True
                    break # ?? useless	

        # remove dead enemies
        enemies = [enemy for enemy in enemies if enemy.hp > 0]

        wave = level.get_current_wave()
        if wave and wave.started and len(enemies) == 0:
            wave.completed = True
            level.current_wave += 1
            level.camera_locked = False

        # if no enemies remain, show win screen and stop
        if len(enemies) == 0:
            screen.fill((120, 190, 255))
            game_win_text = big_font.render("YOU WIN!", True, (255, 215, 0))
            game_win_rect = game_win_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(game_win_text, game_win_rect)
            #pygame.display.flip()
            #pygame.time.delay(2000)  # pause 2 seconds so player can see the message
            #running = False
            #continue

        # update camera
        if level.camera_locked:
            camera.update(player, level.lock_x)
        else:
            camera.update(player)

        ############# draw #############
        # draw background
        screen.fill((120, 190, 255))
        # ground
        pygame.draw.rect(screen, (80, 180, 80),# green
                        (0, LANE_TOP, SCREEN_WIDTH, LANE_BOTTOM - LANE_TOP + player.height))

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

        # draw hp bar
        pygame.draw.rect(screen,
            (100,100,100), (20,20,200,20))
        hp_width = int(200 * (player.hp / player.max_hp))
        pygame.draw.rect(screen, (0,255,0), (20,20,hp_width,20))
        # hp text
        hp_text = font.render(f"HP: {player.hp}/{player.max_hp}", True, (0,0,0))
        screen.blit(hp_text, (230, 20))

        # debug text
        pos_text = small_font.render(
                f"Player x:{int(player.x)} y:{int(player.y)} State:{player.state} Combo:{player.combo_step} " 
                    + f"Camera x:{int(camera.x)} Wave:{level.current_wave + 1} Enemies:{len(enemies)}",
                True, (0,0,0))
        # stamp it to specific coordinates on the screen
        screen.blit(pos_text, (400, 20))
        # end of debugging
        
        # GAME OVER
        if player.state == Player.DEAD:
            game_over_text = big_font.render("GAME OVER", True, (255,0,0))
            game_over_rect = game_over_text.get_rect(
                    center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(game_over_text, game_over_rect)

        # flip
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
