from game.components.character_state import CharacterState


class EnemyState(CharacterState):
    PATROL = "PATROL" # ai decisions
    CHASE = "CHASE"
    RUN = "RUN"
    RUN_ATTACK = "RUN_ATTACK"
    JUMP = "JUMP"
    JUMP_ATTACK = "JUMP_ATTACK"
    THROWN = "THROWN"
    KNOCKDOWN = CharacterState.KNOCKDOWN # heavy hit or thrown cause enemy falls down briefly
    GETUP = CharacterState.GETUP # gets up after knockdown
