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
from main_update import *
from main_draw import *
from game.effects.hit_spark import HitSpark
from game.game_state import GameState
from game.systems.inventory_system import *
from game.systems.wave_system import *
from game.systems.loot_system import *
from game.systems.projectile_system import *
from game.systems.combat_system import *

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
        hit_sparks=hit_sparks
    )

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        update_wave_system(game_state)

        keys = pygame.key.get_pressed()
        update_player_weapon_interaction(player, weapons, keys)

        ############# update #############
        main_update(game_state)

        handle_player_attack_collision(game_state)
        handle_player_projectile_collision(game_state)

        handle_enemy_projectile_collision(game_state)

        # has to be after enemy, object destroyed
        # and before dead enemy and broken object removed
        create_enemy_loot(game_state)
        create_object_loot(game_state)

        update_loot_pickup(game_state)

        main_cleanup(game_state)
        update_wave_completion(game_state)
        main_draw(game_state)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

def main_cleanup(game_state):
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

if __name__ == "__main__":
    main()
