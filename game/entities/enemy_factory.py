from game.entities.ferris_enemy import FerrisEnemy
from game.entities.gneiss_enemy import GneissEnemy
from game.entities.black_elmer_enemy import BlackElmerEnemy

class EnemyFactory:
    @staticmethod
    def create_enemy(enemy_type, x, y):
        if enemy_type == "ferris":
            return FerrisEnemy(x, y)
        if enemy_type == "gneiss":
            return GneissEnemy(x, y)
        if enemy_type == "black_elmer":
            return BlackElmerEnemy(x, y)

        return FerrisEnemy(x, y)
