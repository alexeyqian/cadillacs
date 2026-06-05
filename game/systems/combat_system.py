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

def handle_player_grab_or_throw(game_state, keys):
    player = game_state.player

    if keys[pygame.K_l]:
        if player.grab_pressed:
            return
        player.grab_pressed = True

        if player.grabbed_enemy:
            player.throw_grabbed_enemy()
            return
        
        for enemy in game_state.enemies:
            if player.can_grab_enemy(enemy):
                player.grab_enemy(enemy)
                break
    else:
        player.grab_pressed = False

def handle_player_thrown_enemy_collision(game_state):
    for thrown_enemy in game_state.enemies:
        if thrown_enemy.state != thrown_enemy.THROWN:
            continue
        thrown_rect = create_enemy_rect(thrown_enemy)
        for enemy in game_state.enemies:
            if enemy is thrown_enemy:
                continue
            if enemy.state == enemy.DEAD:
                continue
            # avoid process already hitted enemies because of thrown
            if id(enemy) in thrown_enemy.thrown_hit_targets:
                continue
            
            enemy_rect = create_enemy_rect(enemy)
            if thrown_rect.colliderect(enemy_rect):
                enemy.take_damage(45, thrown_enemy.x)
                thrown_enemy.thrown_hit_targets.add(id(enemy))
