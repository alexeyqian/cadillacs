import pygame

import game.settings as settings
from game.camera import Camera
from game.display import get_window_size
from game.factories.player_factory import PlayerFactory
from game.game_state import GameState
from game.level.level import Level
from game.level.stage_config import EPISODE_1_STAGES
from game.level.stage_loader import load_current_stage
from game.level.stage_manager import StageManager
from game.managers.score_manager import ScoreManager
from game.managers.stage_clear_manager import StageClearManager
from game.settings import SCREEN_HEIGHT, SCREEN_WIDTH


def create_display():
    # Keep game logic/rendering in the 1920x1080 world coordinate system.
    # By default the window uses the same size, so sprite pixels are not
    # silently reduced by final framebuffer scaling.
    window = pygame.display.set_mode(get_window_size(), pygame.NOFRAME)
    screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Cadillacs and Dinosaurs")
    return window, screen


def create_game_state(screen, clock):
    stage_manager = StageManager(EPISODE_1_STAGES, settings.START_STAGE)

    game_state = GameState(
        screen=screen,
        clock=clock,
        player=PlayerFactory.create_player(),
        stage_manager=stage_manager,
        level=Level(stage_manager.get_current_stage()),
        camera=Camera(),
        enemies=[],
        weapons=[],
        projectiles=[],
        enemy_projectiles=[],
        objects=[],
        loot_items=[],
        hit_sparks=[],
        score_manager=ScoreManager(),
        floating_texts=[],
        stage_clear_manager=StageClearManager(),
        explosions=[],
    )
    load_current_stage(game_state)
    return game_state
