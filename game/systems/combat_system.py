import pygame

def create_enemy_rect(enemy):
    return pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)

def handle_player_attack_collision(game_state):
    player = game_state.player
    enemies = game_state.enemies
    objects = game_state.objects

    attack_rect = player.get_attack_rect()
    if not attack_rect:
        return
    if player.already_hit_enemy:
        return

    # attack enemies
    for enemy in enemies:
        enemy_rect = create_enemy_rect(enemy)
        if attack_rect.colliderect(enemy_rect):
            enemy.take_damage(player.attack_damage(), player.x)
            game_state.score_manager.register_hit() # for combo score
            player.already_hit_enemy = True
            #hit_sparks.append(HitSpark(enemy.x+enemy.width//2,enemy.y + enemy.height//2))
            break # ?? useless, only can attack one enemy at a time?

    # attack breakables
    for obj in objects:
        if obj.destroyed:
            continue
        if attack_rect.colliderect(obj.get_rect()):
            obj.take_damage(player.attack_damage())
            
def handle_player_projectile_collision(game_state):
    player = game_state.player
    enemies = game_state.enemies
    objects = game_state.objects
    projectiles = game_state.projectiles

    for projectile in projectiles:
        if not projectile.active:
            continue

        projectile_rect = projectile.get_rect()
        # projectile hit enemy
        for enemy in enemies:
            enemy_rect = create_enemy_rect(enemy)
            if projectile_rect.colliderect(enemy_rect):
                enemy.take_damage(projectile.damage, player.x)
                game_state.score_manager.register_hit() # for combo score
                projectile.active = False
                #hit_sparks.append(HitSpark(enemy.x+enemy.width//2,enemy.y + enemy.height//2))
                break

        # projectile hit breakable
        for obj in objects:
            if obj.destroyed:
                continue

            if projectile_rect.colliderect(obj.get_rect()):
                obj.take_damage(projectile.damage)
                projectile.active = False
                break