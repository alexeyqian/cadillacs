from game.entities.character_state import CharacterState


class EnemyState(CharacterState):
    WALK = CharacterState.WALK # deprecated, patrol is good enough
    PATROL = "PATROL" # ai decisions
    CHASE = "CHASE"
    # HIT means damaged; 
    # RECOIL means clash bounce/no damage
    THROWN = "THROWN"
    KNOCKDOWN = CharacterState.KNOCKDOWN # heavy hit or thrown cause enemy falls down briefly
    GETUP = CharacterState.GETUP # gets up after knockdown
