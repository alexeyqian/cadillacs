import pygame


class InventorySystem:
    @staticmethod
    def update_weapon_interaction(game_state, keys):
        player = game_state.player
        if player.movement.air and not player.movement.air.is_grounded:
            return

        player_rect = player.get_collision_rect()
        for weapon in game_state.weapons:
            if weapon.picked_up:
                continue
            if not player_rect.colliderect(weapon.get_rect()):
                continue
            if player.weapon_slot.weapon is None:
                player.weapon_slot.pick_up(weapon)
                break
            if _weapon_power(weapon) > _weapon_power(player.weapon_slot.weapon):
                player.weapon_slot.drop(player)
                player.weapon_slot.pick_up(weapon)
                break

        if keys[pygame.K_q]:
            player.weapon_slot.drop(player)


def _weapon_power(weapon):
    return weapon.damage if weapon else 0
