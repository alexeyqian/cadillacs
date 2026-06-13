from game.entities.basic_melee_enemy import BasicMeleeEnemy
from game.entities.enemy_config import get_enemy_config
from game.entities.fast_enemy import FastEnemy, FastSmallEnemy
from game.entities.heavy_enemy import HeavyEnemy
from game.entities.ranged_enemy import RangedEnemy
from game.entities.boss_enemy import BossEnemy
from game.entities.raptor_enemy import RaptorEnemy
from game.entities.weapon_enemy import WeaponEnemy
from game.entities.ferris_enemy import FerrisEnemy
from game.entities.gneiss_enemy import GneissEnemy
from game.entities.black_elmer_enemy import BlackElmerEnemy

class EnemyFactory:
    @staticmethod
    def create_enemy(enemy_type, x, y):
        if enemy_type == "boss":
            return BossEnemy(x, y)
        if enemy_type == "raptor":
            return RaptorEnemy(x, y)
        if enemy_type == "ferris":
            return FerrisEnemy(x, y)
        if enemy_type == "gneiss":
            return GneissEnemy(x, y)
        if enemy_type == "black_elmer":
            return BlackElmerEnemy(x, y)

        config = get_enemy_config(enemy_type)
        if config.archetype == "basic_melee":
            return BasicMeleeEnemy(x, y, enemy_type)
        if config.archetype == "fast_small":
            if enemy_type == "fast":
                return FastEnemy(x, y)
            return FastSmallEnemy(x, y, enemy_type)
        if config.archetype == "weapon":
            return WeaponEnemy(x, y, enemy_type)
        if config.archetype == "heavy":
            return HeavyEnemy(x, y, enemy_type)
        if config.archetype == "ranged":
            return RangedEnemy(x, y, enemy_type)

        return BasicMeleeEnemy(x, y, "normal")
