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
from game.effects.hit_spark import HitSpark
from game.game_state import GameState
from game.systems.inventory_system import *
from game.systems.wave_system import *
from game.systems.loot_system import *
from game.systems.projectile_system import *
from game.systems.combat_system import *
from game.systems.cleanup_system import *
from game.ui.score_manager import ScoreManager
from main_draw import *

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
    score_manager = ScoreManager()

    enemies = []
    weapons = [
            Weapon(900,350, "knife"),
            Weapon(1500,350, "bat"),
            Weapon(2000, 350, "pistol")]
    projectiles = []
    enemy_projectiles = []
    objects = [ # breakable objects
        BreakableObject(1100, 360),
        BreakableObject(1800, 360),
        BreakableObject(2500, 360),
    ]
    loot_items = []
    hit_sparks = []

    game_state = GameState(
        screen=screen,
        clock=clock,
        player=player,
        level=level,
        camera=camera,
        enemies=enemies,
        weapons=weapons,
        projectiles=projectiles,
        enemy_projectiles=enemy_projectiles,
        objects=objects,
        loot_items=loot_items,
        hit_sparks=hit_sparks,
        score_manager=score_manager
    )

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        update_player_weapon_interaction(game_state, keys)

        update_wave_system(game_state)
        ############# update #############
        # update player
        player.update()
        collect_player_projectiles(game_state)

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
            collect_enemy_projectile(game_state, enemy)

        update_projectiles(game_state)
            
        # update hit sparks
        for spark in hit_sparks:
            spark.update()

        # update camera
        if level.camera_locked:
            camera.update(player, level.lock_x)
        else:
            camera.update(player)

        handle_player_attack_collision(game_state)
        handle_player_projectile_collision(game_state)

        handle_enemy_projectile_collision(game_state)

        # has to be after enemy, object destroyed
        # and before dead enemy and broken object removed
        create_enemy_loot(game_state)
        create_object_loot(game_state)
        update_loot_pickup(game_state)

        cleanup_game_state(game_state)
        update_wave_completion(game_state)
        main_draw(game_state)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
