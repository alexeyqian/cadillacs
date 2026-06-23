from game.animation.blade_data import BLADE_ANIMATIONS
from game.entities.enemy import Enemy

# Ferris animation data owns the sprite frame slices and per-frame boxes.
# Combat timing stays in enemy_config.py so each enemy has one tuning source.
class BladeEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, enemy_type="blade",
                animation_data=BLADE_ANIMATIONS,
                sprite_scale=4)
