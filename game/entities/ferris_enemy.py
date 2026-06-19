from game.animation.ferris_data import FERRIS_ANIMATIONS, FERRIS_ANIM_FPS
from game.entities.enemy import Enemy

# Ferris animation data owns the sprite frame slices and per-frame boxes.
# Combat timing stays in enemy_config.py so each enemy has one tuning source.
class FerrisEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, enemy_type="ferris",
                animation_data=FERRIS_ANIMATIONS,
                anim_fps=FERRIS_ANIM_FPS,
                sprite_scale=4)
