from game.components.character_state import CharacterState


class PlayerState(CharacterState):
    RUN_ATTACK = "RUN_ATTACK"
    JUMP_TAKEOFF = "JUMP_TAKEOFF"
    JUMP = "JUMP"
    JUMP_ATTACK = "JUMP_ATTACK"
    LANDING = "LANDING"

    ATTACK_1 = "ATTACK_1"
    ATTACK_2 = "ATTACK_2"
    ATTACK_3 = "ATTACK_3"

    GRAB = "GRAB"
    GRAB_KNEE = "GRAB_KNEE"
    THROW = "THROW"
