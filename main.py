import pygame
from game.settings import *
from game.camera import Camera
from game.entities.player import Player
from game.entities.enemy import Enemy

def create_enemy_rect(enemy):
    return pygame.Rect(enemy.x, enemy.y,
                enemy.width, enemy.height)

def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Cadillacs and Dinosaurs")
    font = pygame.font.SysFont(None, 30)

    clock = pygame.time.Clock()

    player = Player()
    camera = Camera()

    # create enemies
    enemies = [
        Enemy(700, 300),
        Enemy(1000, 400),
        Enemy(1400, 350),
        Enemy(1800, 320),
        Enemy(2200, 380)
    ]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        ############# update #############
        player.update()
        for enemy in enemies:
            enemy.update(player)

        # combat detection:
        attack_rect = player.get_attack_rect()
        if attack_rect and not player.already_hit:
            for enemy in enemies:
                enemy_rect = create_enemy_rect(enemy)
                if attack_rect.colliderect(enemy_rect):
                    enemy.take_damage(20, player.x)
                    player.already_hit = True
                    break # ?? useless	

        # remove dead enemies
        enemies = [enemy for enemy in enemies if enemy.hp > 0]

        camera.update(player)

        ############# draw #############
        screen.fill((120, 190, 255))
        # ground
        pygame.draw.rect(screen, 
                        (80, 180, 80),# green
                        (0, 250, SCREEN_WIDTH, 250))

        # world markers
        for x in range(0, WORLD_WIDTH, 200):
            screen_x = x - camera.x
            pygame.draw.line(
                screen,
                (150, 150, 150),
                (screen_x, 250),
                (screen_x, 500),
                2
            )
        
        # depth sorting
        # Classic beat'em-up games draw lower objects later.
        # other wise, may render incorrectly.
        # higher y draw later, appeas closer to camera
        # Exactly how arcade beat'em-ups fake depth.
        entities = []
        entities.append(player)
        for enemy in enemies:
            entities.append(enemy)
        entities.sort(key=lambda e: e.y)
        # draw entities
        for entity in entities:
            entity.draw(screen, camera.x)

        # debug text
        text1 = font.render(
                f"Player x: {int(player.x)} Camera x: {int(camera.x)}",
                True, (0,0,0))
        # stamp it to specific coordinates on the screen
        screen.blit(text1, (10, 10))
        text2 = font.render(
            f"Enemies: {len(enemies)}",
            True, (0, 0, 0))
        screen.blit(text2,(10, 40))
        # end of debugging

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()