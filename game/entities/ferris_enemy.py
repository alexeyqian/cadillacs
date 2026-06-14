from game.animation.ferris_data import *
from game.entities.enemy import Enemy

# Animation is visual part, is diff from above timing window part
#At 60 FPS, attack animation frame duration is:
#  60 / 6 = 10 game frames per sprite frame
#  Ferris has 3 attack sprite frames, so the visual attack animation loops
#  through frames roughly like:
# game frames 0-9    sprite attack frame 0
#  game frames 10-19   sprite attack frame 1
#  game frames 20-29   sprite attack frame 2

#That is why attack_windup = 20 is useful here: the active window starts
#  when sprite frame 2 appears, and Ferris’ attack_rect is on sprite frame 2.

"""
Best practice for this project:

  windup  = frames before the hit pose
  active  = frames where attack_rect should damage
  recovery = frames after hit pose before enemy can act again

  For frame-data enemies like Ferris, set them so the combat active window
  overlaps the sprite frames that have attack_rect.

  For Ferris currently:

  sprite frame 0: anticipation / early motion
  sprite frame 1: windup
  sprite frame 2: punch extended, has attack_rect

  windup = 20
  active = 8
  recovery = 25

  Good rule of thumb:

  - Light enemy punch: windup 12-20, active 5-8, recovery 15-25
  - Fast enemy jab: windup 8-14, active 4-6, recovery 12-18
  - Heavy enemy swing: windup 24-35, active 8-12, recovery 30-45
  - Boss attack: windup 30+, active 10-20, recovery 35+

  For maintainability, the best long-term setup would be to store attack
  timing beside the animation data, for example:

  FERRIS_ATTACK_TIMING = {
      "windup": 20,
      "active": 8,
      "recovery": 25,
  }

  Then FerrisEnemy can load those values instead of hardcoding them in the
  class.
"""
class FerrisEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, enemy_type="ferris",
                animation_data=FERRIS_ANIMATIONS,
                anim_fps=FERRIS_ANIM_FPS,
                sprite_scale=4)
