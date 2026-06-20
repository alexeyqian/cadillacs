from game.effects.explosion import Explosion
from game.effects.floating_text import FloatingText
from game.systems.camera_effect_system import explosion_shake

def create_explosions_from_objects(game_state):
    for obj in game_state.objects:
        if not obj.explosive:
            continue
        if not obj.destroyed:
            continue
        if obj.exploded:
            continue
        obj.exploded = True

        obj_rect = obj.get_rect()
        game_state.explosions.append(Explosion(obj_rect.centerx, obj_rect.centery))
        explosion_shake(game_state)
        game_state.score_manager.add_score(100)
        _damage_enemies_in_radius(game_state,
            obj_rect.centerx, obj_rect.centery, 180, 80)

def _damage_enemies_in_radius(game_state, x, y, radius, damage):
    for enemy in game_state.enemies:
        enemy_hurt_rect = enemy.get_hurt_rect()
        dx = (enemy_hurt_rect.x + enemy_hurt_rect.width // 2) - x
        dy = (enemy_hurt_rect.y + enemy_hurt_rect.height // 2) - y
        distance_sq = dx*dx + dy*dy
        if distance_sq <= radius*radius:
            enemy.take_damage(damage, x)
            game_state.floating_texts.append(
                FloatingText(enemy.x, enemy.y-20, str(damage), (250, 120,0)))
            
def update_explosions(game_state):
    for explosion in game_state.explosions:
        explosion.update()
