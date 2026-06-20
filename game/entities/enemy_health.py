from game.components.character_health import CharacterHealth


class EnemyHealth(CharacterHealth):
    def __init__(self, max_hp):
        super().__init__(max_hp)
