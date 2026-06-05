import pygame

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