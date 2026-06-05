import pygame

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
            obj.loot_generated = True
