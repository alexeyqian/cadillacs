class EnemyState:
    IDLE = "IDLE"
    WALK = "WALK" # deprecated, patrol is good enough
    PATROL = "PATROL" # ai decisions
    CHASE = "CHASE"
    ATTACK = "ATTACK"
    # HIT means damaged; 
    # RECOIL means clash bounce/no damage
    HIT = "HIT"
    RECOIL = "RECOIL"
    DEAD = "DEAD"
    GRABBED = "GRABBED"
    THROWN = "THROWN"
    KNOCKDOWN = "KNOCKDOWN" # heavy hit or thrown cause enemy falls down briefly
    GETUP = "GETUP" # gets up after knockdown