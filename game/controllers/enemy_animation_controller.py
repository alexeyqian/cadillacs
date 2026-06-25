from game.controllers.frame_animation_controller import FrameAnimationController


class EnemyAnimationController(FrameAnimationController):
    def __init__(self, owner, animation_data, anim_fps=None):
        super().__init__(animation_data, anim_fps)
        self.init_frame_animations(owner)

    def get_current_frame_data(self):
        return self.get_current_frame()

    def init_frame_animations(self, owner):
        for state, animation_name, loop in self.get_animation_specs(owner):
            self.add_frame_animation(state, animation_name, loop=loop)

    def get_animation_specs(self, owner):
        specs = [
            (owner.IDLE, "idle", True),
            (owner.WALK, "walk", True),
            (owner.ATTACK, "attack", False),
            (owner.HIT, "hit", True),
            (owner.DEAD, "dead", True),
        ]
        if owner.movement.can_run and "run" in self.animation_data:
            specs.append((owner.RUN, "run", True))
        if owner.movement.can_run_attack and "run_attack" in self.animation_data:
            specs.append((owner.RUN_ATTACK, "run_attack", False))
        if owner.movement.can_jump and "jump" in self.animation_data:
            specs.append((owner.JUMP, "jump", False))
        if owner.movement.can_jump_attack and "jump_attack" in self.animation_data:
            specs.append((owner.JUMP_ATTACK, "jump_attack", False))
        return specs

    def get_animation_state(self, owner):
        state_map = {
            owner.IDLE: owner.IDLE,
            owner.WALK: owner.WALK,
            owner.PATROL: owner.IDLE,
            owner.CHASE: owner.WALK,
            owner.RUN: owner.RUN if owner.movement.can_run else owner.WALK,
            owner.RUN_ATTACK: owner.RUN_ATTACK if owner.movement.can_run_attack else owner.ATTACK,
            owner.JUMP: owner.JUMP if owner.movement.can_jump else owner.IDLE,
            owner.JUMP_ATTACK: owner.JUMP_ATTACK if owner.movement.can_jump_attack else owner.IDLE,
            owner.ATTACK: owner.ATTACK,
            owner.HIT: owner.HIT,
            owner.RECOIL: owner.HIT,
            owner.GRABBED: owner.IDLE,
            owner.THROWN: owner.HIT,
            owner.KNOCKDOWN: owner.HIT,
            owner.GETUP: owner.IDLE,
            owner.DEAD: owner.DEAD,
        }
        return state_map.get(owner.state, owner.IDLE)
