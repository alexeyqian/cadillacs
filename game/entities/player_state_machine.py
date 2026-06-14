class PlayerState:
    name = ""

    def enter(self, owner):
        pass

    def exit(self, owner):
        pass

    def update(self, owner):
        pass


class IdleState(PlayerState):
    name = "IDLE"


class WalkState(PlayerState):
    name = "WALK"


class RunState(PlayerState):
    name = "RUN"


class JumpState(PlayerState):
    name = "JUMP"


class AttackState(PlayerState):
    name = "ATTACK"


class Attack1State(PlayerState):
    name = "ATTACK_1"


class Attack2State(PlayerState):
    name = "ATTACK_2"


class Attack3State(PlayerState):
    name = "ATTACK_3"


class RunAttackState(PlayerState):
    name = "RUN_ATTACK"


class JumpAttackState(PlayerState):
    name = "JUMP_ATTACK"


class HitState(PlayerState):
    name = "HIT"


class DeadState(PlayerState):
    name = "DEAD"


class GrabState(PlayerState):
    name = "GRAB"


class GrabKneeState(PlayerState):
    name = "GRAB_KNEE"


class ThrowState(PlayerState):
    name = "THROW"


class PlayerStateMachine:
    def __init__(self, owner):
        self.states = {
            owner.IDLE: IdleState(),
            owner.WALK: WalkState(),
            owner.RUN: RunState(),
            owner.JUMP: JumpState(),
            owner.ATTACK: AttackState(),
            owner.ATTACK_1: Attack1State(),
            owner.ATTACK_2: Attack2State(),
            owner.ATTACK_3: Attack3State(),
            owner.RUN_ATTACK: RunAttackState(),
            owner.JUMP_ATTACK: JumpAttackState(),
            owner.HIT: HitState(),
            owner.DEAD: DeadState(),
            owner.GRAB: GrabState(),
            owner.GRAB_KNEE: GrabKneeState(),
            owner.THROW: ThrowState(),
        }
        self.current_state = self.states[owner.IDLE]

    def change_to(self, owner, state_name):
        if owner.state == state_name:
            return

        self.current_state.exit(owner)
        owner.state = state_name
        self.current_state = self.states.get(state_name, self.states[owner.IDLE])
        self.current_state.enter(owner)

    def update(self, owner):
        self.current_state.update(owner)