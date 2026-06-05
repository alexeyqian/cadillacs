import pygame
from game.effects.floating_text import FloatingText

# create loots when enemy destroyed
def create_enemy_loot(game_state):
    enemies = game_state.enemies
    loot_items = game_state.loot_items

    for enemy in enemies:
        if enemy.hp > 0:
            continue
        if enemy.loot_generated:
            continue
        loot = enemy.create_loot()
        if loot:
            loot_items.append(loot)
        
        points = game_state.score_manager.enemy_score(enemy)
        game_state.score_manager.add_score(points)
        floating_text = FloatingText(enemy.x, enemy.y - 20, f"+{points}", (255, 255, 0))
        game_state.floating_texts.append(floating_text)
        enemy.loot_generated = True

# create loots when breakable objects destroyed
# before destroyed objects are removed.
def create_object_loot(game_state):
    objects = game_state.objects
    loot_items = game_state.loot_items

    for obj in objects:
        if obj.destroyed and not obj.loot_generated:
            loot = obj.create_loot()
            if loot:
                loot_items.append(loot)
            points = game_state.score_manager.object_score(obj)
            game_state.score_manager.add_score(points)
            floating_text = FloatingText(obj.x, obj.y - 20, f"+{points}", (255, 255, 0))
            game_state.floating_texts.append(floating_text)
            obj.loot_generated = True

def update_loot_pickup(game_state):
    player = game_state.player
    loot_items = game_state.loot_items

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