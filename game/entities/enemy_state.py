from game.components.character_state import CharacterState


class EnemyState(CharacterState):
    PATROL = "PATROL" # ai decisions
    CHASE = "CHASE"
    # HIT means damaged; 
    # RECOIL means clash bounce/no damage
    THROWN = "THROWN"
    KNOCKDOWN = CharacterState.KNOCKDOWN # heavy hit or thrown cause enemy falls down briefly
    GETUP = CharacterState.GETUP # gets up after knockdown
