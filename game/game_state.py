class GameState:
    def __init__(
        self,
        screen,
        clock,
        player,
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
        stage_clear_manager
    ):
        self.screen = screen
        self.clock = clock

        self.player = player
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
        
        self.continue_timer = 60
        self.continue_active = False
        self.continue_used = 0

        self.running = True