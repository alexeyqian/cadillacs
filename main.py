import pygame
from game.settings import *
from game.camera import Camera
from game.level.level import Level
from game.entities.player import Player
from game.entities.weapon import Weapon
from game.entities.breakable_object import BreakableObject
from game.entities.explosive_barrel import ExplosiveBarrel
from game.game_state import GameState
from game.systems.continue_system import *
from game.systems.gameplay_system import *
from game.systems.player_input_system import *
from game.ui.score_manager import ScoreManager
from game.ui.stage_clear_manager import StageClearManager
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
    stage_clear_manager = StageClearManager()

    enemies = []
    weapons = [
            # Light melee upgrade before fast enemies appear.
            Weapon(1500, 650, "knife"),
            # Heavy melee upgrade before the heavy enemy wave.
            Weapon(4050, 650, "bat"),
            # Ranged option before raptors, reinforcements, and boss.
            Weapon(6400, 650, "pistol")]
    projectiles = []
    enemy_projectiles = []
    objects = [ # breakable objects
        # Early recovery after the first warm-up wave.
        BreakableObject(1450, 670),
        # Recovery before the first medium mixed wave.
        BreakableObject(2850, 670),
        # Resource point before the heavy enemy introduction.
        BreakableObject(4200, 670),
        # Resource point before the raptor wave.
        BreakableObject(5550, 670),
        ExplosiveBarrel(5550, 670),
        # Recovery before the reinforcement wave.
        BreakableObject(6750, 670),
        # Final resource point before the boss.
        BreakableObject(8150, 670),
    ]
    loot_items = []
    hit_sparks = []
    floating_texts = []
    explosions = []

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
        score_manager=score_manager,
        floating_texts=floating_texts,
        stage_clear_manager=stage_clear_manager,
        explosions=explosions
    )

    running = True
    while running:
        # 1 process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                # insert coin as credit
                # useful for development, will remove in prod
                if event.key == pygame.K_5:
                    game_state.credits += 1
            if (game_state.stage_clear_manager.active
                    and game_state.stage_clear_manager.timer <= 0):
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        running = False # ??

        # 2 update continue
        keys = pygame.key.get_pressed()
        # player death and lives check, and related continue status
        if (player.state == player.DEAD 
            and player.lives <= 0 
            and game_state.credits > 0):
            game_state.continue_active = True

        update_continue_system(game_state, keys)

        # prevent gameplay while continue screen active
        if game_state.continue_active:
            main_draw(game_state)
            pygame.display.flip()
            clock.tick(FPS)
            continue

        if game_state.stage_clear_manager.active:
            # update stage clear manager
            game_state.stage_clear_manager.update()
            game_state.stage_clear_manager.apply_bonus(score_manager)
        else:
            # 3. update player input
            update_player_input_system(game_state, keys)
            # 4 update gameplay
            update_gameplay(game_state, keys)

        # 5. draw
        main_draw(game_state)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
