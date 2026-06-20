class CharacterState:
    IDLE = "IDLE"
    WALK = "WALK"
    RUN = "RUN"
    ATTACK = "ATTACK"
    HIT = "HIT"
    # RECOIL means clash bounce/no damage
    RECOIL = "RECOIL"
    DEAD = "DEAD"

    # Shared control/recovery states. Enemies use these today; players are
    # expected to support them as grab and knockdown rules grow.
    GRABBED = "GRABBED"
    KNOCKDOWN = "KNOCKDOWN"
    GETUP = "GETUP"
