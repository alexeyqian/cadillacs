class EnemyState:
    IDLE = "IDLE"
    WALK = "WALK" # deprecated, patrol is good enough
    PATROL = "PATROL" # ai decisions
    CHASE = "CHASE"
    ATTACK = "ATTACK"
    HIT = "HIT"
    DEAD = "DEAD"
    GRABBED = "GRABBED"
    THROWN = "THROWN"
    KNOCKDOWN = "KNOCKDOWN" # heavy hit or thrown cause enemy falls down briefly
    GETUP = "GETUP" # gets up after knockdown