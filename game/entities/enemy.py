from game.entities.character import Character
from game.data.enemy_config import get_enemy_config
from game.entities.enemy_state import EnemyState
from game.entities.enemy_health import EnemyHealth
from game.components.character_geometry import CharacterGeometry
from game.controllers.enemy_animation_controller import EnemyAnimationController
from game.components.enemy_renderer import EnemyRenderer
from game.components.enemy_movement import EnemyMovement
from game.components.enemy_flanking import EnemyFlanking
from game.components.enemy_lifecycle_state import EnemyLifecycleState
from game.controllers.enemy_combat_controller import EnemyCombatController
from game.controllers.enemy_reaction_controller import EnemyReactionController
from game.controllers.enemy_lifecycle_controller import EnemyLifecycleController
from game.controllers.enemy_state_controller import EnemyStateController
from game.controllers.enemy_loot_controller import EnemyLootController
from game.combat.damage_request import DamageRequest
from game.combat.hit_reaction import normalize_hit_reaction

# State controller: decides what state the enemy wants
# Movement: changes x/y/facing
# Combat: handles attack hit detection
# Lifecycle: advances temporary states
# Enemy is a small coordinator. Components own movement, combat,
# reactions, lifecycle, state decisions, loot, animation, and rendering.

class Enemy(Character, EnemyState):
    # attack_range: should i attack
    # attack_rect = did i hit
    # detect_range: within detect_range, enemy chases player
    # outside this range, enemy ignores player
    def __init__(self, x, y, enemy_type, 
                animation_data, anim_fps, sprite_scale=4):
        super().__init__(
            x=x,
            y=y,
            state=self.IDLE,
            facing_right=False,
            sprite_scale=sprite_scale,
        )

        self.configure_spawn_state(x, enemy_type)
        self.build_state_components()
        self.build_capability_components()
        self.build_controllers()
        self.configure_from_enemy_config(get_enemy_config(self.enemy_type))
        self.build_presentation_components(animation_data, anim_fps)

    def configure_spawn_state(self, x, enemy_type):
        self.enemy_type = enemy_type
        self.loot_generated = False

    def build_state_components(self):
        self.lifecycle_state = EnemyLifecycleState()

    def build_capability_components(self):
        self.geometry = CharacterGeometry()
        self.movement = EnemyMovement(spawn_x=self.x)
        self.flanking = EnemyFlanking()

    def build_controllers(self):
        self.combat_controller = EnemyCombatController()
        self.reaction_controller = EnemyReactionController()
        self.lifecycle_controller = EnemyLifecycleController()
        self.state_controller = EnemyStateController()
        self.loot_controller = EnemyLootController()

    def configure_from_enemy_config(self, config):
        self.apply_identity_config(config)
        self.apply_body_config(config)
        self.apply_movement_config(config)
        self.apply_combat_config(config)
        self.apply_reward_config(config)

    def build_presentation_components(self, animation_data, anim_fps):
        self.animation_controller = EnemyAnimationController(self, animation_data, anim_fps)
        self.renderer = EnemyRenderer()

    def apply_identity_config(self, config):
        self.enemy_id = config.enemy_id
        self.display_name = config.display_name
        self.archetype = config.archetype

    def apply_body_config(self, config):
        self.geometry.configure(
            config.collision_box_w,
            config.collision_box_h,
            config.hurt_box_w,
            config.hurt_box_h,
            config.hurt_box_offset_x,
            config.hurt_box_offset_y,
        )

        self.health = EnemyHealth(config.max_hp)
        self.sprite_scale = config.sprite_scale

    def apply_movement_config(self, config):
        self.movement.configure(
            speed=config.speed,
            patrol_distance=config.patrol_distance,
            detect_range=config.detect_range,
        )

    def apply_combat_config(self, config):
        self.attack_range = config.attack_range
        self.attack_lane_range = config.attack_lane_range

        self.combat_controller.attack_data = config.attack

        self.flinch_damage_threshold = config.flinch_damage_threshold
        self.attack_flinch_damage_threshold = (
            config.attack_flinch_damage_threshold
            if config.attack_flinch_damage_threshold is not None
            else config.flinch_damage_threshold
        )
        self.melee_attack_slot_limit = getattr(config, "melee_attack_slot_limit", None)

    def apply_reward_config(self, config):
        self.score_points = config.score_points

    def update(self, level, player, enemies):
        if self.lifecycle_controller.update_special_states(self):
            return

        self.lifecycle_controller.update_timers(self)

        if self.lifecycle_controller.update_hit_state(self):
            return

        self.reaction_controller.apply_knockback(self)

        dx, dy, distance_x, distance_y = self.movement.get_player_distance(self, player)

        if distance_x <= self.movement.detect_range:
            self.face_player(player)

        self.state_controller.choose_state(
            self, level, player, distance_x, distance_y, enemies
        )
        if self.state == self.ATTACK:
            self.update_animation()
            self.state_controller.execute_state(self, level, player, enemies, dx, dy)
        else:
            self.state_controller.execute_state(self, level, player, enemies, dx, dy)
            self.update_animation()

    # Lifecycle / reactions
    def is_ready_to_remove(self):
        return self.lifecycle_controller.is_ready_to_remove(self)

    def take_damage(
        self,
        damage,
        attacker_x=None,
        reaction=None,
        hit_stun_duration=None,
        knockback_velocity=None,
    ):
        if isinstance(damage, DamageRequest):
            request = damage
            damage = request.damage
            attacker_x = request.attacker_x if request.attacker_x is not None else attacker_x
            reaction = request.reaction
        if attacker_x is None:
            attacker_x = self.x

        reaction = normalize_hit_reaction(
            reaction,
            hit_stun_duration,
            knockback_velocity,
        )
        self.reaction_controller.take_damage(
            self,
            damage,
            attacker_x,
            reaction,
        )

    def grabbed_by_player(self):
        self.reaction_controller.grabbed_by_player(self)

    def thrown_by_player(self, direction, damage):
        self.reaction_controller.thrown_by_player(self, direction, damage)

    def take_grab_knee_damage(self, damage):
        self.reaction_controller.take_grab_knee_damage(self, damage)

    # Movement / state decisions
    def face_player(self, player):
        self.movement.face_player(self, player)

    # Combat
    def start_attack(self):
        self.combat_controller.start_attack(self)

    def start_clash_recovery(self):
        self.combat_controller.start_clash_recovery(self)

    def update_attack(self, level, player):
        self.combat_controller.update_attack(self, level, player)

    def is_attack_active(self):
        return self.combat_controller.is_attack_active(self)

    def get_attack_total_duration(self):
        return self.combat_controller.get_attack_data(self).total_duration

    def get_attack_phase_name(self):
        if self.state != self.ATTACK:
            return ""
        return self.combat_controller.attack_manager.get_phase_name()

    def get_attack_timing_label(self):
        if self.state != self.ATTACK:
            return ""
        return self.combat_controller.attack_manager.get_timing_label()

    # Rendering / animation / geometry
    def get_current_frame_data(self):
        return self.animation_controller.get_current_frame_data()

    def update_animation(self):
        self.animation_controller.update(self)

    # Loot
    def create_loot(self):
        return self.loot_controller.create_loot(self)
