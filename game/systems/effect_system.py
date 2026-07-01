from game.systems.explosive_system import ExplosiveSystem

class EffectSystem:
    @staticmethod
    def update(game_state):
        for spark in game_state.hit_sparks:
            spark.update()
        ExplosiveSystem.update_explosions(game_state)
