from game.effects.explosion import Explosion
from game.effects.floating_text import FloatingText
from game.systems.camera_effect_system import explosion_shake

def create_explosions_from_objects(game_state):
    for obj in game_state.objects:
        if not getattr(obj, "explosive", False):
            continue
        if not obj.destroyed:
            continue
        if obj.exploded:
            continue
        obj.exploded = True
        
        game_state.explosions.append(Explosion(obj.x+obj.width//2, obj.y+obj.height//2))
        explosion_shake(game_state)
        game_state.score_manager.add_score(100)
        damage_enemies_in_radius(game_state,
            obj.x + obj.width//2, obj.y + obj.height//2, 180, 80)

def damage_enemies_in_radius(game_state, x, y, radius, damage):
    for enemy in game_state.enemies:
        dx = (enemy.x + enemy.width // 2) - x
        dy = (enemy.y + enemy.height // 2) - y
        distance_sq = dx*dx + dy*dy
        if distance_sq <= radius*radius:
            enemy.take_damage(damage, x)
            game_state.floating_texts.append(
                FloatingText(enemy.x, enemy.y-20, str(damage), (250, 120,0)))
            
def update_explosions(game_state):
    for explosion in game_state.explosions:
        explosion.update()