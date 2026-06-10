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

def create_stage_weapons(stage_data):
    wave_positions = stage_data["wave_positions"]
    if len(wave_positions) == 0:
        return []
    weapons = []
    if len(wave_positions) >= 1:
        weapons.append(Weapon(wave_positions[0] - 50, SCREEN_HEIGHT - 100, "knife"))

    if len(wave_positions) >= 2:
        weapons.append(Weapon(wave_positions[1] - 50, SCREEN_HEIGHT - 100, "bat"))

    if len(wave_positions) >= 3:
        weapons.append(Weapon(wave_positions[2] - 50, SCREEN_HEIGHT - 100, "pistol"))

    return weapons

def create_stage_objects(stage_data):
    wave_positions = stage_data["wave_positions"]

    if len(wave_positions) == 0:
        return []

    objects = []

    for wave_x in wave_positions:
        objects.append(BreakableObject(wave_x - 20, SCREEN_HEIGHT - 10))
        objects.append(BreakableObject(wave_x - 40, SCREEN_HEIGHT - 10))

    if len(wave_positions) >= 2:
        objects.append(ExplosiveBarrel(wave_positions[1] - 60, SCREEN_HEIGHT - 10))

    return objects

def load_stage(game_state, stage_data):
    game_state.level = Level(stage_data)

    # Do not create a new Player. Keep the same player so lives, score, 
    # and weapon behavior can be decided intentionally later.
    start_x, start_y = stage_data["player_start"]
    game_state.player.x = start_x
    game_state.player.y = start_y
    game_state.player.respawn_x = start_x
    game_state.player.respawn_y = start_y
    game_state.player.lane_top = stage_data["lane_top"] #todo: remove
    game_state.player.lane_bottom = stage_data["lane_bottom"] #todo: remove
    game_state.player.state = game_state.player.IDLE
    game_state.player.facing_right = True

    game_state.camera.x = 0

    game_state.enemies.clear()
    game_state.weapons.clear()
    game_state.projectiles.clear()
    game_state.enemy_projectiles.clear()
    game_state.objects.clear()
    game_state.loot_items.clear()
    game_state.hit_sparks.clear()
    game_state.floating_texts.clear()
    game_state.explosions.clear()

    game_state.weapons.extend(create_stage_weapons(stage_data))
    game_state.objects.extend(create_stage_objects(stage_data))

    game_state.stage_clear_manager.active = False
    game_state.stage_clear_manager.timer = 0
    game_state.stage_clear_manager.bonus_applied = False

    game_state.announcement_manager.active = False

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
    weapons = create_stage_weapons(stage_manager.get_current_stage())

    projectiles = []
    enemy_projectiles = []
    objects = create_stage_objects(stage_manager.get_current_stage())
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
