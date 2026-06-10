import os
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
from game.level.stage_manager import StageManager
from game.level.stage_config import EPISODE_1_STAGES
from main_draw import *

os.environ["SDL_VIDEO_WINDOW_POS"] = "0,0"
#info = pygame.display.Info()

def load_stage(game_state, stage_data):
    pass

def main():
    pygame.init()

    # internal screen mode for production, not used yet
    #window = pygame.display.set_mode((EXTERNAL_WIDTH, EXTERNAL_HEIGHT), pygame.NOFRAME) # for monitor
    #screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)) # for entire game area

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.NOFRAME)
    pygame.display.set_caption("Cadillacs and Dinosaurs")

    clock = pygame.time.Clock()
    player = Player()
    stage_manager = StageManager(EPISODE_1_STAGES)
    level = Level(stage_manager.get_current_stage())
    camera = Camera()
    
    score_manager = ScoreManager()
    stage_clear_manager = StageClearManager()

    enemies = []
    weapons = [
            # Light melee upgrade before fast enemies appear.
            Weapon(STAGE1_WAVE1_X - 50, SCREEN_HEIGHT-100, "knife"),
            # Heavy melee upgrade before the heavy enemy wave.
            Weapon(STAGE1_WAVE2_X - 50, SCREEN_HEIGHT-100, "bat"),
            # Ranged option before raptors, reinforcements, and boss.
            Weapon(STAGE1_WAVE3_X - 50, SCREEN_HEIGHT-100, "pistol")]
    projectiles = []
    enemy_projectiles = []
    # todo: move to level configs
    objects = [ # breakable objects
        # Early recovery after the first warm-up wave.
        BreakableObject(STAGE1_WAVE1_X - 20, SCREEN_HEIGHT-10),
        # Recovery before the first medium mixed wave.
        BreakableObject(STAGE1_WAVE1_X - 40, SCREEN_HEIGHT-10),
        # Resource point before the heavy enemy introduction.
        BreakableObject(STAGE1_WAVE2_X - 20, SCREEN_HEIGHT-10),
        # Resource point before the raptor wave.
        BreakableObject(STAGE1_WAVE2_X - 40, SCREEN_HEIGHT-10),
        ExplosiveBarrel(STAGE1_WAVE2_X - 60, SCREEN_HEIGHT-10),
        # Recovery before the reinforcement wave.
        BreakableObject(STAGE1_WAVE3_X - 20, SCREEN_HEIGHT-10),
        # Final resource point before the boss.
        BreakableObject(STAGE1_WAVE3_X - 40, SCREEN_HEIGHT-10),
    ]
    loot_items = []
    hit_sparks = []
    floating_texts = []
    explosions = []

    game_state = GameState(
        screen=screen,
        clock=clock,
        player=player,
        stage_manager=stage_manager,
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
        # 1 handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                # todo: insert coin as credit, only use for dev
                if event.key == pygame.K_5:
                    game_state.credits += 1
                if event.key == pygame.K_RETURN:
                    if(game_state.stage_clear_manager.active and
                        game_state.stage_clear_manager.timer <= 0):
                        next_stage_data = game_state.stage_manager.advance_stage()
                        if next_stage_data:
                            load_stage(game_state, next_stage_data)
                        else:
                            running = False # ? game over or last episode win

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

        # internal screen mode for production, not used yet
        #scaled = pygame.transform.smoothscale(screen, window.get_size())
        #window.blit(scaled, (0,0))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
