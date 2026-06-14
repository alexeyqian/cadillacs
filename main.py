import os
import pygame
from game.settings import *
from game.camera import Camera
from game.level.level import Level
from game.entities.mustapha_player import MustaphaPlayer
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

def get_window_size():
    display_info = pygame.display.Info()
    display_w = display_info.current_w or EXTERNAL_WIDTH
    display_h = display_info.current_h or EXTERNAL_HEIGHT

    max_window_w = min(EXTERNAL_WIDTH, display_w)
    max_window_h = min(EXTERNAL_HEIGHT, display_h)
    scale = min(max_window_w / SCREEN_WIDTH, max_window_h / SCREEN_HEIGHT)
    scale = min(1.0, scale)

    return (
        max(1, int(SCREEN_WIDTH * scale)),
        max(1, int(SCREEN_HEIGHT * scale))
    )

def present_screen(screen, window):
    if screen.get_size() == window.get_size():
        window.blit(screen, (0, 0))
    else:
        scaled = pygame.transform.smoothscale(screen, window.get_size())
        window.blit(scaled, (0, 0))

    pygame.display.flip()

def create_stage_weapons(stage_data):
    weapons = []

    for weapon_config in stage_data["weapons"]:
        weapons.append(Weapon(
            weapon_config["x"],
            weapon_config["y"],
            weapon_config["type"]
        ))

    return weapons

def create_stage_objects(stage_data):
    objects = []

    for object_config in stage_data["objects"]:
        kind = object_config["kind"]

        if kind == "breakable":
            objects.append(BreakableObject(
                object_config["x"],
                object_config["y"]
            ))

        elif kind == "barrel":
            objects.append(ExplosiveBarrel(
                object_config["x"],
                object_config["y"]
            ))

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
    game_state.player.ground_y = start_y
    game_state.player.is_jumping = False
    game_state.player.vx = 0
    game_state.player.vy = 0
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

def advance_to_next_stage(game_state):
    next_stage_data = game_state.stage_manager.advance_stage()
    if next_stage_data:
        load_stage(game_state, next_stage_data)
        return True

    return False

def main():
    pygame.init()

    # Keep game logic/rendering in the 1920x1080 world coordinate system,
    # then scale the final frame to the actual display-sized window.
    window = pygame.display.set_mode(get_window_size(), pygame.NOFRAME)
    screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Cadillacs and Dinosaurs")

    clock = pygame.time.Clock()
    player = MustaphaPlayer()
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
    load_stage(game_state, stage_manager.get_current_stage())

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
            present_screen(screen, window)
            clock.tick(FPS)
            continue

        if game_state.stage_clear_manager.active:
            # update stage clear manager
            game_state.stage_clear_manager.update()
            game_state.stage_clear_manager.apply_bonus(score_manager)
            if game_state.stage_clear_manager.timer <= 0:
                running = advance_to_next_stage(game_state)
        else:
            # 3. update player input
            update_player_input_system(game_state, keys)
            # 4 update gameplay
            update_gameplay(game_state, keys)

        # 5. draw
        main_draw(game_state)

        present_screen(screen, window)
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
