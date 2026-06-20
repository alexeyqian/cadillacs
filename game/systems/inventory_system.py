import pygame

# add weapon.pickup_priority in future
def weapon_power(weapon):
    if weapon is None:
        return 0
    return weapon.damage

def update_player_weapon_interaction(game_state, keys):
    player = game_state.player
    weapons = game_state.weapons
    if player.air and not player.air.is_grounded:
        return

    player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
    for weapon in weapons:
        if weapon.picked_up:
            continue
        
        if not player_rect.colliderect(weapon.get_rect()):
            continue

        if player.weapon_slot.weapon is None:
            player.weapon_slot.pick_up(weapon)
            break

        current_power = weapon_power(player.weapon_slot.weapon)
        ground_power = weapon_power(weapon)
        if ground_power > current_power:
            player.weapon_slot.drop(player)
            player.weapon_slot.pick_up(weapon)
            break

    if keys[pygame.K_q]:
        player.weapon_slot.drop(player)
