from game.controllers.frame_animation_controller import FrameAnimationController
from game.tuning import scale_animation_fps_map


class PlayerAnimationController(FrameAnimationController):
    def __init__(self, owner, animation_data, anim_fps=None):
        super().__init__(animation_data, scale_animation_fps_map(anim_fps) if anim_fps else None)
        self.init_animations(owner)

    def init_animations(self, owner):
        for state, animation_name, loop in self.get_animation_specs(owner):
            frames, duration = self.add_frame_animation(state, animation_name, loop=loop)
            total_duration = self.animation_total_duration(len(frames), duration)

            if state == owner.THROW:
                owner.grab_controller.throw_duration = total_duration
            elif state == owner.GRAB_KNEE:
                owner.grab_controller.grab_knee_duration = total_duration

    def get_animation_specs(self, owner):
        # (state_key, animation_name, loop)
        specs = [
            (owner.IDLE,       "idle",       True),
            (owner.WALK,       "walk",       True),
            (owner.RUN,        "run",        True),
            (owner.JUMP,       "jump",       False),
            (owner.ATTACK,     "attack",     False),
            (owner.ATTACK2,    "attack2",    False),
            (owner.ATTACK3,    "attack3",    False),
            (owner.RUN_ATTACK, "run_attack", False),
            (owner.JUMP_ATTACK,"jump_attack",False),
            (owner.GRAB,       "grab",       True),
            (owner.THROW,      "throw",      False),
            (owner.GRAB_KNEE,  "grab_knee",  False),
            (owner.HIT,        "hit",        True),
            (owner.DEAD,       "dead",       False),
        ]
        # Register optional armed/weapon-attack animations when present in data.
        for key, loop in (("walk_armed", True), ("ATTACK_KNIFE", False), ("ATTACK_PISTOL", False)):
            if key in self.animation_data and not self.animation_data[key].get("not_used"):
                specs.append((key, key, loop))
        return specs

    def get_animation_state(self, owner):
        weapon = owner.weapon_slot.weapon
        weapon_type = weapon.weapon_type if weapon else None

        walk_state = self._armed_walk_state(owner, weapon_type)
        attack_state = self._weapon_attack_state(owner, weapon_type)

        state_map = {
            owner.IDLE: owner.IDLE,
            owner.WALK: walk_state,
            owner.RUN: owner.RUN,
            owner.JUMP: owner.JUMP,
            owner.ATTACK: attack_state,
            owner.ATTACK2: owner.ATTACK2,
            owner.ATTACK3: owner.ATTACK3,
            owner.RUN_ATTACK: owner.RUN_ATTACK,
            owner.JUMP_ATTACK: owner.JUMP_ATTACK,
            owner.GRAB: owner.GRAB,
            owner.GRAB_KNEE: owner.GRAB_KNEE,
            owner.THROW: owner.THROW,
            owner.HIT: owner.HIT,
            owner.RECOIL: owner.HIT,
            owner.DEAD: owner.DEAD,
        }
        return state_map.get(owner.state, owner.IDLE)

    def _armed_walk_state(self, owner, weapon_type):
        if weapon_type and "walk_armed" in self.animation_data:
            if not self.animation_data["walk_armed"].get("not_used"):
                return "walk_armed"
        return owner.WALK

    def _weapon_attack_state(self, owner, weapon_type):
        if weapon_type == "knife" and "ATTACK_KNIFE" in self.animation_data:
            if not self.animation_data["ATTACK_KNIFE"].get("not_used"):
                return "ATTACK_KNIFE"
        if weapon_type == "pistol" and "ATTACK_PISTOL" in self.animation_data:
            if not self.animation_data["ATTACK_PISTOL"].get("not_used"):
                return "ATTACK_PISTOL"
        return owner.ATTACK
