from game.effects.floating_text import FloatingText


class LootSystem:
    @staticmethod
    def create_enemy_loot(game_state):
        for enemy in game_state.enemies:
            if enemy.health.hp > 0:
                continue
            if enemy.loot_controller.loot_generated:
                continue
            loot = enemy.create_loot()
            if loot:
                game_state.loot_items.append(loot)
            points = game_state.score_manager.get_combo_score(enemy.score_points)
            game_state.score_manager.add_score(points)
            game_state.floating_texts.append(
                FloatingText(enemy.x, enemy.y - 20, f"+{points}", (255, 255, 0)))
            enemy.loot_controller.loot_generated = True

    @staticmethod
    def create_object_loot(game_state):
        for obj in game_state.objects:
            if not obj.destroyed or obj.loot_generated:
                continue
            loot = obj.create_loot()
            if loot:
                game_state.loot_items.append(loot)
            game_state.score_manager.add_score(50)
            game_state.floating_texts.append(
                FloatingText(obj.x, obj.y - 20, "+50", (255, 255, 0)))
            obj.loot_generated = True

    @staticmethod
    def update_pickup(game_state):
        player = game_state.player
        if player.movement.air and not player.movement.air.is_grounded:
            return
        player_rect = player.get_collision_rect().inflate(200, 200)
        for loot in game_state.loot_items:
            if not loot.active:
                continue
            if not player_rect.colliderect(loot.get_rect()):
                continue
            if loot.loot_type == "health" and player.health.hp < player.health.max_hp:
                player.health.hp = min(player.health.max_hp, player.health.hp + 20)
                loot.active = False
            elif loot.loot_type == "ammo":
                weapon = player.weapon_slot.weapon
                if weapon and weapon.is_ranged:
                    weapon.ammo += 5
                    loot.active = False
