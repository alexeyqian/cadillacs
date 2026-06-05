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
        score=0,
        stage=1
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

        self.running = True