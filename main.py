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

        # create/trigger wave when player reaches trigger_x
        wave = level.get_current_wave()
        # only for SpawnWave
        if wave and wave.started:
            if hasattr(wave, "update"):
                enemies.extend(wave.update())

        # for normal Wave and BossWave
        # since they dont' implement update()
        if wave and not wave.started and player.x >= wave.trigger_x:
            # start the wave and initialize pending enemies
            wave.spawn()
            # lock camera only when wave actually starts
            # set lock_x to current camera.x so the viewport does not jump
            level.camera_locked = True
            level.lock_x = camera.x

        # if wave has started, spawn pending enemies over time
        if wave and wave.started and hasattr(wave, "update_spawn"):
            new_enemies = wave.update_spawn()
            if new_enemies:
                enemies.extend(new_enemies)
        # create loots when breakable destroys
        for enemy in enemies:
            if enemy.hp > 0:
                continue
            if enemy.loot_generated:
                continue
            loot = enemy.create_loot()
            if loot:
                loot_items.append(loot)
            enemy.loot_generated = True

        # collect player projectiles
        if player.pending_projectile:
            projectiles.append(player.pending_projectile)
            player.pending_projectile = None

        keys = pygame.key.get_pressed()
        update_player_weapon_interaction(player, weapons, keys)

        # auto pickup loot
        player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
        for loot in loot_items:
            if not loot.active:
                continue
            if player_rect.colliderect(loot.get_rect()):
                if loot.loot_type == "health":
                    player.hp = min(player.max_hp, player.hp + 30)
                elif loot.loot_type == "ammo":
                    if player.weapon and hasattr(player.weapon, "ammo"):
                        player.weapon.ammo += 10
                loot.active = False
        ############# update #############
        main_update(game_state)

        # player attack collision / combat detection
        attack_rect = player.get_attack_rect()
        if attack_rect and not player.already_hit_enemy:
            # attack enemies
            for enemy in enemies:
                enemy_rect = create_enemy_rect(enemy)
                if attack_rect.colliderect(enemy_rect):
                    enemy.take_damage(player.attack_damage(), player.x)
                    player.already_hit_enemy = True
                    hit_sparks.append(HitSpark(enemy.x+enemy.width//2,
                                        enemy.y + enemy.height//2))
                    break # ?? useless
            # attack breakables
            for obj in objects:
                if obj.destroyed:
                    continue
                if attack_rect.colliderect(obj.get_rect()):
                    obj.take_damage(player.attack_damage())

        # player projectile collision
        for projectile in projectiles:
            if not projectile.active:
                continue
            projectile_rect = projectile.get_rect()
            # projectile hit enemy
            for enemy in enemies:
                enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
                if projectile_rect.colliderect(enemy_rect):
                    enemy.take_damage(projectile.damage, player.x)
                    projectile.active = False
                    hit_sparks.append(HitSpark(enemy.x+enemy.width//2,
                                        enemy.y + enemy.height//2))
                    break
            # projectile hit breakable
            for obj in objects:
                if obj.destroyed:
                    continue
                if projectile_rect.colliderect(obj.get_rect()):
                    obj.take_damage(projectile.damage)
                    projectile.active = False
                    break

        # enemy projectile collision
        for projectile in enemy_projectiles:
            if not projectile.active:
                continue
            player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
            if projectile.get_rect().colliderect(player_rect):
                player.take_damage(projectile.damage)
                projectile.active = False

        # Create loot after combat damage, before destroyed objects are removed.
        for obj in objects:
            if obj.destroyed and not obj.loot_generated:
                loot = obj.create_loot()
                if loot:
                    loot_items.append(loot)
                obj.loot_generated = True
        
        main_cleanup(game_state)

        # wave completion logic
        wave = level.get_current_wave()
        if wave and wave.started:
            wave_finished = False
            if isinstance(wave, SpawnWave):
                wave_finished = wave.all_spawners_finished() and len(enemies) == 0
            else:
                wave_finished = len(enemies) == 0

            if wave_finished:
                wave.completed = True
                level.current_wave += 1
                level.camera_locked = False

        ############# draw #############
        main_draw(game_state)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


def update_player_weapon_interaction(player,weapons,keys):
    if keys[pygame.K_e]:
        if player.weapon is None:
            player_rect = pygame.Rect(
                player.x,player.y,
                player.width,player.height)
            for weapon in weapons:
                if weapon.picked_up:
                    continue
                if player_rect.colliderect(weapon.get_rect()):
                    player.pick_up_weapon(weapon)
                    break
    if keys[pygame.K_q]:
        player.drop_weapon()

def main_cleanup(game_state):
        # remove dead enemies
        game_state.enemies = [enemy for enemy in game_state.enemies if not enemy.is_ready_to_remove()]
        # clean up player projectiles
        game_state.projectiles = [p for p in game_state.projectiles if p.active]
        # clean up enemy projectiles
        game_state.enemy_projectiles = [p for p in game_state.enemy_projectiles if p.active]
        # clean up breakables
        game_state.objects = [obj for obj in game_state.objects if obj.hp > 0]
        # clean up loots
        game_state.loot_items = [l for l in game_state.loot_items if l.active]
        # clean up hit sparks
        game_state.hit_sparks = [s for s in game_state.hit_sparks if s.active]

if __name__ == "__main__":
    main()
