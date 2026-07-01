from game.managers.announcement_manager import AnnouncementManager
from game.core.sound_manager import SoundManager

class GameState:
    def __init__(
        self,
        screen,
        clock,
        player,
        stage_manager,
        level,
        camera,
        
        enemies,
        weapons,
        projectiles,
        enemy_projectiles,
        objects,
        loot_items,
        hit_sparks,
        score_manager,
        floating_texts,
        stage_clear_manager,
        explosions
    ):
        self.screen = screen
        self.clock = clock

        self.player = player
        self.stage_manager = stage_manager
        self.level = level
        self.camera = camera

        self.enemies = enemies
        self.weapons = weapons
        self.projectiles = projectiles
        self.enemy_projectiles = enemy_projectiles
        self.objects = objects
        self.loot_items = loot_items
        self.hit_sparks = hit_sparks
        self.score_manager = score_manager
        self.floating_texts = floating_texts
        self.stage_clear_manager = stage_clear_manager

        self.credits = 3
        self.continue_timer = 600
        self.continue_active = False
        self.continue_used = 0

        self.announcement_manager = AnnouncementManager()
        self.explosions = explosions
        self.sound_manager = SoundManager()

        self.running = True
        # Game paused flag. Toggle with P key to pause/resume gameplay.
        self.paused = False
        # Pause menu state
        self.pause_menu_options = ["Resume", "Restart Stage", "Quit"]
        self.pause_menu_index = 0