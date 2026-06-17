import pygame
from game.effects.floating_text import FloatingText

# create loots when enemy destroyed
def create_enemy_loot(game_state):
    enemies = game_state.enemies
    loot_items = game_state.loot_items

    for enemy in enemies:
        if enemy.health.hp > 0:
            continue
        if enemy.loot_generated:
            continue
        loot = enemy.create_loot()
        if loot:
            loot_items.append(loot)
        
        base_points = game_state.score_manager.enemy_score(enemy)
        points = game_state.score_manager.get_combo_score(base_points)
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
    air = getattr(player, "air", None)
    if air and not air.is_grounded:
        return

    # inflate for easy to pickup
    player_rect = player.get_collision_rect().inflate(40, 40)
    for loot in loot_items:
        if not loot.active:
            continue

        if player_rect.colliderect(loot.get_rect()):
            # add condition to keep health pack if player doesn't need it
            if loot.loot_type == "health" and player.health.hp < player.health.max_hp:
                player.health.hp = min(player.health.max_hp, player.health.hp + 20)
                loot.active = False
            # add condition to keep ammo pack if player doesn't have gun
            elif loot.loot_type == "ammo":
                weapon = player.weapon_slot.weapon
                if weapon and weapon.is_ranged and hasattr(weapon, "ammo"):
                    weapon.ammo += 5
                    loot.active = False
