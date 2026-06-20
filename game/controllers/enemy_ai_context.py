from dataclasses import dataclass


@dataclass
class EnemyAIContext:
    level: object
    player: object
    enemies: list
