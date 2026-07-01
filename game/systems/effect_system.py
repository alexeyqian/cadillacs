
class EffectSystem:
    @staticmethod
    def update(game_state):
        for spark in game_state.hit_sparks:
            spark.update()
