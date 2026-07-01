class InventorySystem:
    @staticmethod
    def update_weapon_interaction(game_state):
        player = game_state.player
        if not player.movement.air or player.movement.air.is_grounded:
            _try_pickup_weapon(player, game_state.weapons)


def _try_pickup_weapon(player, weapons):
    player_rect = player.get_collision_rect()
    for weapon in weapons:
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


def _weapon_power(weapon):
    return weapon.damage if weapon else 0
